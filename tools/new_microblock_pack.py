#!/usr/bin/env python3
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(); p.add_argument('category'); p.add_argument('family'); a=p.parse_args()
t=json.loads((ROOT/'packs/microblock/templates/pack.template.json').read_text()); t['category']=a.category; t['family']=a.family; t['pack_id']=f'microblock.{a.category}.{a.family}'; t['name']=a.family.replace('_',' ').title()
out=ROOT/'packs/microblock'/a.category/f'{a.family}.json'; out.parent.mkdir(parents=True,exist_ok=True)
if out.exists(): raise SystemExit(f'exists: {out}')
out.write_text(json.dumps(t,indent=2)+'\n'); print(out)
