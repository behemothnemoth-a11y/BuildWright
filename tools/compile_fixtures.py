#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,struct,tempfile
from pathlib import Path
from litematic_codec import B,I,L,make,i64
ROOT=Path(__file__).resolve().parents[1]
def as_signed(u):return i64(int(u,16))
def astra_be(words,material):
 oak=words[:] if material=='oak' else [0]*64
 d={'id':'astra_microblocks:test_host','x':I(0),'y':I(0),'z':I(0),'astra_orientation':I(0),'grid_format_v1':B(1),'revision':L(1),'has_undo':B(0),'materials_v2':B(1)}
 for i,v in enumerate(words):d[f'grid_{i}']=L(v)
 for i,v in enumerate(oak):d[f'oak_{i}']=L(v)
 return d
def compile_one(src,out):
 d=json.loads(src.read_text())
 if d['stage']=='vanilla':
  blocks={tuple(x['pos']):x['state'] for x in d['blocks']};name='BuildWright '+d['id'].replace('_',' ').title();desc=(f"BuildWright vanilla detail fixture: {d['category']}/{d['family']}" if d.get('detail_fixture') else f"BuildWright compiled vanilla fixture: {d['category']}/{d['family']}");make(out,name,tuple(d['size']),blocks,desc=desc)
 else:
  words=[as_signed(x) for x in d['occupancy_words_hex']];material=d['host_material'];host='astra_microblocks:oak_host' if material=='oak' else 'astra_microblocks:test_host';blocks={(0,0,0):host+'[orientation=0]'};make(out,'BuildWright MB '+d['id'].replace('_',' ').title(),(1,1,1),blocks,[astra_be(words,material)],desc='Astra Microblocks compiled fixture')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args();reg=json.loads((ROOT/'fixtures/registry.json').read_text());bad=[]
 for item in reg['fixtures']:
  src=ROOT/item['source'];dst=ROOT/item['file']
  if a.check:
   with tempfile.TemporaryDirectory() as td:
    tmp=Path(td)/dst.name;compile_one(src,tmp)
    if hashlib.sha256(tmp.read_bytes()).hexdigest()!=hashlib.sha256(dst.read_bytes()).hexdigest():bad.append(item['id'])
  else:compile_one(src,dst)
 if bad:raise SystemExit('fixture source compile mismatch: '+', '.join(bad))
 print('FIXTURE COMPILE CHECK: PASS' if a.check else 'Fixtures compiled')
if __name__=='__main__':main()
