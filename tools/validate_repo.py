#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
required=['README.md','AGENTS.md','PROJECT_STATE.md','buildwright.json','VANILLA_BUILD_LANGUAGE.md','MICROBLOCK_IMPLEMENTATION.md','docs/PACK_SYSTEM.md','docs/PACK_AUTHORING_GUIDE.md','packs/registry.json','packs/index.json','schemas/pack.schema.json','schemas/asset.schema.json','tools/validate_packs.py','projects/wayne-manor/PROJECT.md','projects/wayne-manor/module_registry.json']
err=[f'missing required file: {r}' for r in required if not (ROOT/r).is_file()]
try:
 cfg=json.loads((ROOT/'buildwright.json').read_text(encoding='utf-8'))
 if cfg.get('name')!='BuildWright': err.append('buildwright.json name must be BuildWright')
 if cfg.get('version')!='0.2.0': err.append('buildwright.json version must be 0.2.0 for DROP 0002')
except Exception as e: err.append(f'buildwright.json invalid: {e}')
if err:
 print('BUILDWRIGHT VALIDATION: FAIL'); [print(' -',x) for x in err]; sys.exit(1)
r=subprocess.run([sys.executable,str(ROOT/'tools/validate_packs.py')],cwd=ROOT)
if r.returncode: sys.exit(r.returncode)
r=subprocess.run([sys.executable,str(ROOT/'tools/build_pack_index.py'),'--check'],cwd=ROOT)
if r.returncode: sys.exit(r.returncode)
print('BUILDWRIGHT VALIDATION: PASS')
