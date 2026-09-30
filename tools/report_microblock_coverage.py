#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
r=json.loads((ROOT/'packs/microblock/registry.json').read_text())
print('BuildWright Microblock Coverage')
print('='*34)
by={}
for e in r['catalog']:
 by.setdefault(e['category'],[0,0]); by[e['category']][0]+=1; by[e['category']][1]+=e['asset_count']
for k,(f,a) in by.items(): print(f'{k:14} {f:3} families  {a:4} variants')
print('-'*34); print('TOTAL',r['totals']['pack_files'],'families',r['totals']['assets'],'variants')
print('primitives',r['totals']['primitives'],'translation rules',r['totals']['translation_rules'],'profiles',r['totals']['detail_profiles'])
