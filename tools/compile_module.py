#!/usr/bin/env python3
from __future__ import annotations
import argparse,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from composition.compiler import compile_brief

def main():
 ap=argparse.ArgumentParser(description='Compile a BuildWright composition brief to source + manifest + SVG + .litematic.')
 ap.add_argument('brief',type=Path);ap.add_argument('--output-dir',type=Path,default=Path('composition/compiled_modules'))
 a=ap.parse_args();brief=a.brief if a.brief.is_absolute() else ROOT/a.brief;out=a.output_dir if a.output_dir.is_absolute() else ROOT/a.output_dir
 r=compile_brief(ROOT,brief,out)
 print('COMPOSITION COMPILE: PASS')
 for k in ('litematic','source','manifest','preview'):print(f'{k}: {r[k]}')
 print('readback:',r['readback'])
 if r['plan'].warnings:
  print('warnings:');[print(' -',w) for w in r['plan'].warnings]
 if any(w.startswith('REQUIRED:') for w in r['plan'].warnings):raise SystemExit(2)
if __name__=='__main__':main()
