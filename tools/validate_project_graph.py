#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from project_graph.model import load_project
from project_graph.solver import solve_project

def main():
    briefs = sorted((ROOT / "examples" / "projects").glob("*.json"))
    if not briefs:
        raise SystemExit("No project graph examples found")
    for path in briefs:
        data = json.loads(path.read_text(encoding="utf-8"))
        plan = load_project(ROOT, data)
        placed = solve_project(plan)
        if len(placed) != len(data["modules"]):
            raise SystemExit(f"{path.name}: not all modules placed")
        print(path.name, {"modules": len(placed), "connections": len(plan.connections)})
    print("PROJECT GRAPH VALIDATION: PASS", {"examples": len(briefs)})

if __name__ == "__main__":
    main()
