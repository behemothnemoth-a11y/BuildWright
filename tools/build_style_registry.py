#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROFILES=ROOT/"project_graph/profiles"
REGISTRY=ROOT/"project_graph/style_registry.json"
INDEX=ROOT/"project_graph/index.json"

def build():
    items=[]
    for path in sorted(PROFILES.glob("*.json")):
        d=json.loads(path.read_text(encoding="utf-8"))
        items.append({
            "id":d["id"],
            "family":d["family"],
            "display_name":d.get("display_name",d["id"]),
            "default_roof":d["default_roof"],
            "window_shape":d["window_shape"],
        })
    return {
        "schema_version":1,
        "count":len(items),
        "families":sorted({x["family"] for x in items}),
        "profiles":items,
    }

def encode(data):
    return (json.dumps(data,indent=2)+"\n").encode("utf-8")

def sync_index(data, check=False):
    index=json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.is_file() else {"schema_version":1}
    detail_projects=[]
    for p in sorted((ROOT/"examples/projects_detail").glob("*.json")):
        detail_projects.append(json.loads(p.read_text(encoding="utf-8"))["id"])
    structural_projects=[]
    for p in sorted((ROOT/"examples/structural_site").glob("*.json")):
        structural_projects.append(json.loads(p.read_text(encoding="utf-8"))["id"])
    style_finish_projects=[]
    for p in sorted((ROOT/"examples/style_finish").glob("*.json")):
        style_finish_projects.append(json.loads(p.read_text(encoding="utf-8"))["id"])
    desired={
        "facade_profiles":[p["id"] for p in data["profiles"]],
        "style_registry":"style_registry.json",
        "style_profiles":data["count"],
        "style_families":len(data["families"]),
        "vanilla_detail_projects":detail_projects,
        "vanilla_finish_engine":True,
        "connection_modes":["attach","corridor","route","stairs"],
        "structural_node_types":["tower","porch","balcony","buttress_run","dormer_row"],
        "site_network_types":["path","road","plaza","wall","fence","retaining_wall","stairs"],
        "foundation_modes":["perimeter","piers","solid"],
        "structural_site_examples":structural_projects,
        "routed_corridors":True,
        "elevation_stairs":True,
        "structural_nodes":True,
        "site_networks":True,
        "foundation_engine":True,
        "style_finish_engine":True,
        "style_finish_profiles":14,
        "style_finish_examples":style_finish_projects,
        "reference_fit_engine":True,
        "reference_fit_constraints":["project_size","module_origin","module_size","port_anchor","facade_length","facade_height"],
    }
    if check:
        for key,value in desired.items():
            if index.get(key)!=value:
                return False
        return True
    index.update(desired)
    INDEX.write_bytes(encode(index))
    return True

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--check",action="store_true")
    args=ap.parse_args()
    data=build()
    payload=encode(data)
    if args.check:
        if not REGISTRY.is_file() or REGISTRY.read_bytes()!=payload or not sync_index(data,check=True):
            print("STYLE REGISTRY: MISMATCH")
            raise SystemExit(1)
        print("STYLE REGISTRY: PASS",data["count"])
        return
    REGISTRY.write_bytes(payload)
    sync_index(data)
    print("STYLE REGISTRY: WROTE",data["count"])

if __name__=="__main__":
    main()
