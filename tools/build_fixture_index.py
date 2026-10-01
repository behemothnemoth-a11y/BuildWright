#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];reg=json.loads((ROOT/'fixtures/registry.json').read_text())
idx={'schema_version':1,'fixtures':[{k:v for k,v in x.items() if k in ('id','stage','category','family','provider','file','source','preview','size','blocks','occupied_cells','detail_fixture')} for x in reg['fixtures']]}
out=ROOT/'fixtures/index.json';text=json.dumps(idx,indent=2)+'\n'
ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args()
if a.check:
 if out.read_text()!=text:print('fixture index stale');sys.exit(1)
 print('fixture index: PASS')
else:out.write_text(text);print(out)
