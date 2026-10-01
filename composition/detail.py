from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

from .transforms import transform_fixture_blocks, transform_pos

ROLE_BY_TEMPLATE = {
    "bedroom_suite": "bedroom",
    "formal_dining": "dining",
    "gallery_corridor": "gallery",
    "garden_courtyard": "garden",
    "grand_hall": "hall",
    "industrial_lab": "industrial",
    "library": "library",
    "operations_bay": "industrial",
    "tavern_common_room": "tavern",
    "workshop": "workshop",
}

DEFAULT_STATES = {
    "trim": "minecraft:dark_oak_slab[type=bottom,waterlogged=false]",
    "crown": "minecraft:dark_oak_planks",
    "beam_x": "minecraft:dark_oak_log[axis=x]",
    "beam_z": "minecraft:dark_oak_log[axis=z]",
    "floor_accent": "minecraft:red_carpet",
}

def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def _detail_data(root: Path) -> dict[str, Any]:
    return _load_json(root / "composition" / "detail_profiles.json")

def _keepout_cells(keepouts) -> set[tuple[int,int,int]]:
    out=set()
    for box in keepouts:
        out.update(box.cells())
    return out

def _soft_state(state: str) -> bool:
    return "carpet" in state

def _resolve_axis(value, length: int, axis: str) -> int:
    if isinstance(value, int):
        return value
    value=str(value)
    if axis=="y":
        if value=="floor": return 1
        if value=="wall": return 2
        if value=="ceiling": return max(1,length-2)
        if value=="center": return length//2
        return int(value)
    lookup={
        "left":2,"front":2,
        "q1":max(3,length//4),
        "center":length//2,
        "q3":min(length-4,(length*3)//4),
        "right":max(2,length-3),"back":max(2,length-3),
    }
    return lookup.get(value,length//2)

class DetailWriter:
    def __init__(self, blocks, room_size, palette, keepouts):
        self.blocks=blocks
        self.size=tuple(room_size)
        self.palette=palette
        self.keepouts=set(keepouts)
        self.stats={
            "surface_blocks":0,
            "fixtures_attempted":0,
            "fixtures_placed":0,
            "fixtures_skipped":0,
            "fixture_ids":[],
        }

    def in_bounds(self,pos):
        x,y,z=pos;w,h,d=self.size
        return 0<=x<w and 0<=y<h and 0<=z<d

    def can_write(self,pos,new_state,allow_soft_replace=False):
        if not self.in_bounds(pos) or pos in self.keepouts:
            return False
        if pos not in self.blocks:
            return True
        if allow_soft_replace and _soft_state(self.blocks[pos]) and not _soft_state(new_state):
            return True
        return False

    def put_surface(self,pos,state):
        state=self.palette.remap(state)
        if self.can_write(pos,state):
            self.blocks[pos]=state
            self.stats["surface_blocks"]+=1
            return True
        return False

    def place_fixture(self, source, target, rotation=0, mirror="none"):
        self.stats["fixtures_attempted"]+=1
        if source.get("stage")!="vanilla":
            raise ValueError(f"Detail pass may only place vanilla fixtures: {source.get('id')}")
        size=tuple(source["size"])
        anchor=transform_pos(tuple(source.get("anchor",[0,0,0])),size,rotation,mirror)
        transformed=transform_fixture_blocks(source["blocks"],size,rotation,mirror)
        origin=tuple(int(target[i])-int(anchor[i]) for i in range(3))
        cells=[]
        for item in transformed:
            x,y,z=item["pos"]
            pos=(origin[0]+x,origin[1]+y,origin[2]+z)
            state=self.palette.remap(item["state"])
            cells.append((pos,state))
        for pos,state in cells:
            if not self.can_write(pos,state,allow_soft_replace=True):
                self.stats["fixtures_skipped"]+=1
                return False
        for pos,state in cells:
            self.blocks[pos]=state
        self.stats["fixtures_placed"]+=1
        self.stats["fixture_ids"].append(source["id"])
        return True


def _surface_pass(writer: DetailWriter, config: dict[str,Any], states: dict[str,str], density: float, rng: random.Random):
    w,h,d=writer.size
    surfaces=config.get("surfaces",{})

    if surfaces.get("perimeter_trim") and w>=7 and d>=7 and rng.random()<=density:
        for x in range(2,w-2):
            writer.put_surface((x,1,1),states["trim"])
            writer.put_surface((x,1,d-2),states["trim"])
        for z in range(2,d-2):
            writer.put_surface((1,1,z),states["trim"])
            writer.put_surface((w-2,1,z),states["trim"])

    if surfaces.get("crown_trim") and h>=7 and rng.random()<=density:
        y=h-2
        for x in range(2,w-2):
            writer.put_surface((x,y,1),states["crown"])
            writer.put_surface((x,y,d-2),states["crown"])
        for z in range(2,d-2):
            writer.put_surface((1,y,z),states["crown"])
            writer.put_surface((w-2,y,z),states["crown"])

    if surfaces.get("ceiling_beams") and h>=8 and w>=11 and d>=11 and rng.random()<=density:
        y=h-2
        # Prefer the short span so the room does not become a barcode ceiling.
        if w>=d:
            for z in range(5,d-4,max(8,d//4 or 8)):
                for x in range(2,w-2):
                    writer.put_surface((x,y,z),states["beam_x"])
        else:
            for x in range(5,w-4,max(8,w//4 or 8)):
                for z in range(2,d-2):
                    writer.put_surface((x,y,z),states["beam_z"])

    if surfaces.get("floor_inlay") and w>=11 and d>=11 and rng.random()<=density:
        y=1
        if w>=d:
            z=d//2
            for x in range(3,w-3):
                writer.put_surface((x,y,z),states["floor_accent"])
        else:
            x=w//2
            for z in range(3,d-3):
                writer.put_surface((x,y,z),states["floor_accent"])

def _fixture_source(root: Path, fixture_id: str, cache: dict[str,dict]) -> dict:
    if fixture_id in cache:
        return cache[fixture_id]
    path=root/"fixtures"/"sources"/"vanilla"/f"{fixture_id}.json"
    if not path.is_file():
        raise FileNotFoundError(f"Vanilla detail fixture not found: {fixture_id}")
    cache[fixture_id]=_load_json(path)
    return cache[fixture_id]

def _candidate_offsets(rng: random.Random):
    # Expand outward from the requested design zone. This keeps intent first,
    # but lets detail furniture find a nearby free pocket in already-furnished rooms.
    out=[(0,0,0)]
    for radius in (2,4,6,8,10):
        ring=[
            ( radius,0,0),(-radius,0,0),(0,0, radius),(0,0,-radius),
            ( radius,0, radius),(-radius,0, radius),( radius,0,-radius),(-radius,0,-radius),
        ]
        rng.shuffle(ring)
        out.extend(ring)
    return out

def apply_vanilla_detail(root: Path, blocks, plan, palette, brief: dict[str,Any]):
    detail_cfg=dict(brief.get("vanilla_detail",{}))
    if not detail_cfg.get("enabled",False):
        return {
            "enabled":False,
            "status":"BASELINE",
            "role":ROLE_BY_TEMPLATE.get(plan.template_id,"default"),
            "surface_blocks":0,
            "fixtures_attempted":0,
            "fixtures_placed":0,
            "fixtures_skipped":0,
            "fixture_ids":[],
        }

    if brief.get("stage","vanilla")!="vanilla":
        raise ValueError("VANILLA_DETAIL_COMPLETE may only be generated from vanilla composition briefs")

    data=_detail_data(root)
    role=str(detail_cfg.get("role") or ROLE_BY_TEMPLATE.get(plan.template_id,"default"))
    profile=dict(data["profiles"].get(role,data["profiles"]["default"]))
    style_slug=(plan.style_profile or "").split(".")[-1]
    override=dict(data.get("style_overrides",{}).get(style_slug,{}))

    density=float(detail_cfg.get("density",profile.get("density",0.75)))
    density*=float(override.get("density_multiplier",1.0))
    density=max(0.0,min(1.0,density))
    seed=int(detail_cfg.get("seed",plan.seed+9009))
    rng=random.Random(seed)

    states=dict(DEFAULT_STATES)
    states.update(detail_cfg.get("states",{}))
    surfaces=dict(profile.get("surfaces",{}))
    for name in override.get("disable_surfaces",[]):
        surfaces[name]=False
    profile["surfaces"]=surfaces

    keepouts=_keepout_cells(plan.keepouts)
    writer=DetailWriter(blocks,plan.room_size,palette,keepouts)
    _surface_pass(writer,profile,states,density,rng)

    w,h,d=plan.room_size
    source_cache={}
    for recipe in profile.get("recipes",[]):
        probability=float(recipe.get("probability",1.0))*density
        if rng.random()>min(1.0,probability):
            continue
        fixture_id=str(recipe["fixture"])
        source=_fixture_source(root,fixture_id,source_cache)
        x=_resolve_axis(recipe.get("x","center"),w,"x")
        y=_resolve_axis(recipe.get("y","floor"),h,"y")
        z=_resolve_axis(recipe.get("z","center"),d,"z")
        offset=recipe.get("offset",[0,0,0])
        base_target=(x+int(offset[0]),y+int(offset[1]),z+int(offset[2]))
        rotation=int(recipe.get("rotation",0))%4
        mirror=str(recipe.get("mirror","none"))

        placed=False
        for dx,dy,dz in _candidate_offsets(rng):
            target=(base_target[0]+dx,base_target[1]+dy,base_target[2]+dz)
            if writer.place_fixture(source,target,rotation,mirror):
                placed=True
                break
        if not placed:
            # place_fixture already records the failed attempts; one recipe is allowed
            # to disappear rather than forcing geometry through circulation.
            continue

    result=dict(writer.stats)
    result.update({
        "enabled":True,
        "status":"VANILLA_DETAIL_COMPLETE",
        "role":role,
        "density":round(density,4),
        "seed":seed,
        "style_profile":plan.style_profile,
        "astra_microblocks":False,
    })
    return result
