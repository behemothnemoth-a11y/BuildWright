#!/usr/bin/env python3
from __future__ import annotations
import argparse,filecmp,tempfile,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from composition.compiler import compile_brief

def outputs(id,base):return [base/f'{id}.{suffix}' for suffix in ['litematic','source.json','manifest.json','plan.svg']]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args();briefs=sorted((ROOT/'examples/composition').glob('*.json'));dest=ROOT/'composition/compiled_examples';dest.mkdir(parents=True,exist_ok=True)
 if a.check:
  bad=[]
  with tempfile.TemporaryDirectory() as td:
   tmp=Path(td)
   for b in briefs:
    import json;id=json.loads(b.read_text())['id'];compile_brief(ROOT,b,tmp)
    for expected,actual in zip(outputs(id,dest),outputs(id,tmp)):
     if not expected.is_file() or expected.read_bytes()!=actual.read_bytes():bad.append(str(expected.relative_to(ROOT)))
  if bad:raise SystemExit('compiled composition example mismatch: '+', '.join(bad[:10]))
  print('COMPOSITION EXAMPLE COMPILE CHECK: PASS',len(briefs));return
 for b in briefs:compile_brief(ROOT,b,dest)
 print('Composition examples compiled:',len(briefs))
if __name__=='__main__':main()
