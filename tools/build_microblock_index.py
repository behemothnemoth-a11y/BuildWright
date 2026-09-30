#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'packs/microblock/registry.json'; OUT=ROOT/'packs/microblock/index.json'
def build():
 r=json.loads(REG.read_text(encoding='utf-8')); assets=[]
 for e in r['catalog']:
  o=json.loads((ROOT/e['path']).read_text(encoding='utf-8'))
  for a in o['assets']:
   assets.append({'id':a['id'],'path':e['path'],'category':a['category'],'family':a['family'],'name':a['name'],'styles':a.get('styles',[]),'source_vanilla_families':a.get('source_vanilla_families',[]),'candidate_class':a['candidate_class'],'default_tier':a['resolution']['default_tier'],'primitives':a.get('recommended_primitives',[])})
 return {'schema_version':1,'drop':'0003','assets':assets,'totals':r['totals']}
p=argparse.ArgumentParser(); p.add_argument('--check',action='store_true'); a=p.parse_args(); new=build(); txt=json.dumps(new,indent=2)+'\n'
if a.check:
 old=OUT.read_text(encoding='utf-8') if OUT.is_file() else ''
 if old!=txt: print('MICROBLOCK INDEX CHECK: FAIL'); sys.exit(1)
 print('MICROBLOCK INDEX CHECK: PASS'); sys.exit(0)
OUT.write_text(txt,encoding='utf-8'); print('wrote',OUT)
