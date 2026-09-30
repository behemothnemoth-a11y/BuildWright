#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from composition.planner import plan_brief
from composition.preview import render_plan_svg

def main():
 ap=argparse.ArgumentParser(description='Plan a BuildWright room/module composition without compiling it.')
 ap.add_argument('brief',type=Path);ap.add_argument('--json',type=Path);ap.add_argument('--svg',type=Path)
 a=ap.parse_args();brief=a.brief if a.brief.is_absolute() else ROOT/a.brief;plan=plan_brief(ROOT,brief)
 data=plan.to_dict();print(json.dumps(data,indent=2))
 if a.json:
  p=a.json if a.json.is_absolute() else ROOT/a.json;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2)+'\n')
 if a.svg:
  p=a.svg if a.svg.is_absolute() else ROOT/a.svg;render_plan_svg(plan,p)
 if any(w.startswith('REQUIRED:') for w in plan.warnings):raise SystemExit(2)
if __name__=='__main__':main()
