#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
reg=json.loads((ROOT/"project_graph/style_registry.json").read_text(encoding="utf-8"))
families=Counter(p["family"] for p in reg["profiles"])
roofs=Counter(p["default_roof"] for p in reg["profiles"])
windows=Counter(p["window_shape"] for p in reg["profiles"])
print("STYLE PROFILES:",reg["count"])
print("FAMILIES:")
for k,v in sorted(families.items()): print(f"  {k}: {v}")
print("DEFAULT ROOFS:")
for k,v in sorted(roofs.items()): print(f"  {k}: {v}")
print("WINDOW LANGUAGES:",len(windows))
