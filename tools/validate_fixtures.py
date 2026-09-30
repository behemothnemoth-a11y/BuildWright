#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys,struct
from pathlib import Path
from litematic_codec import read,unpack
ROOT=Path(__file__).resolve().parents[1]
reg=json.loads((ROOT/'fixtures/registry.json').read_text())
errors=[]
for f in reg['fixtures']:
 p=ROOT/f['file']
 if not p.is_file():errors.append(f"missing {f['file']}");continue
 if hashlib.sha256(p.read_bytes()).hexdigest()!=f['sha256']:errors.append(f"sha mismatch {f['id']}");continue
 try:
  root=read(p); regions=root['Regions']; name=next(iter(regions)); r=regions[name]; size=r['Size']; vol=size['x']*size['y']*size['z'];pal=r['BlockStatePalette'];idx=unpack(r['BlockStates'],vol,len(pal))
  if any(i<0 or i>=len(pal) for i in idx):errors.append(f"palette index {f['id']}")
  nonair=sum(1 for i in idx if pal[i].get('Name')!='minecraft:air')
  if nonair!=root['Metadata']['TotalBlocks']:errors.append(f"block count {f['id']}: {nonair}!={root['Metadata']['TotalBlocks']}")
  if f['stage']=='microblock':
   tes=r.get('TileEntities',[])
   if len(tes)!=1:errors.append(f"microblock tile count {f['id']}")
   elif tes[0].get('id')!='astra_microblocks:test_host':errors.append(f"microblock id {f['id']}")
 except Exception as e:errors.append(f"decode {f['id']}: {e}")
manifest=json.loads((ROOT/'fixtures/corpus/transform_manifest.json').read_text())
for c in manifest['cases']:
 if not (ROOT/c['file']).is_file():errors.append(f"missing transform {c['file']}")
if errors:
 print('FIXTURE VALIDATION: FAIL');[print(' -',e) for e in errors];sys.exit(1)
print(f"FIXTURE VALIDATION: PASS ({reg['counts']['vanilla']} vanilla, {reg['counts']['microblock']} microblock, {reg['counts']['transform_cases']} transforms)")
