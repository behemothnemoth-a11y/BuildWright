#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(); ap.add_argument('--brief',required=True); ap.add_argument('--limit',type=int,default=12); ap.add_argument('--json',action='store_true'); args=ap.parse_args()
brief=json.loads(Path(args.brief).read_text(encoding='utf-8'))
idx=json.loads((ROOT/'packs/index.json').read_text(encoding='utf-8'))
style=brief.get('style_profile','').replace('style.',''); tags=set(brief.get('tags',[])); cats=set(brief.get('categories',[])); fams=set(brief.get('families',[])); scales=set(brief.get('scale_classes',[])); contexts=set(brief.get('contexts',[]))
profile_tags=set()
p=ROOT/f'packs/style_profiles/{style}.json'
if p.is_file(): profile_tags=set(json.loads(p.read_text(encoding='utf-8')).get('selection_tags',[]))
scored=[]
for a in idx['assets']:
    score=0; why=[]
    if cats and a['category'] in cats: score+=8; why.append('category')
    if fams and a['family'] in fams: score+=10; why.append('family')
    s=set(a.get('styles',[])); t=set(a.get('tags',[]))
    n=len(profile_tags&s); score+=n*4
    if n: why.append(f'style:{n}')
    n=len(tags&t); score+=n*3
    if n: why.append(f'tags:{n}')
    n=len(scales&set(a.get('scale_classes',[]))); score+=n*3
    if n: why.append('scale')
    n=len(contexts&set(a.get('contexts',[]))); score+=n*2
    if n: why.append('context')
    if score>0: scored.append((score,a,why))
scored.sort(key=lambda x:(-x[0],x[1]['id']))
res=[{'score':s,'id':a['id'],'name':a['name'],'category':a['category'],'family':a['family'],'why':w,'path':a['path']} for s,a,w in scored[:max(1,args.limit)]]
if args.json: print(json.dumps(res,indent=2))
else:
    for r in res: print(f"{r['score']:>3}  {r['id']}  ({', '.join(r['why'])})")
