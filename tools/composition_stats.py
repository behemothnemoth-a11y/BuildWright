#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
templates=list((ROOT/'composition/templates').glob('*.json'));palettes=list((ROOT/'composition/palettes').glob('*.json'));examples=list((ROOT/'examples/composition').glob('*.json'));compiled=list((ROOT/'composition/compiled_examples').glob('*.litematic'))
print(f'templates: {len(templates)}');print(f'palettes: {len(palettes)}');print(f'example briefs: {len(examples)}');print(f'compiled example modules: {len(compiled)}')
if (ROOT/'composition/index.json').is_file():
 d=json.loads((ROOT/'composition/index.json').read_text());print('index version:',d.get('schema_version'))
