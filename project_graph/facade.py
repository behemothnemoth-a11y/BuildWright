from __future__ import annotations

from .assembler import exterior_sides
from .model import ProjectPlan
from .solver import PlacedModule, world_port

Vec3 = tuple[int, int, int]

ARCHED = {"arched", "pointed", "lancet", "deep_arch", "horseshoe_arch", "organic_arch"}
GRIDDED = {"mullioned", "factory_grid", "shoji_grid", "lattice", "screen", "curtain_wall"}
WIDE = {"ribbon", "curtain_wall", "storefront", "factory_grid", "balcony_group"}
NARROW = {"slot", "lancet", "vertical_band"}

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

def _row_width(shape: str, row: int, total: int, width: int) -> int:
    if total <= 1:
        return width
    from_top = total - 1 - row
    if shape in {"pointed", "lancet", "deep_arch"}:
        if from_top == 0:
            return 1
        if from_top == 1:
            return max(1, width - 2)
    if shape in {"arched", "organic_arch"}:
        if from_top == 0:
            return max(1, width - 2)
    if shape == "horseshoe_arch":
        if from_top == 0:
            return max(1, width - 2)
        if row == 0:
            return max(1, width - 2)
    if shape == "broken":
        return max(1, width - (1 if row % 3 == 0 else 0))
    return width

def _bay_spacing(profile: dict, bay_index: int) -> int:
    base = max(4, int(profile.get("bay_spacing", 8)))
    rhythm = str(profile.get("facade_rhythm", "regular"))
    if rhythm in {"irregular", "organic", "fragmented", "flowing", "free"}:
        delta = (-1, 1, 0, 2, -1)[bay_index % 5]
        return max(4, base + delta)
    if rhythm == "stepped":
        return max(4, base + (2 if bay_index % 3 == 1 else 0))
    return base

def _pier_positions(length: int, profile: dict) -> list[int]:
    positions = [0]
    cursor = 0
    bay_index = 0
    while cursor < length - 1:
        cursor += _bay_spacing(profile, bay_index)
        bay_index += 1
        if cursor < length - 1:
            positions.append(cursor)
    if positions[-1] != length - 1:
        positions.append(length - 1)
    return positions

def _apply_band(blocks, module, side, length, y, depth, state, reserved):
    if y <= 0 or y >= module.size[1]:
        return 0
    count = 0
    for along in range(length):
        if _reserved(along, reserved):
            continue
        for dd in range(1, depth + 1):
            blocks[_out_pos(module, side, along, y, dd)] = state
            count += 1
    return count

