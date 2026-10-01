from __future__ import annotations
from typing import Any

from .assembler import exterior_sides
from .model import ProjectPlan
from .solver import OUT, PlacedModule, world_port

Vec3 = tuple[int, int, int]

def _out_pos(module: PlacedModule, side: str, along: int, y: int, depth: int = 1) -> Vec3:
    ox, oy, oz = module.origin
    w, h, d = module.size
    if side == "north":
        return (ox + along, oy + y, oz - depth)
    if side == "south":
        return (ox + along, oy + y, oz + d - 1 + depth)
    if side == "west":
        return (ox - depth, oy + y, oz + along)
    return (ox + w - 1 + depth, oy + y, oz + along)

def _wall_pos(module: PlacedModule, side: str, along: int, y: int) -> Vec3:
    ox, oy, oz = module.origin
    w, h, d = module.size
    if side == "north":
        return (ox + along, oy + y, oz)
    if side == "south":
        return (ox + along, oy + y, oz + d - 1)
    if side == "west":
        return (ox, oy + y, oz + along)
    return (ox + w - 1, oy + y, oz + along)

def _side_length(module: PlacedModule, side: str) -> int:
    return module.size[0] if side in ("north", "south") else module.size[2]
def _reserved_ranges(plan: ProjectPlan, module_id: str, placed: PlacedModule, side: str):
    module = plan.modules[module_id]
    ranges = []
    for port in module.ports.values():
        if port.side != side:
            continue
        world = world_port(placed.origin, port)
        along = world.pos[0] - placed.origin[0] if side in ("north", "south") else world.pos[2] - placed.origin[2]
        half = port.width // 2 + max(1, port.clearance // 2)
        ranges.append((along - half, along + half))
    return ranges

def _reserved(value: int, ranges) -> bool:
    return any(lo <= value <= hi for lo, hi in ranges)

def apply_facades(plan: ProjectPlan, placed: dict[str, PlacedModule], blocks: dict[Vec3, str]):
    profile = plan.facade_profile
    if profile.get("enabled", True) is False:
        return {"sides": 0, "windows": 0, "piers": 0}
    exposed = exterior_sides(plan)
    bay = max(4, int(profile.get("bay_spacing", 8)))
    pier_depth = max(1, int(profile.get("pier_depth", 1)))
    plinth_h = max(0, int(profile.get("plinth_height", 2)))
    win_w = max(1, int(profile.get("window_width", 3)))
    win_h = max(2, int(profile.get("window_height", 4)))
    sill = max(1, int(profile.get("window_sill_y", 3)))
    pier_state = profile.get("pier_state", "minecraft:polished_deepslate")
    plinth_state = profile.get("plinth_state", pier_state)
    trim_state = profile.get("trim_state", "minecraft:dark_oak_planks")
    glass_state = profile.get("glass_state", "minecraft:glass")
    stats = {"sides": 0, "windows": 0, "piers": 0}
    for module_id, sides in exposed.items():
        placed_module = placed[module_id]
        length = _side_length(placed_module, "north")
        for side in sides:
            stats["sides"] += 1
            length = _side_length(placed_module, side)
            reserved = _reserved_ranges(plan, module_id, placed_module, side)
            # Exterior plinth: add depth without overwriting the module interior.
            for along in range(length):
                for y in range(plinth_h):
                    blocks[_out_pos(placed_module, side, along, y, 1)] = plinth_state

            pier_positions = list(range(0, length, bay))
            if (length - 1) not in pier_positions:
                pier_positions.append(length - 1)
            for along in pier_positions:
                if _reserved(along, reserved):
                    continue
                stats["piers"] += 1
                for depth in range(1, pier_depth + 1):
                    for y in range(1, max(2, placed_module.size[1] - 1)):
                        blocks[_out_pos(placed_module, side, along, y, depth)] = pier_state

            # Windows occupy the boundary wall plane; ports keep priority.
            for left, right in zip(pier_positions, pier_positions[1:]):
                center = (left + right) // 2
                if right - left < win_w + 2 or _reserved(center, reserved):
                    continue
                start = center - win_w // 2
                max_y = min(placed_module.size[1] - 2, sill + win_h - 1)
                if max_y <= sill:
                    continue
                pointed = "gothic" in str(profile.get("id", "")).lower()
                for y in range(sill, max_y + 1):
                    row_w = 1 if pointed and y == max_y else win_w
                    row_start = center - row_w // 2
                    for along in range(row_start, row_start + row_w):
                        blocks[_wall_pos(placed_module, side, along, y)] = glass_state
                # Sill/header read as larger shapes, not micro-noise.
                for along in range(start - 1, start + win_w + 1):
                    blocks[_out_pos(placed_module, side, along, max(1, sill - 1), 1)] = trim_state
                    if max_y + 1 < placed_module.size[1]:
                        blocks[_out_pos(placed_module, side, along, max_y + 1, 1)] = trim_state
                stats["windows"] += 1

            cornice_depth = int(profile.get("cornice_depth", 1))
            if cornice_depth > 0:
                cornice_y = max(2, placed_module.size[1] - 2)
                for along in range(length):
                    for depth in range(1, cornice_depth + 1):
                        blocks[_out_pos(placed_module, side, along, cornice_y, depth)] = trim_state
    return stats
