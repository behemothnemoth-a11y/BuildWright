#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from project_graph.compiler import compile_project

SUFFIXES = ("litematic", "project.json", "manifest.json", "plan.svg")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    examples = sorted((ROOT / "examples" / "projects").glob("*.json"))
    committed = ROOT / "project_graph" / "compiled_examples"
    committed.mkdir(parents=True, exist_ok=True)

    if not args.check:
        for brief in examples:
            out = compile_project(ROOT, brief, committed)
            print("compiled", brief.name, out["readback"])
        print("PROJECT EXAMPLE COMPILE: PASS", {"examples": len(examples)})
        return

    mismatches = []
    with tempfile.TemporaryDirectory() as td:
        temp = Path(td)
        for brief in examples:
            project_id = json.loads(brief.read_text(encoding="utf-8"))["id"]
            compile_project(ROOT, brief, temp)
            for suffix in SUFFIXES:
                generated = temp / f"{project_id}.{suffix}"
                expected = committed / f"{project_id}.{suffix}"
                if not expected.is_file() or generated.read_bytes() != expected.read_bytes():
                    mismatches.append(str(expected.relative_to(ROOT)))
    if mismatches:
        print("compiled project example mismatch:", ", ".join(mismatches))
        raise SystemExit(1)
    print("PROJECT EXAMPLE COMPILE CHECK: PASS", {"examples": len(examples)})

if __name__ == "__main__":
    main()