def _apply_window(blocks, module, side, center, sill, width, height, shape, glass_state, trim_state):
    top = min(module.size[1] - 2, sill + height - 1)
    if top <= sill:
        return 0
    total = top - sill + 1
    placed = 0
    for row, y in enumerate(range(sill, top + 1)):
        row_width = _row_width(shape, row, total, width)
        start = center - row_width // 2
        for along in range(start, start + row_width):
            if shape == "broken" and (along + y) % 7 == 0:
                continue
            blocks[_wall_pos(module, side, along, y)] = glass_state
            placed += 1

    # Shape-preserving external frame.
    frame_start = center - width // 2 - 1
    frame_end = frame_start + width + 1
    for along in range(frame_start, frame_end + 1):
        blocks[_out_pos(module, side, along, max(1, sill - 1), 1)] = trim_state
        if top + 1 < module.size[1]:
            blocks[_out_pos(module, side, along, top + 1, 1)] = trim_state

    # Gridded families get mullions/transoms as external trim so glass remains visible.
    if shape in GRIDDED:
        centers = [center]
        if width >= 6:
            centers = [center - width // 3, center + width // 3]
        for along in centers:
            for y in range(sill, top + 1):
                blocks[_out_pos(module, side, along, y, 1)] = trim_state
        if height >= 4:
            transom_y = sill + height // 2
            for along in range(center - width // 2, center - width // 2 + width):
                blocks[_out_pos(module, side, along, transom_y, 1)] = trim_state
    return placed

def _apply_balcony(blocks, module, side, center, sill, width, trim_state):
    depth = 2
    y = max(1, sill - 1)
    count = 0
    for dd in range(1, depth + 1):
        for along in range(center - width // 2 - 1, center + width // 2 + 2):
            blocks[_out_pos(module, side, along, y, dd)] = trim_state
            count += 1
    return count

def apply_facades(plan: ProjectPlan, placed: dict[str, PlacedModule], blocks: dict[Vec3, str]):
    profile = plan.facade_profile
    if profile.get("enabled", True) is False:
        return {"sides": 0, "windows": 0, "piers": 0, "bands": 0, "balconies": 0}

    exposed = exterior_sides(plan)
    pier_depth = max(1, int(profile.get("pier_depth", 1)) + max(0, int(profile.get("depth_bias", 1)) - 1))
    plinth_h = max(0, int(profile.get("plinth_height", 2)))
    win_w = max(1, int(profile.get("window_width", 3)))
    win_h = max(2, int(profile.get("window_height", 4)))
    sill = max(1, int(profile.get("window_sill_y", 3)))
    window_shape = str(profile.get("window_shape", "rect"))
    if window_shape in WIDE:
        win_w = max(win_w, 5)
    if window_shape in NARROW:
        win_w = min(win_w, 3)

    pier_state = profile.get("pier_state", "minecraft:polished_deepslate")
    plinth_state = profile.get("plinth_state", pier_state)
    trim_state = profile.get("trim_state", "minecraft:dark_oak_planks")
    accent_state = profile.get("accent_state", trim_state)
    glass_state = profile.get("glass_state", "minecraft:glass")
    ornament = float(profile.get("ornament_density", 0.4))
    vertical = float(profile.get("vertical_emphasis", 0.5))

    stats = {"sides": 0, "windows": 0, "piers": 0, "bands": 0, "balconies": 0}
    for module_id, sides in exposed.items():
        module = placed[module_id]
        side_overrides = profile.get("side_overrides", {})
        for side in sides:
            local = dict(profile)
            local.update(side_overrides.get(side, {}))
            zone_assignments = profile.get("zone_assignments", {})
            zone_name = zone_assignments.get(f"{module_id}:{side}", zone_assignments.get(side, "primary"))
            zone = dict(profile.get("zone_presets", {}).get(zone_name, {}))
            local_ornament = max(0.0, ornament * float(zone.get("ornament_multiplier", 1.0)))
            local_pier_depth = max(1, pier_depth + int(zone.get("depth_add", 0)))
            window_scale = max(0.0, float(zone.get("window_scale", 1.0)))
            local_win_w = max(1, int(round(win_w * window_scale))) if window_scale > 0 else 0
            local_win_h = max(2, int(round(win_h * window_scale))) if window_scale > 0 else 0
            local_shape = str(local.get("window_shape", window_shape))
            local_pier_state = local.get("pier_state", pier_state)
            local_plinth_state = local.get("plinth_state", plinth_state)
            local_trim_state = local.get("trim_state", trim_state)
            local_accent_state = local.get("accent_state", accent_state)
            local_glass_state = local.get("glass_state", glass_state)
            stats["sides"] += 1
            length = _side_length(module, side)
            reserved = _reserved_ranges(plan, module_id, module, side)

            # Base zone.
            for along in range(length):
                for y in range(plinth_h):
                    blocks[_out_pos(module, side, along, y, 1)] = local_plinth_state

            pier_positions = _pier_positions(length, local)
            for index, along in enumerate(pier_positions):
                if _reserved(along, reserved):
                    continue
                stats["piers"] += 1
                depth = local_pier_depth
                rhythm = str(local.get("facade_rhythm", "regular"))
                if rhythm in {"monumental", "processional"} and index % 2 == 0:
                    depth += 1
                for dd in range(1, depth + 1):
                    for y in range(1, max(2, module.size[1] - 1)):
                        blocks[_out_pos(module, side, along, y, dd)] = local_pier_state

                # Vertical emphasis can add an accent spine without covering every pier.
                if vertical >= 0.75 and index % 2 == 0:
                    for y in range(max(2, plinth_h), max(2, module.size[1] - 2)):
                        blocks[_out_pos(module, side, along, y, depth + 1)] = local_accent_state

            # Body zone windows.
            for bay_index, (left, right) in enumerate(zip(pier_positions, pier_positions[1:])):
                center = (left + right) // 2
                if local_win_w <= 0 or right - left < local_win_w + 2 or _reserved(center, reserved):
                    continue
                placed_cells = _apply_window(
                    blocks, module, side, center, sill, local_win_w, local_win_h,
                    local_shape, local_glass_state, local_trim_state
                )
                if placed_cells:
                    stats["windows"] += 1
                if local_shape == "balcony_group" or (
                    local_ornament >= 0.75 and bay_index % 3 == 1 and str(local.get("family", "")) in {"classical", "historic_european"}
                ):
                    stats["balconies"] += _apply_balcony(blocks, module, side, center, sill, local_win_w, local_trim_state)

            # Base/body/crown bands give styles horizontal hierarchy without surface noise.
            if local_ornament >= 0.28:
                y = max(plinth_h + 1, min(module.size[1] - 3, module.size[1] // 3))
                stats["bands"] += _apply_band(blocks, module, side, length, y, 1, local_trim_state, reserved)
            if local_ornament >= 0.62:
                y = max(plinth_h + 2, min(module.size[1] - 3, (module.size[1] * 2) // 3))
                stats["bands"] += _apply_band(blocks, module, side, length, y, 1, local_accent_state, reserved)

            cornice_depth = int(local.get("cornice_depth", 1))
            if cornice_depth > 0:
                cornice_y = max(2, module.size[1] - 2)
                stats["bands"] += _apply_band(blocks, module, side, length, cornice_y, cornice_depth, local_trim_state, reserved)

    return stats
