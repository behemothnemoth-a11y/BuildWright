from __future__ import annotations
import hashlib,json
from pathlib import Path

def sha256(path:Path):return hashlib.sha256(path.read_bytes()).hexdigest()

def write_manifest(path:Path, *, plan, litematic_path:Path, source_path:Path, block_count:int, palette_id:str|None, microblock_hosts:int, warnings:list[str]):
    data={
      'schema_version':1,'brief_id':plan.brief_id,'template':plan.template_id,'room_size':list(plan.room_size),
      'style_profile':plan.style_profile,'palette':palette_id,'seed':plan.seed,
      'placements':[p.to_dict() for p in plan.placements],'connectors':plan.connectors,
      'block_count':block_count,'microblock_hosts':microblock_hosts,
      'source':str(source_path.as_posix()),'litematic':str(litematic_path.as_posix()),
      'litematic_sha256':sha256(litematic_path),'warnings':warnings,
      'maturity':'OFFLINE_COMPILED','live_game_status':'PENDING'
    }
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes((json.dumps(data,indent=2)+'\n').encode('utf-8'));return data
