from __future__ import annotations
from .model import ProjectPlan
from .solver import PlacedModule

Vec3 = tuple[int, int, int]

def _set(blocks, x, y, z, state):
    blocks[(int(x), int(y), int(z))] = state

def _flat(blocks, module: PlacedModule, cfg):
    ox, oy, oz = module.origin
    w, h, d = module.size
    y = oy + h
    over = int(cfg.get("overhang", 1))
    state = cfg.get("state", "minecraft:dark_oak_planks")
    for z in range(oz - over, oz + d + over):
        for x in range(ox - over, ox + w + over):
            _set(blocks, x, y, z, state)
    return 1

def _gable(blocks, module: PlacedModule, cfg):
    ox, oy, oz = module.origin
    w, h, d = module.size
    over = int(cfg.get("overhang", 1))
    run = max(1, int(cfg.get("step_run", 2)))
    axis = str(cfg.get("ridge_axis", "x")).lower()
    state = cfg.get("state", "minecraft:dark_oak_planks")
    wall = cfg.get("gable_state", "minecraft:tuff_bricks")
    top = oy + h
    span = d + 2 * over if axis == "x" else w + 2 * over
    rises = (span + (2 * run) - 1) // (2 * run)
    for rise in range(rises + 1):
        inset = rise * run
        if axis == "x":
            z1 = oz - over + inset
            z2 = oz + d - 1 + over - inset
            if z1 > z2:
                break
            for x in range(ox - over, ox + w + over):
                for z in {z1, z2}:
                    for rr in range(run):
                        zz = z + rr if z == z1 else z - rr
                        if z1 <= zz <= z2:
                            _set(blocks, x, top + rise, zz, state)
        else:
            x1 = ox - over + inset
            x2 = ox + w - 1 + over - inset
            if x1 > x2:
                break
            for z in range(oz - over, oz + d + over):
                for x in {x1, x2}:
                    for rr in range(run):
                        xx = x + rr if x == x1 else x - rr
                        if x1 <= xx <= x2:
                            _set(blocks, xx, top + rise, z, state)
    # Close gable ends so the roof reads as a real volume from outside.
    if axis == "x":
        center = (d - 1) / 2
        for x in (ox, ox + w - 1):
            for local_z in range(d):
                rise = int(min(local_z, d - 1 - local_z) // run)
                for y in range(top, top + rise + 1):
                    _set(blocks, x, y, oz + local_z, wall)
    else:
        for z in (oz, oz + d - 1):
            for local_x in range(w):
                rise = int(min(local_x, w - 1 - local_x) // run)
                for y in range(top, top + rise + 1):
                    _set(blocks, ox + local_x, y, z, wall)
    return rises + 1

def _hip(blocks, module: PlacedModule, cfg):
    ox, oy, oz = module.origin
    w, h, d = module.size
    over = int(cfg.get("overhang", 1))
    run = max(1, int(cfg.get("step_run", 2)))
    state = cfg.get("state", "minecraft:dark_oak_planks")
    top = oy + h
    x0, x1 = ox - over, ox + w - 1 + over
    z0, z1 = oz - over, oz + d - 1 + over
    rise = 0
    while x0 <= x1 and z0 <= z1:
        for x in range(x0, x1 + 1):
            _set(blocks, x, top + rise, z0, state)
            _set(blocks, x, top + rise, z1, state)
        for z in range(z0, z1 + 1):
            _set(blocks, x0, top + rise, z, state)
            _set(blocks, x1, top + rise, z, state)
        x0 += run; x1 -= run; z0 += run; z1 -= run; rise += 1
    return rise
def apply_roofs(plan: ProjectPlan, placed: dict[str, PlacedModule], blocks: dict[Vec3, str]):
    global_cfg = dict(plan.roof)
    if global_cfg.get("enabled", True) is False:
        return {"modules": 0, "max_rise": 0}
    overrides = global_cfg.pop("module_overrides", {})
    stats = {"modules": 0, "max_rise": 0}
    for module_id, module in placed.items():
        cfg = dict(global_cfg)
        cfg.update(overrides.get(module_id, {}))
        style = str(cfg.get("style", "gable")).lower()
        if style == "none":
            continue
        if style == "flat":
            rise = _flat(blocks, module, cfg)
        elif style == "hip":
            rise = _hip(blocks, module, cfg)
        elif style == "mansard":
            lower = dict(cfg); lower["step_run"] = max(1, int(cfg.get("step_run", 1)))
            rise = _hip(blocks, module, lower)
            # cap the steep lower roof with a quiet flat crown
            cap_cfg = dict(cfg); cap_cfg["overhang"] = -max(0, rise - 1)
            rise += _flat(blocks, PlacedModule(module.id, (module.origin[0], module.origin[1] + rise, module.origin[2]), module.size), cap_cfg)
        else:
            rise = _gable(blocks, module, cfg)
        stats["modules"] += 1
        stats["max_rise"] = max(stats["max_rise"], rise)
    return stats
