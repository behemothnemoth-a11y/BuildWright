#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def brief_row(path,compiled_dir):
    d=load(path)
    lit=ROOT/compiled_dir/f"{d['id']}.litematic"
    return {
      'id':d['id'],
      'template':d.get('template'),
      'brief':str(path.relative_to(ROOT).as_posix()),
      'compiled':str(lit.relative_to(ROOT).as_posix()) if lit.is_file() else None,
      'sha256':sha(lit) if lit.is_file() else None,
      'detail_status':'VANILLA_DETAIL_COMPLETE' if d.get('vanilla_detail',{}).get('enabled') else 'BASELINE'
    }

def build():
    cfg=load(ROOT/'buildwright.json')
    templates=[]
    for p in sorted((ROOT/'composition/templates').glob('*.json')):
        d=load(p)
        templates.append({
          'id':d['id'],'name':d.get('name',d['id']),
          'file':str(p.relative_to(ROOT).as_posix()),
          'slots':len(d.get('slots',[])),
          'style_profile':d.get('style_profile'),'palette':d.get('palette')
        })
    palettes=[]
    for p in sorted((ROOT/'composition/palettes').glob('*.json')):
        d=load(p)
        palettes.append({'id':d['id'],'name':d.get('name',d['id']),'file':str(p.relative_to(ROOT).as_posix())})
    examples=[brief_row(p,'composition/compiled_examples') for p in sorted((ROOT/'examples/composition').glob('*.json'))]
    detail_examples=[brief_row(p,'composition/detailed_examples') for p in sorted((ROOT/'examples/vanilla_detail').glob('*.json'))]
    detail_data=load(ROOT/'composition/detail_profiles.json')
    detail_profiles=[
      {'id':name,'density':profile.get('density'),'recipes':len(profile.get('recipes',[])),'surfaces':profile.get('surfaces',{})}
      for name,profile in sorted(detail_data['profiles'].items())
    ]
    return {
      'schema_version':2,
      'buildwright_version':cfg['version'],
      'counts':{
        'templates':len(templates),'palettes':len(palettes),'examples':len(examples),
        'vanilla_detail_profiles':len(detail_profiles),'vanilla_detail_examples':len(detail_examples)
      },
      'templates':templates,'palettes':palettes,'examples':examples,
      'vanilla_detail_profiles':detail_profiles,'vanilla_detail_examples':detail_examples
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args()
    data=build();p=ROOT/'composition/index.json';blob=json.dumps(data,indent=2)+'\n'
    if a.check:
        if not p.is_file() or p.read_text(encoding='utf-8')!=blob:
            raise SystemExit('composition index mismatch; run tools/build_composition_index.py')
        print('COMPOSITION INDEX: PASS',data['counts'])
    else:
        p.write_text(blob,encoding='utf-8')
        print('composition index written',data['counts'])

if __name__=='__main__':main()
