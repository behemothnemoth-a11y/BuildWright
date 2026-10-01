from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

from .model import CARDINAL, VERTICAL, Connection, ModuleSpec, ProjectPlan, Port, port_for

Vec3 = tuple[int, int, int]
OUT = {"north": (0, 0, -1), "south": (0, 0, 1), "west": (-1, 0, 0), "east": (1, 0, 0), "up": (0, 1, 0), "down": (0, -1, 0)}
OPPOSITE = {"north": "south", "south": "north", "west": "east", "east": "west", "up": "down", "down": "up"}

@dataclass(frozen=True)
class PlacedModule:
    id: str
    origin: Vec3
    size: Vec3

    @property
    def box(self):
        x, y, z = self.origin
        w, h, d = self.size
        return (x, y, z, x + w - 1, y + h - 1, z + d - 1)

def add(a: Vec3, b: Vec3) -> Vec3:
    return tuple(a[i] + b[i] for i in range(3))

def sub(a: Vec3, b: Vec3) -> Vec3:
    return tuple(a[i] - b[i] for i in range(3))

def mul(a: Vec3, n: int) -> Vec3:
    return tuple(v * n for v in a)
def world_port(origin: Vec3, port: Port) -> Port:
    return port.translated(origin)

def _validate_pair(a: Port, b: Port):
    if OPPOSITE.get(a.side) != b.side:
        raise ValueError(f"Ports must face each other: {a.side} -> {b.side}")
    if a.side in CARDINAL and b.side not in CARDINAL:
        raise ValueError("Cannot connect cardinal port to vertical port")
    if a.side in VERTICAL and b.side not in VERTICAL:
        raise ValueError("Cannot connect vertical port to cardinal port")

def target_origin(source_origin: Vec3, source_port: Port, target_port: Port, mode: str, gap: int) -> Vec3:
    _validate_pair(source_port, target_port)
    source_world = world_port(source_origin, source_port).pos
    separation = 0 if mode == "attach" else max(0, gap) + 1
    desired = add(source_world, mul(OUT[source_port.side], separation))
    return sub(desired, target_port.pos)

def _box_intersection(a, b):
    x0, y0, z0, x1, y1, z1 = a
    a0, b0, c0, a1, b1, c1 = b
    if x1 < a0 or a1 < x0 or y1 < b0 or b1 < y0 or z1 < c0 or c1 < z0:
        return None
    return (max(x0, a0), max(y0, b0), max(z0, c0), min(x1, a1), min(y1, b1), min(z1, c1))

def _thin_shared_plane(intersection) -> bool:
    if intersection is None:
        return True
    x0, y0, z0, x1, y1, z1 = intersection
    return sum((x1 - x0) == 0 for _ in [0]) + sum((y1 - y0) == 0 for _ in [0]) + sum((z1 - z0) == 0 for _ in [0]) >= 1
def solve_project(plan: ProjectPlan) -> dict[str, PlacedModule]:
    modules = plan.modules
    placed: dict[str, PlacedModule] = {}
    for module in modules.values():
        if module.origin is not None:
            placed[module.id] = PlacedModule(module.id, module.origin, module.size)
    if not placed:
        first = next(iter(modules.values()))
        placed[first.id] = PlacedModule(first.id, (0, 0, 0), first.size)

    unresolved = list(plan.connections)
    progress = True
    while unresolved and progress:
        progress = False
        for connection in list(unresolved):
            a_done = connection.a_module in placed
            b_done = connection.b_module in placed
            if a_done == b_done:
                continue
            if a_done:
                source_id, source_port_id = connection.a_module, connection.a_port
                target_id, target_port_id = connection.b_module, connection.b_port
                reverse = False
            else:
                source_id, source_port_id = connection.b_module, connection.b_port
                target_id, target_port_id = connection.a_module, connection.a_port
                reverse = True
            source = modules[source_id]
            target = modules[target_id]
            source_port = port_for(source, source_port_id)
            target_port = port_for(target, target_port_id)
            mode = connection.mode
            origin = target_origin(placed[source_id].origin, source_port, target_port, mode, connection.gap)
            placed[target_id] = PlacedModule(target_id, origin, target.size)
            unresolved.remove(connection)
            progress = True

    if unresolved:
        names = [f"{c.a_module}:{c.a_port}->{c.b_module}:{c.b_port}" for c in unresolved]
        raise ValueError(f"Unresolved project graph connections: {names}")

    # Reject volumetric collisions. One-block shared planes are allowed for attached rooms.
    attached_pairs = {frozenset((c.a_module, c.b_module)) for c in plan.connections if c.mode == "attach"}
    items = list(placed.values())
    for i, a in enumerate(items):
        for b in items[i + 1:]:
            inter = _box_intersection(a.box, b.box)
            if inter is None:
                continue
            pair = frozenset((a.id, b.id))
            if pair in attached_pairs and _thin_shared_plane(inter):
                continue
            raise ValueError(f"Module collision: {a.id} {a.box} vs {b.id} {b.box} at {inter}")
    return placed

def project_bounds(placed: Iterable[PlacedModule]):
    placed = list(placed)
    return (
        min(p.box[0] for p in placed), min(p.box[1] for p in placed), min(p.box[2] for p in placed),
        max(p.box[3] for p in placed), max(p.box[4] for p in placed), max(p.box[5] for p in placed),
    )
