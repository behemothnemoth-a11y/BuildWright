#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from composition.planner import plan_brief
from composition.compiler import _validate_litematic

def main():
 errors=[]
 templates=list((ROOT/'composition/templates').glob('*.json'));palettes=list((ROOT/'composition/palettes').glob('*.json'));briefs=list((ROOT/'examples/composition').glob('*.json'))
 tids=set();
 for p in templates:
  try:d=json.loads(p.read_text());assert d['id'];tids.add(d['id']);assert isinstance(d.get('slots',[]),list)
  except Exception as e:errors.append(f'{p}: {e}')
 pids=set()
 for p in palettes:
  try:d=json.loads(p.read_text());assert d['id'];pids.add(d['id']);assert 'shell' in d
  except Exception as e:errors.append(f'{p}: {e}')
 for p in briefs:
  try:
   d=json.loads(p.read_text());
   if d.get('template') not in tids:errors.append(f'{p}: unknown template {d.get("template")}')
   if d.get('palette') and d['palette'] not in pids:errors.append(f'{p}: unknown palette {d["palette"]}')
   plan=plan_brief(ROOT,d)
   req=[w for w in plan.warnings if w.startswith('REQUIRED:')]
   if req:errors.extend(f'{p}: {w}' for w in req)
   lit=ROOT/'composition/compiled_examples'/f"{d['id']}.litematic";man=ROOT/'composition/compiled_examples'/f"{d['id']}.manifest.json"
   if not lit.is_file() or not man.is_file():errors.append(f'{p}: compiled example missing')
   else:
    m=json.loads(man.read_text());_validate_litematic(lit,int(m['block_count']))
    if m.get('live_game_status')!='PENDING':errors.append(f'{man}: live_game_status must stay PENDING until tested')
  except Exception as e:errors.append(f'{p}: {type(e).__name__}: {e}')
 if errors:
  print('COMPOSITION VALIDATION: FAIL');[print(' -',e) for e in errors];raise SystemExit(1)
 print(f'COMPOSITION VALIDATION: PASS ({len(templates)} templates, {len(palettes)} palettes, {len(briefs)} examples)')
if __name__=='__main__':main()
