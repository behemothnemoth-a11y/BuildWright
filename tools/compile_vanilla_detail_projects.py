#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, tempfile, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
from project_graph.compiler import compile_project

SUFFIXES=("litematic","project.json","manifest.json","plan.svg")

def outputs(ident,base):
    return [base/f"{ident}.{suffix}" for suffix in SUFFIXES]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--check",action="store_true")
    args=ap.parse_args()
    briefs=sorted((ROOT/"examples/projects_detail").glob("*.json"))
    dest=ROOT/"project_graph/detailed_examples"
    dest.mkdir(parents=True,exist_ok=True)

    if args.check:
        bad=[]
        with tempfile.TemporaryDirectory() as td:
            tmp=Path(td)
            for brief in briefs:
                ident=json.loads(brief.read_text(encoding="utf-8"))["id"]
                compile_project(ROOT,brief,tmp)
                for expected,actual in zip(outputs(ident,dest),outputs(ident,tmp)):
                    if not expected.is_file() or expected.read_bytes()!=actual.read_bytes():
                        bad.append(str(expected.relative_to(ROOT)))
        if bad:
            raise SystemExit("vanilla detail project mismatch: "+", ".join(bad[:10]))
        print("VANILLA DETAIL PROJECT COMPILE CHECK: PASS",len(briefs))
        return

    for brief in briefs:
        result=compile_project(ROOT,brief,dest)
        manifest=json.loads(Path(result["manifest"]).read_text(encoding="utf-8"))
        if manifest.get("detail_status")!="VANILLA_DETAIL_COMPLETE":
            raise SystemExit(f"{brief.name}: project detail status not complete")
        if int(manifest.get("block_entities",0) or 0)!=0:
            # Current detail-complete regression projects are pure vanilla and should
            # not carry Astra tile entities or other unexpected block entities.
            raise SystemExit(f"{brief.name}: unexpected block entities in vanilla detail project")
        print(brief.name,manifest["vanilla_finish"])
    print("VANILLA DETAIL PROJECTS: WROTE",len(briefs))

if __name__=="__main__":
    main()
