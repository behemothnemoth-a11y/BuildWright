#!/usr/bin/env python3
import hashlib,json,struct,sys
from pathlib import Path
from litematic_codec import read
ROOT=Path(__file__).resolve().parents[1];m=json.loads((ROOT/'fixtures/corpus/transform_manifest.json').read_text());bad=[]
# Offline gate validates corpus structure and uniqueness. Live transformed-cell verification belongs to Fabric/Litematica integration.
seen=set()
for c in m['cases']:
 p=ROOT/c['file'];key=(c['fixture'],c['orientation'])
 if key in seen:bad.append('duplicate '+str(key))
 seen.add(key)
 if not p.is_file():bad.append('missing '+c['file']);continue
 try:
  r=read(p);reg=next(iter(r['Regions'].values()));pal=reg['BlockStatePalette'];host=[x for x in pal if x.get('Name','').startswith('astra_microblocks:')]
  if not host:bad.append('no Astra host '+c['file'])
 except Exception as e:bad.append(f"decode {c['file']}: {e}")
if bad:print('TRANSFORM CORPUS: FAIL');[print(' -',x) for x in bad];sys.exit(1)
print('TRANSFORM CORPUS: PASS',len(m['cases']))
