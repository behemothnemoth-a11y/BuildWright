from __future__ import annotations
from collections import Counter
from typing import Any

from composition.compiler import _astra_be
from composition.transforms import transform_fixture_blocks, transform_grid_words, transform_pos, transform_state

from .model import CARDINAL, Connection, ModuleSpec, ProjectPlan, Port, port_for
from .solver import OUT, PlacedModule, world_port

Vec3 = tuple[int, int, int]

def _add(a: Vec3, b: Vec3) -> Vec3:
    return tuple(a[i] + b[i] for i in range(3))

def module_payload(module: ModuleSpec, placement: PlacedModule):
    ox, oy, oz = placement.origin
    transformed = transform_fixture_blocks(module.source["blocks"], module.source_size, module.rotation, module.mirror)
    blocks = {}
    for block in transformed:
        x, y, z = block["pos"]
        blocks[(ox + x, oy + y, oz + z)] = block["state"]

    block_entities = []
    for host in module.source.get("microblock_hosts", []):
        local = transform_pos(tuple(host["pos"]), module.source_size, module.rotation, module.mirror)
        pos = (ox + local[0], oy + local[1], oz + local[2])
        words = [int(h, 16) for h in host["occupancy_words_hex"]]
        words = transform_grid_words(words, module.rotation, module.mirror)
        block_entities.append(_astra_be(pos, words, host.get("host_material", "stone")))
    return blocks, block_entities

def merge_modules(plan: ProjectPlan, placed: dict[str, PlacedModule]):
    blocks: dict[Vec3, str] = {}
    block_entities: list[dict[str, Any]] = []
    conflicts = Counter()
    for module_id in plan.modules:
        module = plan.modules[module_id]
        payload, entities = module_payload(module, placed[module_id])
        for pos, state in payload.items():
            if pos in blocks and blocks[pos] != state:
                conflicts[(blocks[pos], state)] += 1
            blocks[pos] = state
        block_entities.extend(entities)
    warnings = []
    if conflicts:
        total = sum(conflicts.values())
        warnings.append(f"{total} overlapping module block-state conflicts reconciled by graph order")
    return blocks, block_entities, warnings

def _opening_cells(anchor: Vec3, port: Port, width: int | None = None, height: int | None = None):
    x, y, z = anchor
    width = int(width or port.width)
    height = int(height or port.height)
    half = width // 2
    if port.side in ("north", "south"):
        for yy in range(y, y + height):
            for xx in range(x - half, x - half + width):
                for zz in range(z - 1, z + 2):
                    yield (xx, yy, zz)
    elif port.side in ("west", "east"):
        for yy in range(y, y + height):
            for zz in range(z - half, z - half + width):
                for xx in range(x - 1, x + 2):
                    yield (xx, yy, zz)
    else:
        depth = max(1, port.depth)
        for yy in range(y - 1, y + 2):
            for xx in range(x - half, x - half + width):
                for zz in range(z - depth // 2, z - depth // 2 + depth):
                    yield (xx, yy, zz)
def carve_connections(plan: ProjectPlan, placed: dict[str, PlacedModule], blocks: dict[Vec3, str]):
    for connection in plan.connections:
        a_mod = plan.modules[connection.a_module]
        b_mod = plan.modules[connection.b_module]
        a = world_port(placed[a_mod.id].origin, port_for(a_mod, connection.a_port))
        b = world_port(placed[b_mod.id].origin, port_for(b_mod, connection.b_port))
        width = int(connection.width or min(a.width, b.width))
        height = int(connection.height or min(a.height, b.height))
        for pos in _opening_cells(a.pos, a, width, height):
            blocks.pop(pos, None)
        for pos in _opening_cells(b.pos, b, width, height):
            blocks.pop(pos, None)

def build_straight_corridors(plan: ProjectPlan, placed: dict[str, PlacedModule], blocks: dict[Vec3, str]):
    floor_state = "minecraft:polished_deepslate"
    wall_state = "minecraft:tuff_bricks"
    ceiling_state = "minecraft:dark_oak_planks"
    for connection in plan.connections:
        if connection.mode != "corridor":
            continue
        a_mod = plan.modules[connection.a_module]
        b_mod = plan.modules[connection.b_module]
        a = world_port(placed[a_mod.id].origin, port_for(a_mod, connection.a_port))
        b = world_port(placed[b_mod.id].origin, port_for(b_mod, connection.b_port))
        width = int(connection.width or min(a.width, b.width))
        height = int(connection.height or min(a.height, b.height))
        _corridor_between(blocks, a.pos, b.pos, a.side, width, height, floor_state, wall_state, ceiling_state)

def _corridor_between(blocks, start: Vec3, end: Vec3, side: str, width: int, height: int, floor_state: str, wall_state: str, ceiling_state: str):
    sx, sy, sz = start
    ex, ey, ez = end
    if sy != ey:
        raise ValueError("Straight corridor endpoints must share connector floor elevation")
    half = width // 2
    base_y = sy - 1
    if side in ("east", "west"):
        lo, hi = sorted((sx, ex))
        for x in range(lo, hi + 1):
            for z in range(sz - half, sz - half + width):
                blocks[(x, base_y, z)] = floor_state
                blocks[(x, base_y + height + 1, z)] = ceiling_state
                for y in range(base_y + 1, base_y + height + 1):
                    if z in (sz - half, sz - half + width - 1):
                        blocks[(x, y, z)] = wall_state
                    else:
                        blocks.pop((x, y, z), None)
    elif side in ("north", "south"):
        lo, hi = sorted((sz, ez))
        for z in range(lo, hi + 1):
            for x in range(sx - half, sx - half + width):
                blocks[(x, base_y, z)] = floor_state
                blocks[(x, base_y + height + 1, z)] = ceiling_state
                for y in range(base_y + 1, base_y + height + 1):
                    if x in (sx - half, sx - half + width - 1):
                        blocks[(x, y, z)] = wall_state
                    else:
                        blocks.pop((x, y, z), None)
    else:
        raise ValueError(f"Corridor mode requires cardinal ports, got {side}")

def exterior_sides(plan: ProjectPlan):
    interior = set()
    for c in plan.connections:
        if c.mode == "attach":
            interior.add((c.a_module, port_for(plan.modules[c.a_module], c.a_port).side))
            interior.add((c.b_module, port_for(plan.modules[c.b_module], c.b_port).side))
    return {
        m.id: [side for side in ("north", "south", "east", "west") if (m.id, side) not in interior]
        for m in plan.modules.values()
    }
