#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
required=['README.md','AGENTS.md','PROJECT_STATE.md','buildwright.json','VANILLA_BUILD_LANGUAGE.md','MICROBLOCK_IMPLEMENTATION.md','docs/PACK_SYSTEM.md','docs/PACK_AUTHORING_GUIDE.md','packs/registry.json','packs/index.json','packs/microblock/registry.json','packs/microblock/index.json','schemas/pack.schema.json','schemas/asset.schema.json','schemas/microblock_pack.schema.json','schemas/microblock_asset.schema.json','tools/validate_packs.py','tools/validate_microblocks.py','projects/wayne-manor/PROJECT.md','projects/wayne-manor/module_registry.json']
err=[f'missing required file: {r}' for r in required if not (ROOT/r).is_file()]
try:
 cfg=json.loads((ROOT/'buildwright.json').read_text(encoding='utf-8'))
 if cfg.get('name')!='BuildWright': err.append('buildwright.json name must be BuildWright')
 if cfg.get('version')!='0.3.0': err.append('buildwright.json version must be 0.3.0 for DROP 0003')
except Exception as e: err.append(f'buildwright.json invalid: {e}')
if err:
 print('BUILDWRIGHT VALIDATION: FAIL'); [print(' -',x) for x in err]; sys.exit(1)
for tool,args in [('validate_packs.py',[]),('build_pack_index.py',['--check']),('validate_microblocks.py',[]),('build_microblock_index.py',['--check'])]:
 r=subprocess.run([sys.executable,str(ROOT/'tools'/tool),*args],cwd=ROOT)
 if r.returncode: sys.exit(r.returncode)
print('BUILDWRIGHT VALIDATION: PASS')
