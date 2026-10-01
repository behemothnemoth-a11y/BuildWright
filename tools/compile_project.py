#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from project_graph.compiler import compile_project

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("brief", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    result = compile_project(ROOT, args.brief, args.output)
    print("PROJECT COMPILE: PASS")
    print("litematic:", result["litematic"])
    print("size:", result["readback"]["volume"], "volume")
    print("blocks:", result["readback"]["nonair"])
    print("block_entities:", result["readback"]["block_entities"])

if __name__ == "__main__":
    main()
