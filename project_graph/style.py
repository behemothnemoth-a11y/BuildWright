from __future__ import annotations
import json
from pathlib import Path
from typing import Any

NUMERIC_KEYS = {
    "bay_spacing", "pier_depth", "plinth_height", "window_width", "window_height",
    "window_sill_y", "cornice_depth", "depth_bias", "vertical_emphasis",
    "ornament_density", "roof_step_run", "roof_overhang",
}

def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def load_profile(root: Path, profile_id: str) -> dict[str, Any]:
    path = Path(root) / "project_graph" / "profiles" / f"{profile_id}.json"
    if not path.is_file():
        raise FileNotFoundError(f"Unknown BuildWright style profile: {profile_id}")
    return _load(path)

def _blend_numeric(a, b, weight: float):
    if isinstance(a, bool) or isinstance(b, bool):
        return a
    value = float(a) * (1.0 - weight) + float(b) * weight
    if isinstance(a, int) and isinstance(b, int):
        return int(round(value))
    return round(value, 4)

def blend_profiles(primary: dict[str, Any], secondary: dict[str, Any], weight: float) -> dict[str, Any]:
    weight = max(0.0, min(1.0, float(weight)))
    out = dict(primary)
    for key in NUMERIC_KEYS:
        if key in primary and key in secondary:
            out[key] = _blend_numeric(primary[key], secondary[key], weight)

    # Massing is numeric enough to blend safely; categorical style language remains primary.
    massing = dict(primary.get("massing", {}))
    for key, value in secondary.get("massing", {}).items():
        if key in massing and isinstance(massing[key], (int, float)) and isinstance(value, (int, float)):
            massing[key] = round(float(massing[key]) * (1.0 - weight) + float(value) * weight, 4)
    out["massing"] = massing

    out["style_influences"] = [
        {"id": primary["id"], "weight": round(1.0 - weight, 4)},
        {"id": secondary["id"], "weight": round(weight, 4)},
    ]
    out["id"] = f"{primary['id']}+{secondary['id']}"
    out["display_name"] = f"{primary.get('display_name', primary['id'])} + {secondary.get('display_name', secondary['id'])}"
    return out

def resolve_style(root: Path, brief: dict[str, Any]) -> dict[str, Any]:
    style = brief.get("style")
    if not style:
        profile_id = str(brief.get("facade_profile", "massive_gothic_manor"))
        resolved = load_profile(root, profile_id)
    else:
        primary_id = str(style.get("primary", brief.get("facade_profile", "modern")))
        resolved = load_profile(root, primary_id)
        secondary_id = style.get("secondary")
        if secondary_id:
            resolved = blend_profiles(resolved, load_profile(root, str(secondary_id)), float(style.get("blend", 0.25)))
        # Explicit material-role overrides are safer than trying to interpolate block IDs.
        roles = dict(resolved.get("material_roles", {}))
        roles.update(style.get("material_roles", {}))
        resolved["material_roles"] = roles
        for role, state in roles.items():
            key = {
                "wall": "wall_state", "structure": "pier_state", "trim": "trim_state",
                "accent": "accent_state", "glass": "glass_state", "plinth": "plinth_state",
                "roof": "roof_state",
            }.get(role)
            if key:
                resolved[key] = state
        resolved.update(style.get("overrides", {}))

    resolved.update(brief.get("facade", {}))
    return resolved
