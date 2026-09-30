#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'packs/registry.json'
errors=[]
try: reg=json.loads(REG.read_text(encoding='utf-8'))
except Exception as e: print('PACK VALIDATION: FAIL\n - registry unreadable:',e); sys.exit(1)
tech_ids={x['id'] for x in reg.get('techniques',[])}
palette_ids={x['id'] for x in reg.get('palettes',[])}
asset_ids=set(); pack_ids=set(); count=0
for entry in reg.get('catalog',[]):
    p=ROOT/entry['path']
    if not p.is_file(): errors.append(f'missing pack: {entry["path"]}'); continue
    try: obj=json.loads(p.read_text(encoding='utf-8'))
    except Exception as e: errors.append(f'invalid json {entry["path"]}: {e}'); continue
    pid=obj.get('pack_id')
    if pid in pack_ids: errors.append(f'duplicate pack_id: {pid}')
    pack_ids.add(pid)
    assets=obj.get('assets',[])
    if len(assets)!=entry.get('asset_count'): errors.append(f'asset_count mismatch: {pid}')
    for a in assets:
        count += 1; aid=a.get('id')
        if aid in asset_ids: errors.append(f'duplicate asset id: {aid}')
        asset_ids.add(aid)
        for key in ['name','category','family','tags','styles','scale_classes','dimension_hint','recommended_techniques','placement','variation','recipe','qa']:
            if key not in a: errors.append(f'{aid}: missing {key}')
        for t in a.get('recommended_techniques',[]):
            full=t if t.startswith('vanilla.technique.') else 'vanilla.technique.'+t
            if full not in tech_ids: errors.append(f'{aid}: unknown technique {t}')
        if not re.match(r'^vanilla\.[a-z0-9_]+\.[a-z0-9_]+\.[a-z0-9_]+$', aid or ''):
            errors.append(f'invalid asset id: {aid}')
if count != reg.get('totals',{}).get('assets'): errors.append(f'registry total assets mismatch: {count}')
for x in reg.get('palettes',[]):
    if not (ROOT/x['path']).is_file(): errors.append(f'missing palette: {x["path"]}')
for x in reg.get('techniques',[]):
    if not (ROOT/x['path']).is_file(): errors.append(f'missing technique: {x["path"]}')
for x in reg.get('style_profiles',[]):
    p=ROOT/x['path']
    if not p.is_file(): errors.append(f'missing style profile: {x["path"]}'); continue
    try: s=json.loads(p.read_text(encoding='utf-8'))
    except Exception as e: errors.append(f'invalid style profile {x["path"]}: {e}'); continue
    for pal in s.get('preferred_palettes',[]):
        if pal not in palette_ids: errors.append(f'{s.get("id")}: unknown palette {pal}')
if errors:
    print('PACK VALIDATION: FAIL')
    for e in errors[:200]: print(' -',e)
    if len(errors)>200: print(f' ... {len(errors)-200} more')
    sys.exit(1)
print('PACK VALIDATION: PASS')
print('packs:',len(pack_ids))
print('assets:',count)
print('techniques:',len(tech_ids))
print('palettes:',len(palette_ids))
print('style profiles:',len(reg.get('style_profiles',[])))
