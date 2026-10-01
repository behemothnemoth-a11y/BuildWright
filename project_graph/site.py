from __future__ import annotations

from .model import ProjectPlan
from .solver import PlacedModule, project_bounds

Vec3 = tuple[int, int, int]

CHARACTER_DEFAULTS = {
    "formal": ("minecraft:grass_block", "minecraft:stone_bricks"),
    "courtyard": ("minecraft:smooth_sandstone", "minecraft:cut_sandstone"),
    "garden": ("minecraft:moss_block", "minecraft:gravel"),
    "integrated_landscape": ("minecraft:grass_block", "minecraft:smooth_stone"),
    "lush_integrated": ("minecraft:moss_block", "minecraft:stone_bricks"),
    "forest": ("minecraft:podzol", "minecraft:gravel"),
    "cold_temperate": ("minecraft:grass_block", "minecraft:stone"),
    "mountain": ("minecraft:stone", "minecraft:gravel"),
    "farm": ("minecraft:grass_block", "minecraft:dirt_path"),
    "dusty_street": ("minecraft:coarse_dirt", "minecraft:gravel"),
    "desert": ("minecraft:sand", "minecraft:sandstone"),
    "dense_urban": ("minecraft:gray_concrete", "minecraft:smooth_stone"),
    "hardscape": ("minecraft:stone", "minecraft:polished_andesite"),
    "service_yard": ("minecraft:stone", "minecraft:gray_concrete"),
    "platform": ("minecraft:smooth_stone", "minecraft:iron_block"),
    "temple_garden": ("minecraft:grass_block", "minecraft:stone_bricks"),
    "monumental": ("minecraft:stone", "minecraft:polished_andesite"),
    "overgrown": ("minecraft:moss_block", "minecraft:mossy_cobblestone"),
    "submerged": ("minecraft:prismarine", "minecraft:dark_prismarine"),
    "minimal": ("minecraft:grass_block", "minecraft:smooth_quartz"),
    "generic": ("minecraft:grass_block", "minecraft:gravel"),
}

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

def _edge_feature_state(character: str):
    if character in {"formal", "garden", "lush_integrated", "temple_garden"}:
        return "minecraft:oak_leaves"
    if character in {"courtyard", "monumental"}:
        return "minecraft:stone_bricks"
    if character in {"dense_urban", "hardscape", "service_yard", "platform"}:
        return "minecraft:polished_andesite"
    if character in {"desert", "dusty_street"}:
        return "minecraft:sandstone"
    if character in {"submerged"}:
        return "minecraft:dark_prismarine"
    return None

def apply_site(plan: ProjectPlan, placed: dict[str, PlacedModule], blocks: dict[Vec3, str]):
    cfg = plan.site
    if not cfg.get("enabled", False):
        return {"ground_blocks": 0, "path_blocks": 0, "edge_blocks": 0, "character": cfg.get("character", "generic")}

    x0, y0, z0, x1, y1, z1 = project_bounds(placed.values())
    margin = max(0, int(cfg.get("margin", 8)))
    ground_y = int(cfg.get("ground_y", y0 - 1))
    character = str(cfg.get("character", "generic"))
    default_ground, default_path = CHARACTER_DEFAULTS.get(character, CHARACTER_DEFAULTS["generic"])
    ground_state = cfg.get("ground_state", default_ground)
    path_state = cfg.get("path_state", default_path)

    ground_count = 0
    for z in range(z0 - margin, z1 + margin + 1):
        for x in range(x0 - margin, x1 + margin + 1):
            pos = (x, ground_y, z)
            if pos not in blocks:
                blocks[pos] = ground_state
                ground_count += 1

    path_count = 0
    for route in cfg.get("paths", []):
        start = tuple(int(v) for v in route["from"])
        end = tuple(int(v) for v in route["to"])
        width = max(1, int(route.get("width", 3)))
        half = width // 2
        for x, z in _line_points(start, end):
            # Widen perpendicular to the path in a deterministic, simple way.
            for dx in range(-half, -half + width):
                pos = (x + dx, ground_y, z)
                blocks[pos] = path_state
                path_count += 1

    # Optional edge language is intentionally sparse: a border/hedge/retaining cue, not landscaping spam.
    edge_count = 0
    if cfg.get("edge_feature", True):
        edge_state = cfg.get("edge_state", _edge_feature_state(character))
        if edge_state and margin >= 3:
            ex0, ex1 = x0 - margin + 2, x1 + margin - 2
            ez0, ez1 = z0 - margin + 2, z1 + margin - 2
            spacing = max(2, int(cfg.get("edge_spacing", 3)))
            for x in range(ex0, ex1 + 1, spacing):
                for z in (ez0, ez1):
                    blocks[(x, ground_y + 1, z)] = edge_state
                    edge_count += 1
            for z in range(ez0, ez1 + 1, spacing):
                for x in (ex0, ex1):
                    blocks[(x, ground_y + 1, z)] = edge_state
                    edge_count += 1

    return {
        "ground_blocks": ground_count,
        "path_blocks": path_count,
        "edge_blocks": edge_count,
        "character": character,
        "vegetation_profile": cfg.get("vegetation_profile", "temperate"),
    }
