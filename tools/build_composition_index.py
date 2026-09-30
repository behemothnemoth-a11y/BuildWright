#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build():
 templates=[]
 for p in sorted((ROOT/'composition/templates').glob('*.json')):
  d=json.loads(p.read_text());templates.append({'id':d['id'],'name':d.get('name',d['id']),'file':str(p.relative_to(ROOT).as_posix()),'slots':len(d.get('slots',[])),'style_profile':d.get('style_profile'),'palette':d.get('palette')})
 palettes=[]
 for p in sorted((ROOT/'composition/palettes').glob('*.json')):
  d=json.loads(p.read_text());palettes.append({'id':d['id'],'name':d.get('name',d['id']),'file':str(p.relative_to(ROOT).as_posix())})
 examples=[]
 for p in sorted((ROOT/'examples/composition').glob('*.json')):
  d=json.loads(p.read_text());lit=ROOT/'composition/compiled_examples'/f"{d['id']}.litematic";examples.append({'id':d['id'],'template':d.get('template'),'brief':str(p.relative_to(ROOT).as_posix()),'compiled':str(lit.relative_to(ROOT).as_posix()) if lit.is_file() else None,'sha256':sha(lit) if lit.is_file() else None})
 return {'schema_version':1,'buildwright_version':'0.5.0','counts':{'templates':len(templates),'palettes':len(palettes),'examples':len(examples)},'templates':templates,'palettes':palettes,'examples':examples}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args();data=build();p=ROOT/'composition/index.json';blob=json.dumps(data,indent=2)+'\n'
 if a.check:
  if not p.is_file() or p.read_text()!=blob:raise SystemExit('composition index mismatch; run tools/build_composition_index.py')
  print('COMPOSITION INDEX: PASS',data['counts'])
 else:p.write_text(blob);print('composition index written',data['counts'])
if __name__=='__main__':main()
