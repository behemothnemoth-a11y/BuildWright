from __future__ import annotations
from typing import Any

from .model import ProjectPlan
from .solver import PlacedModule

Vec3=tuple[int,int,int]

def _put(blocks,pos,state,stats):
    if pos in blocks:return False
    blocks[pos]=state;stats["blocks"]+=1
    return True

def _perimeter_points(m:PlacedModule):
    x0,y0,z0,x1,y1,z1=m.box
    pts=set()
    for x in range(x0,x1+1):
        pts.add((x,z0));pts.add((x,z1))
    for z in range(z0,z1+1):
        pts.add((x0,z));pts.add((x1,z))
    return pts

def _pier_points(m:PlacedModule,spacing:int):
    x0,y0,z0,x1,y1,z1=m.box
    pts={(x0,z0),(x1,z0),(x0,z1),(x1,z1)}
    for x in range(x0,x1+1,spacing):
        pts.add((x,z0));pts.add((x,z1))
    for z in range(z0,z1+1,spacing):
        pts.add((x0,z));pts.add((x1,z))
    return pts

def apply_foundations(plan:ProjectPlan,placed:dict[str,PlacedModule],blocks:dict[Vec3,str],brief:dict[str,Any]):
    cfg=dict(plan.site.get("foundation",{}))
    cfg.update(brief.get("foundation",{}))
    if not cfg.get("enabled",False):
        return {"enabled":False,"blocks":0,"modules":0,"mode":cfg.get("mode","perimeter")}
    ground_y=int(cfg.get("ground_y",plan.site.get("ground_y",min(p.origin[1] for p in placed.values())-1)))
    state=cfg.get("state",plan.facade_profile.get("plinth_state","minecraft:stone_bricks"))
    mode=str(cfg.get("mode","perimeter"))
    spacing=max(3,int(cfg.get("pier_spacing",7)))
    stats={"enabled":True,"blocks":0,"modules":0,"mode":mode,"ground_y":ground_y,"max_drop":0}
    for m in placed.values():
        base_y=m.origin[1]
        if base_y<=ground_y+1:continue
        drop=base_y-ground_y-1
        stats["max_drop"]=max(stats["max_drop"],drop)
        if mode=="solid":
            x0,y0,z0,x1,y1,z1=m.box
            pts={(x,z) for x in range(x0,x1+1) for z in range(z0,z1+1)}
        elif mode=="piers":
            pts=_pier_points(m,spacing)
        elif mode=="perimeter":
            pts=_perimeter_points(m)
        else:
            raise ValueError(f"Unknown foundation mode: {mode}")
        for x,z in pts:
            for y in range(ground_y+1,base_y):
                _put(blocks,(x,y,z),state,stats)
        stats["modules"]+=1
    return stats
