#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(); ap.add_argument('category'); ap.add_argument('family'); args=ap.parse_args()
out=ROOT/'packs/vanilla'/args.category/f'{args.family}.json'
if out.exists(): raise SystemExit(f'exists: {out}')
tpl=json.loads((ROOT/'packs/templates/pack.template.json').read_text(encoding='utf-8'))
tpl['pack_id']=f'vanilla.{args.category}.{args.family}'; tpl['name']=args.family.replace('_',' ').title(); tpl['category']=args.category; tpl['family']=args.family
out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(tpl,indent=2)+'\n',encoding='utf-8'); print(out)
