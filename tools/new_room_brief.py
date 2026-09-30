#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('id');ap.add_argument('--template',default='library');ap.add_argument('--size',default='41,15,31');ap.add_argument('--style',default='style.massive_gothic_manor');ap.add_argument('--palette',default='composition.massive_gothic_manor');ap.add_argument('--seed',type=int,default=1);ap.add_argument('--output',type=Path)
 a=ap.parse_args();size=[int(x) for x in a.size.split(',')];d={'schema_version':1,'id':a.id,'name':a.id.replace('_',' ').title(),'stage':'vanilla','template':a.template,'size':size,'style_profile':a.style,'palette':a.palette,'seed':a.seed,'fixture_policy':{'density':0.85,'max_repeats':4},'connectors':[]}
 p=a.output or ROOT/'examples/composition'/f'{a.id}.json';p=p if p.is_absolute() else ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n');print(p)
if __name__=='__main__':main()
