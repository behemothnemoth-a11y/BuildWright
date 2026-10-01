#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "project_graph" / "style_registry.json"
PROFILES = ROOT / "project_graph" / "profiles"

REQUIRED_ROLES = {"wall","structure","trim","accent","glass","plinth","roof"}
ROOF_STYLES = {
    "flat","mechanical_flat","green_terrace","false_front","gable","steep_gable",
    "swept_gable","low_gable","hip","mansard","shed","butterfly","sawtooth",
    "pagoda","tiered","dome","dome_flat","vaulted_mass","terraced","ruined"
}

def main():
    reg=json.loads(REG.read_text(encoding="utf-8"))
    errors=[]
    ids=set()
    families=set()
    for item in reg["profiles"]:
        pid=item["id"]
        if pid in ids: errors.append(f"duplicate style id: {pid}")
        ids.add(pid); families.add(item["family"])
        path=PROFILES/f"{pid}.json"
        if not path.is_file():
            errors.append(f"missing profile file: {pid}")
            continue
        p=json.loads(path.read_text(encoding="utf-8"))
        if p.get("id")!=pid: errors.append(f"{pid}: id mismatch")
        if p.get("family")!=item["family"]: errors.append(f"{pid}: family mismatch")
        if set(p.get("material_roles",{})) < REQUIRED_ROLES: errors.append(f"{pid}: incomplete material roles")
        if p.get("default_roof") not in ROOF_STYLES: errors.append(f"{pid}: unsupported roof {p.get('default_roof')}")
        if not p.get("window_shape"): errors.append(f"{pid}: missing window shape")
        if not p.get("facade_rhythm"): errors.append(f"{pid}: missing facade rhythm")
        if not p.get("zone_presets"): errors.append(f"{pid}: missing zone presets")
        m=p.get("massing",{})
        for k in ("tower_bias","courtyard_bias","setback_bias","verticality"):
            if not 0 <= float(m.get(k,-1)) <= 1: errors.append(f"{pid}: invalid massing {k}")
    if reg.get("count")!=len(ids): errors.append("registry count mismatch")
    if len(families)<12: errors.append("style family coverage below 12")
    if len(ids)<30: errors.append("style profile coverage below 30")
    if errors:
        print("STYLE SYSTEM VALIDATION: FAIL")
        for e in errors: print(" -",e)
        sys.exit(1)
    print("STYLE SYSTEM VALIDATION: PASS",{"profiles":len(ids),"families":len(families)})

if __name__=="__main__":
    main()
