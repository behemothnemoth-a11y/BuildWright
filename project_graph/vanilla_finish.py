from __future__ import annotations

import random
from typing import Any

from .assembler import exterior_sides
from .model import CARDINAL, ProjectPlan, port_for
from .solver import PlacedModule, world_port

Vec3=tuple[int,int,int]
OUT={"north":(0,0,-1),"south":(0,0,1),"west":(-1,0,0),"east":(1,0,0)}

HISTORIC_FAMILIES={"gothic","classical","historic_european","mediterranean","vernacular","east_asian","desert","fantasy","ancient"}
PLANTED_SITES={"formal","courtyard","garden","integrated_landscape","lush_integrated","forest","temple_garden","overgrown"}
SERVICE_FAMILIES={"industrial","speculative","modern"}

def _add(a,b,n=1):
    return tuple(a[i]+b[i]*n for i in range(3))

def _outside(module:PlacedModule,side:str,along:int,y:int,depth:int=1)->Vec3:
    ox,oy,oz=module.origin;w,h,d=module.size
    if side=="north": return (ox+along,oy+y,oz-depth)
    if side=="south": return (ox+along,oy+y,oz+d-1+depth)
    if side=="west": return (ox-depth,oy+y,oz+along)
    return (ox+w-1+depth,oy+y,oz+along)

def _side_length(module:PlacedModule,side:str)->int:
    return module.size[0] if side in ("north","south") else module.size[2]

def _put(blocks,pos,state,stats,key):
    if pos in blocks:
        return False
    blocks[pos]=state
    stats[key]=stats.get(key,0)+1
    return True

def _connected_endpoints(plan:ProjectPlan):
    out=set()
    for c in plan.connections:
        out.add((c.a_module,c.a_port))
        out.add((c.b_module,c.b_port))
    return out

def _entrance_finish(plan,placed,blocks,stats,profile,cfg):
    connected=_connected_endpoints(plan)
    pad_state=cfg.get("entrance_state",profile.get("plinth_state","minecraft:stone_bricks"))
    accent=cfg.get("entrance_accent_state",profile.get("trim_state","minecraft:spruce_planks"))
    for module_id,module in plan.modules.items():
        for port_id,port in module.ports.items():
            if port.side not in CARDINAL or (module_id,port_id) in connected:
                continue
            wp=world_port(placed[module_id].origin,port)
            direction=OUT[port.side]
            width=max(3,min(7,port.width))
            half=width//2
            for depth in range(1,4):
                center=_add(wp.pos,direction,depth)
                for lateral in range(-half,half+1):
                    if port.side in ("north","south"):
                        pos=(center[0]+lateral,wp.pos[1]-1,center[2])
                    else:
                        pos=(center[0],wp.pos[1]-1,center[2]+lateral)
                    _put(blocks,pos,pad_state,stats,"entrance_blocks")
            # Two restrained marker posts, not a decorative wall.
            for lateral in (-half,half):
                if port.side in ("north","south"):
                    base=(wp.pos[0]+lateral,wp.pos[1],wp.pos[2])
                else:
                    base=(wp.pos[0],wp.pos[1],wp.pos[2]+lateral)
                out=_add(base,direction,1)
                _put(blocks,out,accent,stats,"entrance_blocks")
                _put(blocks,(out[0],out[1]+1,out[2]),"minecraft:lantern[hanging=false,waterlogged=false]",stats,"lighting_blocks")
            stats["entrances"]=stats.get("entrances",0)+1

