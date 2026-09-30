#!/usr/bin/env python3
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
reg=json.loads((ROOT/'packs/microblock/registry.json').read_text()); profiles={p['id']:json.loads((ROOT/p['path']).read_text()) for p in reg['detail_profiles']}
p=argparse.ArgumentParser(); p.add_argument('--source-blocks',type=int,required=True); p.add_argument('--profile',default='architectural_standard'); a=p.parse_args()
b=profiles[a.profile]['budget']; hosts=(a.source_blocks*b['max_micro_hosts_per_100_source_blocks']+99)//100
print(json.dumps({'source_blocks':a.source_blocks,'profile':a.profile,'design_guardrail':{'max_micro_hosts_estimate':hosts,'target_average_materials_per_host':b['target_average_materials_per_host'],'max_tier4_share_percent':b['max_tier4_share_of_micro_hosts_percent']},'note':'Design guardrail, not an engine hard limit.'},indent=2))
