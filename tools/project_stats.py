#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
compiled = ROOT / "project_graph" / "compiled_examples"
for manifest in sorted(compiled.glob("*.manifest.json")):
    data = json.loads(manifest.read_text(encoding="utf-8"))
    print(data["id"], {
        "modules": data["modules"],
        "connections": data["connections"],
        "size": data["size"],
        "blocks": data["blocks"],
        "facade": data["facade"],
        "roof": data["roof"],
    })
