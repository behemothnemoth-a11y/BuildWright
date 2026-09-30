from __future__ import annotations
import json
from pathlib import Path

def load_style(root:Path, style_id:str|None)->dict:
    if not style_id:return {}
    slug=style_id.split('.')[-1]
    p=root/'packs/style_profiles'/f'{slug}.json'
    return json.loads(p.read_text(encoding='utf-8')) if p.is_file() else {}
