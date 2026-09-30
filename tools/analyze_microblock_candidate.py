#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
rules=json.loads((ROOT/'packs/microblock/translation_map.json').read_text())['rules']
parser=argparse.ArgumentParser(); parser.add_argument('family'); a=parser.parse_args()
hits=[x for x in rules if x['source_family']==a.family]
if not hits:
 print(json.dumps({'source_family':a.family,'candidate_class':'KEEP_VANILLA','reason':'No default microblock mapping; keep vanilla unless manually justified.'},indent=2))
else:
 print(json.dumps({'source_family':a.family,'candidate_class':'GOOD_MICROBLOCK_TARGET','mappings':hits},indent=2))
