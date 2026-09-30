#!/usr/bin/env python3
from __future__ import annotations
import argparse,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from composition.planner import plan_brief
from composition.preview import render_plan_svg

def main():
 ap=argparse.ArgumentParser();ap.add_argument('brief',type=Path);ap.add_argument('output',type=Path);a=ap.parse_args()
 b=a.brief if a.brief.is_absolute() else ROOT/a.brief;o=a.output if a.output.is_absolute() else ROOT/a.output
 render_plan_svg(plan_brief(ROOT,b),o);print(o)
if __name__=='__main__':main()
