#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def build():
    reg=json.loads((ROOT/'packs/registry.json').read_text(encoding='utf-8'))
    out=[]
    for e in reg.get('catalog',[]):
        p=json.loads((ROOT/e['path']).read_text(encoding='utf-8'))
        for a in p.get('assets',[]):
            out.append({'id':a['id'],'pack_id':p['pack_id'],'path':e['path'],'category':a['category'],'family':a['family'],'name':a['name'],'tags':a['tags'],'styles':a['styles'],'scale_classes':a['scale_classes'],'contexts':a['contexts']})
    return {'schema_version':1,'generated_from_registry_schema':reg.get('schema_version'),'asset_count':len(out),'assets':out}
ap=argparse.ArgumentParser(); ap.add_argument('--check',action='store_true'); args=ap.parse_args()
new=build(); path=ROOT/'packs/index.json'
if args.check:
    old=json.loads(path.read_text(encoding='utf-8')) if path.exists() else None
    if old!=new:
        print('PACK INDEX: OUT OF DATE'); sys.exit(1)
    print('PACK INDEX: PASS',new['asset_count']); sys.exit(0)
path.write_text(json.dumps(new,indent=2)+"\n",encoding='utf-8'); print('wrote',path,'assets',new['asset_count'])
