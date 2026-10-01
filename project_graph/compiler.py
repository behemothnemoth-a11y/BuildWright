from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

from .assembler import build_straight_corridors, carve_connections, exterior_sides, merge_modules
from .facade import apply_facades
from .model import ProjectPlan, load_project
from .preview import render_project_svg
from .roof import apply_roofs
from .site import apply_site
from .foundation import apply_foundations
from .structures import apply_structures
from .vanilla_finish import apply_vanilla_finish
from .solver import project_bounds, solve_project

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))
from litematic_codec import I, make, read, unpack

def _write_lf(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8"))

def _shift_entity(entity, delta):
    dx, dy, dz = delta
    out = dict(entity)
    out["x"] = I(int(entity["x"].v) + dx)
    out["y"] = I(int(entity["y"].v) + dy)
    out["z"] = I(int(entity["z"].v) + dz)
    return out

def _normalize(blocks, block_entities):
    xs = [p[0] for p in blocks]
    ys = [p[1] for p in blocks]
    zs = [p[2] for p in blocks]
    min_pos = (min(xs), min(ys), min(zs))
    max_pos = (max(xs), max(ys), max(zs))
    delta = tuple(-v for v in min_pos)
    shifted = {(x + delta[0], y + delta[1], z + delta[2]): state for (x, y, z), state in blocks.items()}
    entities = [_shift_entity(be, delta) for be in block_entities]
    size = tuple(max_pos[i] - min_pos[i] + 1 for i in range(3))
    return shifted, entities, size, delta, min_pos, max_pos

def _validate_litematic(path: Path, expected_nonair: int, expected_tiles: int):
    root = read(path)
    regions = root["Regions"]
    if len(regions) != 1:
        raise ValueError("project output must contain exactly one region")
    region = next(iter(regions.values()))
    size = region["Size"]
    count = size["x"] * size["y"] * size["z"]
    palette = region["BlockStatePalette"]
    indices = unpack(region["BlockStates"], count, len(palette))
    nonair = sum(i != 0 for i in indices)
    tiles = len(region["TileEntities"])
    if nonair != expected_nonair or root["Metadata"]["TotalBlocks"] != expected_nonair:
        raise ValueError(f"project readback mismatch {nonair}/{root['Metadata']['TotalBlocks']} != {expected_nonair}")
    if tiles != expected_tiles:
        raise ValueError(f"project block entity mismatch {tiles} != {expected_tiles}")
    return {"regions": 1, "nonair": nonair, "volume": count, "palette": len(palette), "block_entities": tiles}

def compile_project(root: Path, brief: dict | Path, output_dir: Path | None = None):
    root = Path(root)
    if isinstance(brief, Path):
        brief_path = brief
        brief = json.loads(brief.read_text(encoding="utf-8"))
    else:
        brief_path = None
    plan = load_project(root, brief)
    placed = solve_project(plan)
    blocks, block_entities, warnings = merge_modules(plan, placed)

    carve_connections(plan, placed, blocks)
    circulation_stats = build_straight_corridors(plan, placed, blocks)
    facade_stats = apply_facades(plan, placed, blocks)
    roof_stats = apply_roofs(plan, placed, blocks)
    structure_stats = apply_structures(plan, placed, blocks, brief)
    site_stats = apply_site(plan, placed, blocks)
    foundation_stats = apply_foundations(plan, placed, blocks, brief)
    finish_stats = apply_vanilla_finish(plan, placed, blocks, brief)

    normalized, entities, size, delta, min_pos, max_pos = _normalize(blocks, block_entities)
    output_dir = Path(output_dir) if output_dir else root / "project_graph" / "compiled_examples"
    output_dir.mkdir(parents=True, exist_ok=True)

    project_id = str(brief["id"])
    lit_path = output_dir / f"{project_id}.litematic"
    source_path = output_dir / f"{project_id}.project.json"
    manifest_path = output_dir / f"{project_id}.manifest.json"
    preview_path = output_dir / f"{project_id}.plan.svg"

    module_records = []
    for module_id, placement in placed.items():
        module = plan.modules[module_id]
        module_records.append({
            "id": module_id,
            "source": str(module.source_path.relative_to(root)).replace("\\", "/"),
            "origin": list(placement.origin),
            "normalized_origin": [placement.origin[i] + delta[i] for i in range(3)],
            "size": list(placement.size),
            "rotation": module.rotation,
            "mirror": module.mirror,
            "ports": sorted(module.ports),
        })
    canonical = {
        "schema_version": 1,
        "id": project_id,
        "brief": brief,
        "modules": module_records,
        "normalization_offset": list(delta),
        "pre_normalized_bounds": [*min_pos, *max_pos],
        "exterior_sides": exterior_sides(plan),
        "circulation": circulation_stats,
        "structures": structure_stats,
        "foundations": foundation_stats,
        "vanilla_finish": finish_stats,
    }
    _write_lf(source_path, json.dumps(canonical, indent=2) + "\n")

    make(
        lit_path,
        "BuildWright " + brief.get("name", project_id),
        size,
        normalized,
        entities,
        desc=f"BuildWright whole-building compile: {project_id}",
        dataversion=int(brief.get("data_version", 4903)),
    )
    readback = _validate_litematic(lit_path, len(normalized), len(entities))
    render_project_svg(plan, placed, preview_path)

    digest = hashlib.sha256(lit_path.read_bytes()).hexdigest()
    manifest = {
        "schema_version": 1,
        "id": project_id,
        "maturity": "OFFLINE_COMPILED",
        "live_game_status": "PENDING",
        "modules": len(placed),
        "connections": len(plan.connections),
        "size": list(size),
        "blocks": len(normalized),
        "block_entities": len(entities),
        "litematic": lit_path.name,
        "project_source": source_path.name,
        "preview": preview_path.name,
        "litematic_sha256": digest,
        "readback": readback,
        "facade": facade_stats,
        "roof": roof_stats,
        "site": site_stats,
        "circulation": circulation_stats,
        "structures": structure_stats,
        "foundations": foundation_stats,
        "vanilla_finish": finish_stats,
        "detail_status": finish_stats.get("status","BASELINE"),
        "warnings": warnings + plan.warnings,
    }
    _write_lf(manifest_path, json.dumps(manifest, indent=2) + "\n")

    return {
        "plan": plan,
        "placed": placed,
        "litematic": lit_path,
        "source": source_path,
        "manifest": manifest_path,
        "preview": preview_path,
        "readback": readback,
    }
