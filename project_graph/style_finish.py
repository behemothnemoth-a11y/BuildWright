from __future__ import annotations
import json, math, random
from pathlib import Path
from typing import Any

from .assembler import exterior_sides
from .model import ProjectPlan
from .solver import PlacedModule

Vec3=tuple[int,int,int]
ROOT=Path(__file__).resolve().parents[1]

def _load_profiles():
    return json.loads((ROOT/"project_graph/style_finish_profiles.json").read_text(encoding="utf-8"))["families"]

def _outside(m:PlacedModule,side:str,along:int,y:int,depth:int=1)->Vec3:
    ox,oy,oz=m.origin;w,h,d=m.size
    if side=="north":return (ox+along,oy+y,oz-depth)
    if side=="south":return (ox+along,oy+y,oz+d-1+depth)
    if side=="west":return (ox-depth,oy+y,oz+along)
    return (ox+w-1+depth,oy+y,oz+along)

def _side_len(m:PlacedModule,side:str)->int:
    return m.size[0] if side in ("north","south") else m.size[2]

def _put(blocks,pos,state,stats,key):
    if pos in blocks:return False
    blocks[pos]=state;stats[key]=stats.get(key,0)+1;return True

def _material(profile,role,default):
    roles=profile.get("material_roles",{})
    return roles.get(role,profile.get({
        "wall":"wall_state","structure":"pier_state","trim":"trim_state",
        "accent":"accent_state","glass":"glass_state","plinth":"plinth_state","roof":"roof_state"
    }.get(role,""),default))

def _apply_bands(plan,placed,blocks,stats,cfg,style_cfg):
    trim=_material(plan.facade_profile,"trim","minecraft:spruce_planks")
    accent=_material(plan.facade_profile,"accent",trim)
    exposed=exterior_sides(plan)
    fractions=style_cfg.get("bands",[])
    for mid,sides in exposed.items():
        m=placed[mid]
        for side in sides:
            length=_side_len(m,side)
            for idx,f in enumerate(fractions):
                y=max(2,min(m.size[1]-2,round((m.size[1]-1)*float(f))))
                state=trim if idx%2==0 else accent
                for along in range(1,max(1,length-1)):
                    _put(blocks,_outside(m,side,along,y,1),state,stats,"band_blocks")

def _apply_corner_posts(plan,placed,blocks,stats,style_cfg):
    depth=max(0,int(style_cfg.get("corner_posts",0)))
    if not depth:return
    state=_material(plan.facade_profile,"structure","minecraft:stone_bricks")
    exposed=exterior_sides(plan)
    for mid,sides in exposed.items():
        m=placed[mid]
        for side in sides:
            length=_side_len(m,side)
            for along in (0,length-1):
                for dep in range(1,depth+1):
                    for y in range(1,max(2,m.size[1]-1)):
                        _put(blocks,_outside(m,side,along,y,dep),state,stats,"corner_blocks")

