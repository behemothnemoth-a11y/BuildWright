#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT/'tools') not in sys.path:
    sys.path.insert(0,str(ROOT/'tools'))

from litematic_codec import read

def state_name(entry):
    if isinstance(entry,dict):
        return str(entry.get('Name','minecraft:air'))
    return str(entry)

def audit_litematic(path:Path):
    root=read(path)
    bad_states=[]
    bad_entities=[]
    for region in root['Regions'].values():
        for state in region.get('BlockStatePalette',[]):
            name=state_name(state)
            if name.startswith('astra_microblocks:'):
                bad_states.append(name)
        for be in region.get('TileEntities',[]):
            ident=str(be.get('id',''))
            if ident.startswith('astra_microblocks:'):
                bad_entities.append(ident)
    return sorted(set(bad_states)),sorted(set(bad_entities))

def vanilla_room_paths():
    out=[]
    for manifest in sorted((ROOT/'composition/compiled_examples').glob('*.manifest.json')):
        data=json.loads(manifest.read_text(encoding='utf-8'))
        if int(data.get('microblock_hosts',0) or 0)==0:
            out.append(manifest.with_name(data['litematic']))
    return out

def main():
    groups={
      'vanilla_rooms':vanilla_room_paths(),
      'whole_buildings':sorted((ROOT/'project_graph/compiled_examples').glob('*.litematic')),
      'style_baselines':sorted((ROOT/'project_graph/style_showcases').glob('*.litematic'))
    }
    errors=[]
    count=0
    for group,paths in groups.items():
        for path in paths:
            count+=1
            states,entities=audit_litematic(path)
            if states or entities:
                errors.append(f"{group}/{path.name}: Astra content states={states} block_entities={entities}")
    visual=ROOT/'catalog/visual/visual_manifest.json'
    if visual.is_file():
        data=json.loads(visual.read_text(encoding='utf-8'))
        for group in ('rooms','projects','style_baselines'):
            for row in data.get('vanilla',{}).get(group,[]):
                if row.get('uses_astra_microblocks'):
                    errors.append(f"visual vanilla/{group}/{row.get('id')}: marked Astra")
        if any(x.get('stage')!='vanilla' for x in data.get('vanilla',{}).get('fixtures',[])):
            errors.append('visual vanilla fixtures contain non-vanilla stage')
    if errors:
        print('VANILLA BASELINE VALIDATION: FAIL')
        for e in errors: print(' -',e)
        raise SystemExit(1)
    print('VANILLA BASELINE VALIDATION: PASS',{'litematics':count,'policy':'no astra_microblocks namespace'})

if __name__=='__main__':
    main()
