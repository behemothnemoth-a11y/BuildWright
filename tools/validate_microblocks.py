#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'packs/microblock/registry.json'
errors=[]
try:r=json.loads(REG.read_text(encoding='utf-8'))
except Exception as e: print('MICROBLOCK VALIDATION: FAIL\n - registry unreadable:',e); sys.exit(1)
prim=json.loads((ROOT/r['primitives']).read_text(encoding='utf-8'))
prim_ids={x['id'] for x in prim['primitives']}
profile_ids={x['id'] for x in r.get('detail_profiles',[])}
asset_ids=set(); pack_ids=set(); count=0
for entry in r.get('catalog',[]):
 p=ROOT/entry['path']
 if not p.is_file(): errors.append(f'missing pack: {entry["path"]}'); continue
 try:o=json.loads(p.read_text(encoding='utf-8'))
 except Exception as e: errors.append(f'invalid json {entry["path"]}: {e}'); continue
 pid=o.get('pack_id')
 if pid in pack_ids: errors.append(f'duplicate pack_id: {pid}')
 pack_ids.add(pid)
 assets=o.get('assets',[])
 if len(assets)!=entry.get('asset_count'): errors.append(f'asset_count mismatch: {pid}')
 for a in assets:
  count+=1; aid=a.get('id')
  if aid in asset_ids: errors.append(f'duplicate asset id: {aid}')
  asset_ids.add(aid)
  if not re.match(r'^microblock\.[a-z0-9_]+\.[a-z0-9_]+\.[a-z0-9_]+$',aid or ''): errors.append(f'invalid asset id: {aid}')
  for key in ['source_vanilla_families','candidate_class','resolution','recommended_primitives','translation','complexity','variation','qa']:
   if key not in a: errors.append(f'{aid}: missing {key}')
  for op in a.get('recommended_primitives',[]):
   if op not in prim_ids: errors.append(f'{aid}: unknown primitive {op}')
  tier=a.get('resolution',{}).get('default_tier')
  if tier not in ['TIER_0','TIER_1','TIER_2','TIER_3','TIER_4']: errors.append(f'{aid}: invalid default tier {tier}')
  if a.get('complexity',{}).get('preferred_min_feature_cells',0)<1: errors.append(f'{aid}: min feature cells must be >=1')
if count!=r.get('totals',{}).get('assets'): errors.append(f'registry total assets mismatch: {count}')
if len(pack_ids)!=r.get('totals',{}).get('pack_files'): errors.append('registry pack_files mismatch')
for p in r.get('detail_profiles',[]):
 if not (ROOT/p['path']).is_file(): errors.append(f'missing detail profile: {p["path"]}')
for required in [r.get('translation_map'),r.get('resolution_tiers'),r.get('material_policy')]:
 if not required or not (ROOT/required).is_file(): errors.append(f'missing required microblock support file: {required}')
if errors:
 print('MICROBLOCK VALIDATION: FAIL')
 for e in errors[:300]: print(' -',e)
 if len(errors)>300: print(f' ... {len(errors)-300} more')
 sys.exit(1)
print('MICROBLOCK VALIDATION: PASS')
print('packs:',len(pack_ids)); print('assets:',count); print('primitives:',len(prim_ids)); print('detail profiles:',len(profile_ids))
