#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
reg=json.loads((ROOT/'packs/registry.json').read_text(encoding='utf-8'))
print('BuildWright vanilla pack coverage')
print('families:',reg['totals']['pack_files'],'assets:',reg['totals']['assets'],'techniques:',reg['totals']['techniques'],'palettes:',reg['totals']['palettes'],'styles:',reg['totals']['style_profiles'])
c=Counter(x['category'] for x in reg['catalog'])
a=Counter()
for x in reg['catalog']: a[x['category']]+=x['asset_count']
for k in sorted(c): print(f'{k:12} families={c[k]:3} assets={a[k]:4}')
