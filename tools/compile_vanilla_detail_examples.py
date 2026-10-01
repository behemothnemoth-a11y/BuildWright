#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, tempfile, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
from composition.compiler import compile_brief

SUFFIXES=("litematic","source.json","manifest.json","plan.svg")

def outputs(ident,base):
    return [base/f"{ident}.{suffix}" for suffix in SUFFIXES]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--check",action="store_true")
    args=ap.parse_args()
    briefs=sorted((ROOT/"examples/vanilla_detail").glob("*.json"))
    dest=ROOT/"composition/detailed_examples"
    dest.mkdir(parents=True,exist_ok=True)

    if args.check:
        bad=[]
        with tempfile.TemporaryDirectory() as td:
            tmp=Path(td)
            for brief in briefs:
                ident=json.loads(brief.read_text(encoding="utf-8"))["id"]
                compile_brief(ROOT,brief,tmp)
                for expected,actual in zip(outputs(ident,dest),outputs(ident,tmp)):
                    if not expected.is_file() or expected.read_bytes()!=actual.read_bytes():
                        bad.append(str(expected.relative_to(ROOT)))
        if bad:
            raise SystemExit("vanilla detail example mismatch: "+", ".join(bad[:10]))
        print("VANILLA DETAIL EXAMPLE COMPILE CHECK: PASS",len(briefs))
        return

    for brief in briefs:
        result=compile_brief(ROOT,brief,dest)
        manifest=json.loads(Path(result["manifest"]).read_text(encoding="utf-8"))
        if manifest.get("detail_status")!="VANILLA_DETAIL_COMPLETE":
            raise SystemExit(f"{brief.name}: detail status not complete")
        if int(manifest.get("microblock_hosts",0) or 0)!=0:
            raise SystemExit(f"{brief.name}: microblocks leaked into vanilla detail output")
        print(brief.name,manifest["vanilla_detail"])
    print("VANILLA DETAIL EXAMPLES: WROTE",len(briefs))

if __name__=="__main__":
    main()
