#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,tempfile,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
from project_graph.compiler import compile_project

SUFFIXES=("litematic","project.json","manifest.json","plan.svg")

def paths(ident,base):
    return [base/f"{ident}.{s}" for s in SUFFIXES]

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--check",action="store_true");args=ap.parse_args()
    briefs=sorted((ROOT/"examples/style_finish").glob("*.json"))
    dest=ROOT/"project_graph/style_finish_examples";dest.mkdir(parents=True,exist_ok=True)
    if args.check:
        bad=[]
        with tempfile.TemporaryDirectory() as td:
            tmp=Path(td)
            for brief in briefs:
                ident=json.loads(brief.read_text(encoding="utf-8"))["id"]
                compile_project(ROOT,brief,tmp)
                for expected,actual in zip(paths(ident,dest),paths(ident,tmp)):
                    if not expected.is_file() or expected.read_bytes()!=actual.read_bytes():
                        bad.append(str(expected.relative_to(ROOT)))
        if bad:raise SystemExit("style-finish example mismatch: "+", ".join(bad[:20]))
        print("STYLE FINISH EXAMPLE COMPILE CHECK: PASS",len(briefs));return
    for brief in briefs:
        result=compile_project(ROOT,brief,dest)
        m=json.loads(Path(result["manifest"]).read_text(encoding="utf-8"))
        if m.get("block_entities",0):raise SystemExit(f"{brief.name}: unexpected block entities")
        if not m.get("style_finish",{}).get("enabled"):raise SystemExit(f"{brief.name}: style finish disabled")
        print(brief.name,{"blocks":m["blocks"],"family":m["style_finish"].get("family"),"finish_blocks":m["style_finish"].get("total_blocks"),"reference":m["reference_fit"].get("status")})
    print("STYLE FINISH EXAMPLES: WROTE",len(briefs))

if __name__=="__main__":main()
