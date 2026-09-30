#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
reg=json.loads((ROOT/'packs/microblock/registry.json').read_text())
idx=json.loads((ROOT/'packs/microblock/index.json').read_text())['assets']
tmap=json.loads((ROOT/'packs/microblock/translation_map.json').read_text())['rules']
profiles={p['id']:json.loads((ROOT/p['path']).read_text()) for p in reg['detail_profiles']}
parser=argparse.ArgumentParser(description='Plan BuildWright vanilla-to-microblock refinement.')
parser.add_argument('--source-family',action='append',default=[],help='Vanilla family such as vanilla.architecture.arches')
parser.add_argument('--profile',default='architectural_standard')
parser.add_argument('--style',default='general')
parser.add_argument('--limit',type=int,default=8)
parser.add_argument('--json-out')
a=parser.parse_args(); allowed=set(profiles[a.profile]['allowed_tiers']); items=[]
for sf in a.source_family:
 targets=[]
 for rule in tmap:
  if rule['source_family']==sf:
   fam=rule['target_family'].split('.')[-1]
   matches=[x for x in idx if x['family']==fam and x['default_tier'] in allowed and (a.style=='general' or a.style in x.get('styles',[]) or 'general' in x.get('styles',[]))]
   targets.extend([x['id'] for x in matches[:a.limit]])
 if targets: items.append({'source':sf,'candidate_class':'GOOD_MICROBLOCK_TARGET','targets':targets[:a.limit]})
plan={'schema_version':1,'provider':'astra_microblocks_0_4_0','detail_profile':a.profile,'style':a.style,'items':items}
print(json.dumps(plan,indent=2))
if a.json_out: Path(a.json_out).write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
