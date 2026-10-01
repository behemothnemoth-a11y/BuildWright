from __future__ import annotations
import math

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
            a = oz - over + inset
            b = oz + d - 1 + over - inset
            if a > b:
                break
            for x in range(ox - over, ox + w + over):
                for z in {a, b}:
                    for rr in range(run):
                        zz = z + rr if z == a else z - rr
                        if a <= zz <= b:
                            _set(blocks, x, top + rise, zz, state)
        else:
            a = ox - over + inset
            b = ox + w - 1 + over - inset
            if a > b:
                break
            for z in range(oz - over, oz + d + over):
                for x in {a, b}:
                    for rr in range(run):
                        xx = x + rr if x == a else x - rr
                        if a <= xx <= b:
                            _set(blocks, xx, top + rise, z, state)

    # Close gable ends.
    if axis == "x":
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
        x0 += run
        x1 -= run
        z0 += run
        z1 -= run
        rise += 1
    return rise

def _shed(blocks, module: PlacedModule, cfg):
    ox, oy, oz = module.origin
    w, h, d = module.size
    over = int(cfg.get("overhang", 1))
    run = max(1, int(cfg.get("step_run", 3)))
    axis = str(cfg.get("slope_axis", "z")).lower()
    state = cfg.get("state", "minecraft:dark_oak_planks")
    top = oy + h
    max_rise = 0
    if axis == "x":
        for local_x in range(-over, w + over):
            rise = max(0, (local_x + over) // run)
            max_rise = max(max_rise, rise)
            for z in range(oz - over, oz + d + over):
                _set(blocks, ox + local_x, top + rise, z, state)
    else:
        for local_z in range(-over, d + over):
            rise = max(0, (local_z + over) // run)
            max_rise = max(max_rise, rise)
            for x in range(ox - over, ox + w + over):
                _set(blocks, x, top + rise, oz + local_z, state)
    return max_rise + 1

def _butterfly(blocks, module: PlacedModule, cfg):
    ox, oy, oz = module.origin
    w, h, d = module.size
    over = int(cfg.get("overhang", 1))
    run = max(1, int(cfg.get("step_run", 3)))
    axis = str(cfg.get("ridge_axis", "x")).lower()
    state = cfg.get("state", "minecraft:dark_oak_planks")
    top = oy + h
    max_rise = 0
    if axis == "x":
        center = (d - 1) / 2
        for z in range(-over, d + over):
            rise = int(abs(z - center) // run)
            max_rise = max(max_rise, rise)
            for x in range(ox - over, ox + w + over):
                _set(blocks, x, top + rise, oz + z, state)
    else:
        center = (w - 1) / 2
        for x in range(-over, w + over):
            rise = int(abs(x - center) // run)
            max_rise = max(max_rise, rise)
            for z in range(oz - over, oz + d + over):
                _set(blocks, ox + x, top + rise, z, state)
    return max_rise + 1

def _sawtooth(blocks, module: PlacedModule, cfg):
    ox, oy, oz = module.origin
    w, h, d = module.size
    state = cfg.get("state", "minecraft:polished_deepslate")
    glass = cfg.get("saw_glass_state", "minecraft:light_blue_stained_glass")
    tooth = max(4, int(cfg.get("tooth_width", 6)))
    top = oy + h
    max_rise = 0
    for z0 in range(oz, oz + d, tooth):
        z1 = min(oz + d - 1, z0 + tooth - 1)
        span = max(1, z1 - z0)
        for z in range(z0, z1 + 1):
            rise = (z - z0) // 2
            max_rise = max(max_rise, rise)
            for x in range(ox, ox + w):
                _set(blocks, x, top + rise, z, state)
        wall_z = z1
        for y in range(top, top + max(1, span // 2)):
            for x in range(ox, ox + w):
                _set(blocks, x, y, wall_z, glass)
    return max_rise + 1

def _tiered(blocks, module: PlacedModule, cfg):
    # Pagoda / tiered temple massing: stacked shallow hip roofs with strong overhang.
    ox, oy, oz = module.origin
    w, h, d = module.size
    tiers = max(2, int(cfg.get("tiers", 3)))
    state = cfg.get("state", "minecraft:dark_oak_planks")
    total_rise = 0
    current = module
    for tier in range(tiers):
        local = dict(cfg)
        local["state"] = state
        local["step_run"] = max(2, int(cfg.get("step_run", 3)))
        local["overhang"] = max(1, int(cfg.get("overhang", 3)) - tier)
        rise = _hip(blocks, current, local)
        total_rise += max(2, rise)
        shrink = 2 * (tier + 1)
        nw = max(5, w - shrink * 2)
        nd = max(5, d - shrink * 2)
        current = PlacedModule(
            module.id,
            (ox + shrink, oy + h + total_rise, oz + shrink),
            (nw, 1, nd),
        )
    return total_rise + 1

def _dome(blocks, module: PlacedModule, cfg):
    ox, oy, oz = module.origin
    w, h, d = module.size
    state = cfg.get("state", "minecraft:smooth_quartz")
    top = oy + h
    rx = max(2.0, (w - 1) / 2)
    rz = max(2.0, (d - 1) / 2)
    ry = max(2.0, min(rx, rz) * float(cfg.get("dome_height_ratio", 0.65)))
    cx = ox + (w - 1) / 2
    cz = oz + (d - 1) / 2
    max_y = int(math.ceil(ry))
    for y in range(0, max_y + 1):
        level = max(0.0, 1.0 - (y / ry) ** 2)
        sx = rx * math.sqrt(level)
        sz = rz * math.sqrt(level)
        if sx < 0.5 or sz < 0.5:
            _set(blocks, round(cx), top + y, round(cz), state)
            continue
        steps = max(16, int((sx + sz) * 5))
        for i in range(steps):
            a = (math.tau * i) / steps
            _set(blocks, round(cx + math.cos(a) * sx), top + y, round(cz + math.sin(a) * sz), state)
    return max_y + 1

def _vault(blocks, module: PlacedModule, cfg):
    ox, oy, oz = module.origin
    w, h, d = module.size
    axis = str(cfg.get("ridge_axis", "x")).lower()
    state = cfg.get("state", "minecraft:deepslate_bricks")
    top = oy + h
    if axis == "x":
        radius = max(2, d // 2)
        center = oz + (d - 1) / 2
        for z in range(oz, oz + d):
            dz = (z - center) / radius
            rise = int(round(math.sqrt(max(0.0, 1.0 - dz * dz)) * radius))
            for x in range(ox, ox + w):
                _set(blocks, x, top + rise, z, state)
    else:
        radius = max(2, w // 2)
        center = ox + (w - 1) / 2
        for x in range(ox, ox + w):
            dx = (x - center) / radius
            rise = int(round(math.sqrt(max(0.0, 1.0 - dx * dx)) * radius))
            for z in range(oz, oz + d):
                _set(blocks, x, top + rise, z, state)
    return radius + 1

def _terraced(blocks, module: PlacedModule, cfg):
    ox, oy, oz = module.origin
    w, h, d = module.size
    state = cfg.get("state", "minecraft:stone_bricks")
    levels = max(2, int(cfg.get("terrace_levels", 3)))
    top = oy + h
    for level in range(levels):
        inset = level * max(1, int(cfg.get("terrace_inset", 2)))
        if inset * 2 >= min(w, d):
            break
        for z in range(oz + inset, oz + d - inset):
            for x in range(ox + inset, ox + w - inset):
                _set(blocks, x, top + level, z, state)
    return levels

def _ruined(blocks, module: PlacedModule, cfg):
    # Deterministic partial roof, useful for ruin language without random output.
    temp = {}
    rise = _gable(temp, module, cfg)
    for (x, y, z), state in temp.items():
        if (x * 31 + y * 17 + z * 13) % 11 not in {0, 1, 2}:
            blocks[(x, y, z)] = state
    return rise

def apply_roofs(plan: ProjectPlan, placed: dict[str, PlacedModule], blocks: dict[Vec3, str]):
    global_cfg = dict(plan.roof)
    if global_cfg.get("enabled", True) is False:
        return {"modules": 0, "max_rise": 0, "styles": {}}

    overrides = global_cfg.pop("module_overrides", {})
    stats = {"modules": 0, "max_rise": 0, "styles": {}}
    for module_id, module in placed.items():
        cfg = dict(global_cfg)
        cfg.update(overrides.get(module_id, {}))
        style = str(cfg.get("style", "gable")).lower()
        if style == "none":
            continue

        # Semantic aliases let style profiles describe architecture instead of implementation.
        if style in {"steep_gable", "swept_gable"}:
            cfg["step_run"] = min(int(cfg.get("step_run", 2)), 1)
            rise = _gable(blocks, module, cfg)
        elif style == "low_gable":
            cfg["step_run"] = max(int(cfg.get("step_run", 2)), 3)
            rise = _gable(blocks, module, cfg)
        elif style in {"flat", "mechanical_flat", "false_front"}:
            rise = _flat(blocks, module, cfg)
        elif style == "hip":
            rise = _hip(blocks, module, cfg)
        elif style == "mansard":
            lower = dict(cfg)
            lower["step_run"] = max(1, int(cfg.get("step_run", 1)))
            rise = _hip(blocks, module, lower)
            cap = PlacedModule(module.id, (module.origin[0], module.origin[1] + rise, module.origin[2]), module.size)
            cap_cfg = dict(cfg)
            cap_cfg["overhang"] = 0
            rise += _flat(blocks, cap, cap_cfg)
        elif style == "shed":
            rise = _shed(blocks, module, cfg)
        elif style == "butterfly":
            rise = _butterfly(blocks, module, cfg)
        elif style == "sawtooth":
            rise = _sawtooth(blocks, module, cfg)
        elif style in {"pagoda", "tiered"}:
            rise = _tiered(blocks, module, cfg)
        elif style in {"dome", "dome_flat"}:
            rise = _dome(blocks, module, cfg)
        elif style == "vaulted_mass":
            rise = _vault(blocks, module, cfg)
        elif style in {"terraced", "green_terrace"}:
            rise = _terraced(blocks, module, cfg)
        elif style == "ruined":
            rise = _ruined(blocks, module, cfg)
        else:
            rise = _gable(blocks, module, cfg)

        stats["modules"] += 1
        stats["max_rise"] = max(stats["max_rise"], rise)
        stats["styles"][style] = stats["styles"].get(style, 0) + 1
    return stats