def _facade_lighting(plan,placed,blocks,stats,profile,cfg):
    exposed=exterior_sides(plan)
    spacing=max(8,int(cfg.get("light_spacing",12)))
    bracket=profile.get("trim_state","minecraft:spruce_planks")
    for module_id,sides in exposed.items():
        module=placed[module_id]
        for side in sides:
            length=_side_length(module,side)
            for along in range(spacing//2,length,spacing):
                base=_outside(module,side,along,2,1)
                lamp=(base[0],base[1]+1,base[2])
                if _put(blocks,base,bracket,stats,"lighting_blocks"):
                    _put(blocks,lamp,"minecraft:lantern[hanging=false,waterlogged=false]",stats,"lighting_blocks")

def _foundation_planting(plan,placed,blocks,stats,profile,cfg,rng):
    site=str(plan.site.get("character",profile.get("site_character","generic")))
    if site not in PLANTED_SITES:
        return
    leaf=cfg.get("plant_state","minecraft:oak_leaves[persistent=true,distance=1,waterlogged=false]")
    exposed=exterior_sides(plan)
    for module_id,sides in exposed.items():
        module=placed[module_id]
        for side in sides:
            length=_side_length(module,side)
            for along in range(5,length-4,10):
                if rng.random()>0.72:
                    continue
                p=_outside(module,side,along,0,2)
                for dy in (0,1):
                    _put(blocks,(p[0],p[1]+dy,p[2]),leaf,stats,"vegetation_blocks")

def _column_top(blocks,x,z,default_y):
    ys=[y for (bx,y,bz) in blocks if bx==x and bz==z]
    return max(ys) if ys else default_y

def _roof_finish(plan,placed,blocks,stats,profile,cfg):
    family=str(profile.get("family",""))
    for module_id,module in placed.items():
        ox,oy,oz=module.origin;w,h,d=module.size
        candidates=[
            (ox+max(2,min(w-3,w//4)),oz+max(2,min(d-3,d//4))),
            (ox+max(2,min(w-3,(w*3)//4)),oz+max(2,min(d-3,(d*3)//4))),
        ]
        if family in HISTORIC_FAMILIES:
            state=cfg.get("chimney_state",profile.get("pier_state","minecraft:stone_bricks"))
            for x,z in candidates[:1 if w*d<1800 else 2]:
                top=_column_top(blocks,x,z,oy+h)
                for y in range(top+1,top+4):
                    _put(blocks,(x,y,z),state,stats,"roof_detail_blocks")
        elif family in SERVICE_FAMILIES:
            state=cfg.get("vent_state","minecraft:iron_block")
            for x,z in candidates[:2]:
                top=_column_top(blocks,x,z,oy+h)
                _put(blocks,(x,top+1,z),state,stats,"roof_detail_blocks")
                _put(blocks,(x,top+2,z),"minecraft:iron_bars",stats,"roof_detail_blocks")

def _service_story(plan,placed,blocks,stats,profile,cfg,rng):
    family=str(profile.get("family",""))
    if family not in {"industrial","speculative"}:
        return
    exposed=exterior_sides(plan)
    for module_id,sides in exposed.items():
        module=placed[module_id]
        for side in sides:
            length=_side_length(module,side)
            if length<10 or rng.random()>0.75:
                continue
            along=min(length-4,max(3,length//3))
            p=_outside(module,side,along,0,2)
            _put(blocks,p,"minecraft:barrel[facing=up,open=false]",stats,"service_blocks")
            _put(blocks,(p[0]+(1 if side in ("north","south") else 0),p[1],p[2]+(1 if side in ("east","west") else 0)),
                 "minecraft:copper_block",stats,"service_blocks")

def apply_vanilla_finish(plan:ProjectPlan,placed:dict[str,PlacedModule],blocks:dict[Vec3,str],brief:dict[str,Any]):
    cfg=dict(brief.get("vanilla_finish",{}))
    if not cfg.get("enabled",False):
        return {"enabled":False,"status":"BASELINE","astra_microblocks":False}

    seed=int(cfg.get("seed",sum(ord(c) for c in str(brief.get("id","project")))+9009))
    rng=random.Random(seed)
    profile=plan.facade_profile
    stats={
        "enabled":True,
        "status":"VANILLA_DETAIL_COMPLETE",
        "seed":seed,
        "astra_microblocks":False,
        "entrances":0,
        "entrance_blocks":0,
        "lighting_blocks":0,
        "vegetation_blocks":0,
        "roof_detail_blocks":0,
        "service_blocks":0,
    }
    _entrance_finish(plan,placed,blocks,stats,profile,cfg)
    _facade_lighting(plan,placed,blocks,stats,profile,cfg)
    _foundation_planting(plan,placed,blocks,stats,profile,cfg,rng)
    _roof_finish(plan,placed,blocks,stats,profile,cfg)
    _service_story(plan,placed,blocks,stats,profile,cfg,rng)
    return stats
