#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROFILES=ROOT/"project_graph/profiles"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("family")
    ap.add_argument("display_name")
    ap.add_argument("--base",default="modern")
    args=ap.parse_args()
    if not re.fullmatch(r"[a-z0-9_]+",args.id):
        raise SystemExit("style id must be lowercase snake_case")
    target=PROFILES/f"{args.id}.json"
    if target.exists():
        raise SystemExit(f"already exists: {target}")
    source=PROFILES/f"{args.base}.json"
    if not source.is_file():
        raise SystemExit(f"base style not found: {args.base}")
    data=json.loads(source.read_text(encoding="utf-8"))
    data["id"]=args.id
    data["family"]=args.family
    data["display_name"]=args.display_name
    data["derived_from"]=args.base
    target.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    print(target.relative_to(ROOT))
    print("Edit the new profile, then run: python tools/build_style_registry.py")

if __name__=="__main__":
    main()
