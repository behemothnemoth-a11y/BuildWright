#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
from project_graph.compiler import compile_project

SUFFIXES=("litematic","project.json","manifest.json","plan.svg")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--check",action="store_true")
    args=ap.parse_args()
    briefs=sorted((ROOT/"examples/style_showcases").glob("*.json"))
    out=ROOT/"project_graph/style_showcases"
    out.mkdir(parents=True,exist_ok=True)
    if not args.check:
        for brief in briefs:
            result=compile_project(ROOT,brief,out)
            print("compiled",brief.name,result["readback"])
        print("STYLE SHOWCASE COMPILE: PASS",{"examples":len(briefs)})
        return
    mismatches=[]
    with tempfile.TemporaryDirectory() as td:
        temp=Path(td)
        for brief in briefs:
            sid=json.loads(brief.read_text(encoding="utf-8"))["id"]
            compile_project(ROOT,brief,temp)
            for suffix in SUFFIXES:
                a=temp/f"{sid}.{suffix}"
                b=out/f"{sid}.{suffix}"
                if not b.is_file() or a.read_bytes()!=b.read_bytes():
                    mismatches.append(str(b.relative_to(ROOT)))
    if mismatches:
        print("style showcase mismatch:",", ".join(mismatches))
        raise SystemExit(1)
    print("STYLE SHOWCASE COMPILE CHECK: PASS",{"examples":len(briefs)})

if __name__=="__main__":
    main()