def _apply_eaves(plan,placed,blocks,stats,style_cfg):
    spacing=int(style_cfg.get("eave_spacing",0))
    if spacing<=0:return
    state=_material(plan.facade_profile,"trim","minecraft:spruce_planks")
    exposed=exterior_sides(plan)
    for mid,sides in exposed.items():
        m=placed[mid];y=max(2,m.size[1]-1)
        for side in sides:
            length=_side_len(m,side)
            for along in range(max(1,spacing//2),length-1,spacing):
                for dep in (1,2):
                    _put(blocks,_outside(m,side,along,y,dep),state,stats,"eave_blocks")

def _apply_lighting(plan,placed,blocks,stats,style_cfg):
    spacing=int(style_cfg.get("lantern_spacing",0))
    if spacing<=0:return
    bracket=_material(plan.facade_profile,"trim","minecraft:spruce_planks")
    exposed=exterior_sides(plan)
    for mid,sides in exposed.items():
        m=placed[mid]
        for side in sides:
            length=_side_len(m,side)
            for along in range(max(2,spacing//2),length-2,spacing):
                p=_outside(m,side,along,2,2)
                if _put(blocks,p,bracket,stats,"lighting_blocks"):
                    _put(blocks,(p[0],p[1]+1,p[2]),"minecraft:lantern[hanging=false,waterlogged=false]",stats,"lighting_blocks")

def _apply_planting(plan,placed,blocks,stats,style_cfg,rng):
    spacing=int(style_cfg.get("plant_spacing",0))
    if spacing<=0:return
    leaf="minecraft:oak_leaves[persistent=true,distance=1,waterlogged=false]"
    exposed=exterior_sides(plan)
    for mid,sides in exposed.items():
        m=placed[mid]
        for side in sides:
            length=_side_len(m,side)
            for along in range(max(3,spacing//2),length-3,spacing):
                if rng.random()>0.72:continue
                p=_outside(m,side,along,0,3)
                _put(blocks,p,leaf,stats,"plant_blocks")
                _put(blocks,(p[0],p[1]+1,p[2]),leaf,stats,"plant_blocks")

def _apply_service_runs(plan,placed,blocks,stats,style_cfg):
    spacing=int(style_cfg.get("service_spacing",0))
    if spacing<=0:return
    state=_material(plan.facade_profile,"accent","minecraft:copper_block")
    exposed=exterior_sides(plan)
    for mid,sides in exposed.items():
        m=placed[mid]
        for side in sides:
            length=_side_len(m,side)
            for along in range(max(2,spacing//2),length-2,spacing):
                for y in range(2,min(m.size[1]-2,7)):
                    _put(blocks,_outside(m,side,along,y,2),state,stats,"service_blocks")

def _apply_parapet(plan,placed,blocks,stats,style_cfg):
    if not style_cfg.get("parapet",False):return
    state=_material(plan.facade_profile,"trim","minecraft:stone_bricks")
    exposed=exterior_sides(plan)
    for mid,sides in exposed.items():
        m=placed[mid];y=m.origin[1]+m.size[1]+1
        for side in sides:
            length=_side_len(m,side)
            for along in range(length):
                p=_outside(m,side,along,m.size[1],1)
                _put(blocks,p,state,stats,"parapet_blocks")

def _apply_finials(plan,placed,blocks,stats,style_cfg):
    if not style_cfg.get("roof_finials",False):return
    state=_material(plan.facade_profile,"accent","minecraft:stone_bricks")
    for m in placed.values():
        ox,oy,oz=m.origin;w,h,d=m.size
        for x,z in ((ox,oz),(ox+w-1,oz),(ox,oz+d-1),(ox+w-1,oz+d-1)):
            top=max([y for (bx,y,bz) in blocks if bx==x and bz==z],default=oy+h)
            _put(blocks,(x,top+1,z),state,stats,"finial_blocks")
            _put(blocks,(x,top+2,z),"minecraft:lightning_rod[facing=up,waterlogged=false]",stats,"finial_blocks")

def apply_style_finish(plan:ProjectPlan,placed:dict[str,PlacedModule],blocks:dict[Vec3,str],brief:dict[str,Any]):
    cfg=dict(brief.get("style_finish",{}))
    enabled=cfg.get("enabled")
    if enabled is None:
        enabled=bool(brief.get("vanilla_finish",{}).get("enabled",False))
    if not enabled:
        return {"enabled":False,"status":"DISABLED","family":plan.facade_profile.get("family"),"astra_microblocks":False}
    family=str(plan.facade_profile.get("family","modern"))
    profiles=_load_profiles()
    style_cfg=dict(profiles.get(family,profiles["modern"]))
    style_cfg.update(cfg.get("overrides",{}))
    seed=int(cfg.get("seed",sum(ord(c) for c in str(brief.get("id","project")))+11011))
    rng=random.Random(seed)
    stats={"enabled":True,"status":"VANILLA_STYLE_FINISH_COMPLETE","family":family,"seed":seed,"astra_microblocks":False,
           "band_blocks":0,"corner_blocks":0,"eave_blocks":0,"lighting_blocks":0,"plant_blocks":0,
           "service_blocks":0,"parapet_blocks":0,"finial_blocks":0}
    _apply_bands(plan,placed,blocks,stats,cfg,style_cfg)
    _apply_corner_posts(plan,placed,blocks,stats,style_cfg)
    _apply_eaves(plan,placed,blocks,stats,style_cfg)
    _apply_lighting(plan,placed,blocks,stats,style_cfg)
    _apply_planting(plan,placed,blocks,stats,style_cfg,rng)
    _apply_service_runs(plan,placed,blocks,stats,style_cfg)
    _apply_parapet(plan,placed,blocks,stats,style_cfg)
    _apply_finials(plan,placed,blocks,stats,style_cfg)
    stats["total_blocks"]=sum(v for k,v in stats.items() if k.endswith("_blocks"))
    return stats
