#!/usr/bin/env python3
import argparse
from pathlib import Path
from litematic_codec import read,unpack
ap=argparse.ArgumentParser();ap.add_argument('file');a=ap.parse_args();root=read(Path(a.file))
print('Version',root.get('Version'),'SubVersion',root.get('SubVersion'),'DataVersion',root.get('MinecraftDataVersion'))
print('Metadata',root.get('Metadata'))
for name,r in root['Regions'].items():
 s=r['Size'];vol=s['x']*s['y']*s['z'];pal=r['BlockStatePalette'];idx=unpack(r['BlockStates'],vol,len(pal));print(name,s,'palette',len(pal),'nonair',sum(pal[i].get('Name')!='minecraft:air' for i in idx),'tile_entities',len(r.get('TileEntities',[])))
