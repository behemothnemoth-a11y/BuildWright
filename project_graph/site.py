from __future__ import annotations
from .model import ProjectPlan
from .solver import PlacedModule, project_bounds

Vec3 = tuple[int, int, int]

def _line_points(a, b):
    x, z = a
    tx, tz = b
    while x != tx:
        yield x, z
        x += 1 if tx > x else -1
    while z != tz:
        yield x, z
        z += 1 if tz > z else -1
    yield x, z

def apply_site(plan: ProjectPlan, placed: dict[str, PlacedModule], blocks: dict[Vec3, str]):
    cfg = plan.site
    if not cfg.get("enabled", False):
        return {"ground_blocks": 0, "path_blocks": 0}
    x0, y0, z0, x1, y1, z1 = project_bounds(placed.values())
    margin = max(0, int(cfg.get("margin", 8)))
    ground_y = int(cfg.get("ground_y", y0 - 1))
    ground_state = cfg.get("ground_state", "minecraft:grass_block")
    count = 0
    for z in range(z0 - margin, z1 + margin + 1):
        for x in range(x0 - margin, x1 + margin + 1):
            pos = (x, ground_y, z)
            if pos not in blocks:
                blocks[pos] = ground_state
                count += 1

    path_state = cfg.get("path_state", "minecraft:gravel")
    path_count = 0
    for route in cfg.get("paths", []):
        start = tuple(int(v) for v in route["from"])
        end = tuple(int(v) for v in route["to"])
        width = max(1, int(route.get("width", 3)))
        half = width // 2
        for x, z in _line_points(start, end):
            for dx in range(-half, -half + width):
                pos = (x + dx, ground_y, z)
                blocks[pos] = path_state
                path_count += 1
    return {"ground_blocks": count, "path_blocks": path_count}
