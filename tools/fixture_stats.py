#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path
r=json.loads((Path(__file__).resolve().parents[1]/'fixtures/registry.json').read_text())
print('BuildWright compiled fixtures')
print(r['counts'])
print('by stage',dict(Counter(x['stage'] for x in r['fixtures'])))
print('by category',dict(Counter(x['category'] for x in r['fixtures'])))
