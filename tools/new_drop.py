#!/usr/bin/env python3
"""Create a minimal numbered Buildwright drop workspace.

Usage:
    python tools/new_drop.py 2 VANILLA_PACK_FOUNDATION
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

if len(sys.argv) != 3:
    raise SystemExit("usage: new_drop.py <number> <PURPOSE>")
number = int(sys.argv[1])
purpose = re.sub(r"[^A-Z0-9_]+", "_", sys.argv[2].upper()).strip("_")
name = f"Buildwright_DROP_{number:04d}_{purpose}"
root = Path.cwd() / ".drop-work" / name
(root / "payload").mkdir(parents=True, exist_ok=False)
(root / "drop.json").write_text(json.dumps({
    "project": "Buildwright",
    "drop_id": f"DROP_{number:04d}_{purpose}",
    "package_name": name + ".zip",
    "payload_root": "payload",
    "commit_message": f"drop {number:04d}: {purpose.lower().replace('_', ' ')}"
}, indent=2) + "\n", encoding="utf-8")
(root / "README_FIRST.md").write_text(f"# {name}\n\nAdd payload files, generate checksums, then package.\n", encoding="utf-8")
print(root)
