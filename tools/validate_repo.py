#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "AGENTS.md",
    "PROJECT_STATE.md",
    "buildwright.json",
    "docs/VANILLA_BUILD_LANGUAGE.md",
    "docs/MICROBLOCK_IMPLEMENTATION.md",
    "docs/PACK_SYSTEM.md",
    "packs/registry.json",
    "projects/wayne-manor/PROJECT.md",
    "projects/wayne-manor/module_registry.json",
]

errors: list[str] = []
for rel in REQUIRED:
    if not (ROOT / rel).is_file():
        errors.append(f"missing required file: {rel}")

for rel in ["buildwright.json", "packs/registry.json", "projects/wayne-manor/module_registry.json"]:
    path = ROOT / rel
    if path.is_file():
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid JSON {rel}: {exc}")

try:
    cfg = json.loads((ROOT / "buildwright.json").read_text(encoding="utf-8"))
    if cfg.get("name") != "Buildwright":
        errors.append("buildwright.json name must be Buildwright")
    if "vanilla_build_language" not in cfg.get("pipeline", []):
        errors.append("pipeline is missing vanilla_build_language")
    if "microblock_implementation" not in cfg.get("pipeline", []):
        errors.append("pipeline is missing microblock_implementation")
except Exception:
    pass

try:
    modules = json.loads((ROOT / "projects/wayne-manor/module_registry.json").read_text(encoding="utf-8"))
    ids = {m.get("id") for m in modules.get("modules", [])}
    for required in {"GH-ARCH", "GH-STAIR", "GH-CEIL", "BATCAVE"}:
        if required not in ids:
            errors.append(f"Wayne module registry missing {required}")
except Exception:
    pass

seed = ROOT / "projects/wayne-manor/schematics/working/Wayne_Manor_Grand_Hall_CALM_CEILING_v7.litematic"
if not seed.is_file():
    errors.append("Wayne seed litematic is missing")
elif seed.stat().st_size == 0:
    errors.append("Wayne seed litematic is empty")

if errors:
    print("BUILDWRIGHT VALIDATION: FAIL")
    for e in errors:
        print(f" - {e}")
    sys.exit(1)

print("BUILDWRIGHT VALIDATION: PASS")
print(f"root: {ROOT}")
print(f"required files: {len(REQUIRED)}")
