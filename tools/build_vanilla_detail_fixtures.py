#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT/"tools") not in sys.path:
    sys.path.insert(0,str(ROOT/"tools"))
from litematic_codec import make
from render_litematic_iso import read_blocks, render_iso

SRC=ROOT/"fixtures/sources/vanilla"
OUT=ROOT/"fixtures/compiled/vanilla"
PRE=ROOT/"fixtures/previews/vanilla"
REG=ROOT/"fixtures/registry.json"

def block(pos,state,role=None):
    d={"pos":list(pos),"state":state}
    if role:d["role"]=role
    return d

def fill(blocks,x0,y0,z0,x1,y1,z1,state,role=None):
    for y in range(y0,y1+1):
        for z in range(z0,z1+1):
            for x in range(x0,x1+1):
                blocks.append(block((x,y,z),state,role))

def fixture(fid,category,family,size,anchor,blocks,qa=None):
    return {
      "schema_version":1,"id":fid,"stage":"vanilla","category":category,"family":family,
      "size":list(size),"anchor":list(anchor),"blocks":blocks,
      "compiled":f"fixtures/compiled/vanilla/{fid}.litematic",
      "preview":f"fixtures/previews/vanilla/{fid}.png",
      "detail_fixture":True,
      "qa":qa or ["player_clearance","rotation_review","material_readability"]
    }

WOOD="minecraft:dark_oak_planks"
WOOD2="minecraft:spruce_planks"
STONE="minecraft:polished_andesite"
METAL="minecraft:iron_block"
ACCENT="minecraft:copper_block"
GLASS="minecraft:glass"
LIGHT="minecraft:lantern[hanging=false,waterlogged=false]"
CHAIN="minecraft:chain[axis=y,waterlogged=false]"
LEAF="minecraft:oak_leaves[persistent=true,distance=1,waterlogged=false]"
MOSS="minecraft:moss_block"

def table(fid,w,d,h=4):
    b=[]
    fill(b,0,h-1,0,w-1,h-1,d-1,WOOD,"furniture_wood")
    for x,z in ((0,0),(w-2,0),(0,d-2),(w-2,d-2)):
        fill(b,x,0,z,x+1,h-2,z+1,WOOD,"furniture_wood")
    return fixture(fid,"furniture","tables",(w,h,d),(w//2,0,d//2),b)

def chair(fid="dining_chair"):
    b=[]
    fill(b,0,0,0,2,1,2,WOOD,"furniture_wood")
    fill(b,0,2,0,2,2,2,WOOD2,"upholstery")
    fill(b,0,3,2,2,4,2,WOOD,"furniture_wood")
    return fixture(fid,"furniture","seating",(3,5,3),(1,0,1),b)

def cabinet(fid,w,h,d,family):
    b=[]
    fill(b,0,0,0,w-1,h-1,d-1,WOOD,"furniture_wood")
    if w>=5:
        fill(b,w//2,1,0,w//2,h-2,0,METAL,"metal")
    return fixture(fid,"furniture",family,(w,h,d),(w//2,0,d//2),b)

def lamp(fid,h,tabletop=False):
    b=[]
    fill(b,1,0,1,1,max(0,h-3),1,METAL,"metal")
    b.append(block((1,h-2,1),LIGHT,"light"))
    if not tabletop:
        fill(b,0,0,0,2,0,2,STONE,"stone")
    return fixture(fid,"decor","lighting",(3,h,3),(1,0,1),b)

def plant(fid,size=(3,5,3)):
    w,h,d=size;b=[]
    fill(b,w//2,0,d//2,w//2,1,d//2,"minecraft:flower_pot","pottery")
    for y in range(2,h):
        radius=1 if y<h-1 else 0
        for z in range(max(0,d//2-radius),min(d,d//2+radius+1)):
            for x in range(max(0,w//2-radius),min(w,w//2+radius+1)):
                b.append(block((x,y,z),LEAF,"plant"))
    return fixture(fid,"vegetation","indoor_plants",size,(w//2,0,d//2),b)

def build_defs():
    out=[]

    # Furniture: side pieces and room-filling sets.
    out.append(table("side_table_small",3,3,3))
    out.append(cabinet("nightstand",3,3,3,"bedroom"))
    out.append(cabinet("wardrobe_tall",5,7,3,"storage"))
    out.append(cabinet("dresser_low",7,4,3,"storage"))
    out.append(table("dining_table_long",13,5,4))
    out.append(chair())
    # Sofa
    b=[];fill(b,0,0,0,8,1,3,WOOD,"furniture_wood");fill(b,0,2,1,8,3,3,WOOD2,"upholstery");fill(b,0,2,3,8,4,3,WOOD,"furniture_wood")
    out.append(fixture("lounge_sofa","furniture","seating",(9,5,4),(4,0,2),b))
    b=[];fill(b,0,0,0,4,1,3,WOOD,"furniture_wood");fill(b,0,2,1,4,3,3,WOOD2,"upholstery");fill(b,0,2,3,4,4,3,WOOD,"furniture_wood")
    out.append(fixture("lounge_chair","furniture","seating",(5,5,4),(2,0,2),b))
    out.append(table("coffee_table",7,5,3))
    b=[];fill(b,0,0,0,8,3,2,WOOD,"furniture_wood");fill(b,0,3,0,8,3,2,STONE,"countertop")
    out.append(fixture("kitchen_counter","furniture","kitchen",(9,4,3),(4,0,1),b))
    b=[];fill(b,0,0,0,8,3,4,WOOD,"furniture_wood");fill(b,0,3,0,8,3,4,STONE,"countertop")
    out.append(fixture("kitchen_island","furniture","kitchen",(9,4,5),(4,0,2),b))
    b=[];fill(b,0,0,0,10,2,3,WOOD,"furniture_wood");fill(b,0,3,0,10,3,3,STONE,"work_surface");fill(b,0,4,3,10,4,3,WOOD,"furniture_wood")
    out.append(fixture("workshop_bench","furniture","workshop",(11,5,4),(5,0,2),b))
    b=[];fill(b,0,0,0,4,4,3,"minecraft:barrel[facing=north,open=false]","storage")
    out.append(fixture("storage_crates_stack","furniture","storage",(5,5,4),(2,0,2),b))
    b=[];fill(b,0,0,0,6,3,2,"minecraft:barrel[facing=north,open=false]","storage")
    out.append(fixture("barrel_rack","furniture","storage",(7,4,3),(3,0,1),b))
    out.append(table("tavern_table",7,7,4))
    b=[];fill(b,0,0,0,2,2,2,WOOD,"furniture_wood")
    out.append(fixture("stool","furniture","seating",(3,3,3),(1,0,1),b))

    # Decor and storytelling.
    b=[]
    for x in (1,5):
        fill(b,x,1,0,x,5,0,"minecraft:red_wool","textile")
        b.append(block((x,0,0),WOOD,"furniture_wood"))
    fill(b,0,6,0,6,6,0,WOOD,"furniture_wood")
    out.append(fixture("wall_banner_pair","decor","banners",(7,7,1),(3,0,0),b))
    b=[]
    for x0,w in ((0,3),(4,5)):
        fill(b,x0,1,0,x0+w-1,4,0,"minecraft:brown_wool","art")
        for x in range(x0,x0+w): b.append(block((x,0,0),WOOD,"furniture_wood"))
    out.append(fixture("painting_group","decor","art",(9,5,1),(4,0,0),b))
    b=[];fill(b,0,0,0,2,2,2,STONE,"stone");fill(b,1,3,1,1,5,1,ACCENT,"accent")
    out.append(fixture("trophy_pedestal","decor","displays",(3,6,3),(1,0,1),b))
    b=[];fill(b,0,0,0,4,0,2,"minecraft:bookshelf","books");b.append(block((1,1,1),"minecraft:red_carpet","textile"));b.append(block((3,1,1),"minecraft:blue_carpet","textile"))
    out.append(fixture("book_clutter_tabletop","decor","books",(5,2,3),(2,0,1),b))
    b=[];fill(b,0,0,0,1,1,1,"minecraft:flower_pot","pottery");fill(b,3,0,1,4,2,2,"minecraft:terracotta","pottery");fill(b,1,0,3,2,1,3,"minecraft:terracotta","pottery")
    out.append(fixture("pottery_cluster","decor","pottery",(5,3,4),(2,0,2),b))
    b=[];fill(b,0,0,0,6,0,4,"minecraft:red_carpet","textile")
    out.append(fixture("rug_small","decor","rugs",(7,1,5),(3,0,2),b))
    b=[];fill(b,0,0,0,12,0,8,"minecraft:blue_carpet","textile")
    out.append(fixture("rug_large","decor","rugs",(13,1,9),(6,0,4),b))
    b=[]
    for x,z in ((0,0),(2,0),(1,2),(3,2)):
        b.append(block((x,0,z),"minecraft:candle[candles=2,lit=true,waterlogged=false]","light"))
    out.append(fixture("candle_cluster","decor","lighting",(4,1,3),(2,0,1),b))

    # Lighting.
    b=[];fill(b,0,0,0,6,0,0,WOOD,"furniture_wood")
    for x in (1,5):
        b.append(block((x,2,0),LIGHT,"light"));b.append(block((x,3,0),CHAIN,"metal"))
    out.append(fixture("wall_sconce_pair","decor","lighting",(7,5,1),(3,0,0),b))
    b=[]
    for x in (0,4,8):
        b.append(block((x,0,1),LIGHT,"light"))
        for y in range(1,7):b.append(block((x,y,1),CHAIN,"metal"))
    out.append(fixture("hanging_lantern_row","decor","lighting",(9,7,3),(4,6,1),b))
    out.append(lamp("table_lamp_small",4,True))
    out.append(lamp("floor_lamp",7,False))
    b=[];fill(b,0,0,0,8,0,2,"minecraft:sea_lantern","light")
    out.append(fixture("recessed_light_strip","decor","lighting",(9,1,3),(4,0,1),b))

    # Vegetation and landscape.
    b=[]
    fill(b,0,0,0,6,1,6,MOSS,"ground")
    for x,z in ((1,1),(5,1),(2,4),(5,5)):
        fill(b,x,2,z,x,3,z,LEAF,"plant")
    out.append(fixture("shrub_cluster","vegetation","shrubs",(7,4,7),(3,0,3),b))
    b=[];fill(b,0,0,0,8,0,4,"minecraft:dirt","ground")
    flowers=["minecraft:poppy","minecraft:dandelion","minecraft:cornflower","minecraft:azure_bluet"]
    for x in range(1,8,2):
        for z in range(1,4,2):
            b.append(block((x,1,z),flowers[(x+z)%len(flowers)],"plant"))
    out.append(fixture("flower_bed","vegetation","flower_beds",(9,2,5),(4,0,2),b))
    out.append(plant("indoor_plant_small",(3,5,3)))
    b=[];fill(b,0,0,0,8,1,2,"minecraft:bricks","pottery")
    for x in range(1,8,2):
        b.append(block((x,2,1),LEAF,"plant"));b.append(block((x,3,1),LEAF,"plant"))
    out.append(fixture("planter_long","vegetation","planters",(9,4,3),(4,0,1),b))
    b=[]
    for y in range(0,8):
        b.append(block((0,y,0),"minecraft:vine[north=false,east=false,south=true,west=false,up=false]","plant"))
    out.append(fixture("vine_column","vegetation","vines",(1,8,1),(0,0,0),b))

    # Service / mechanical.
    b=[]
    for y in (0,3,6):fill(b,0,y,0,8,y,2,METAL,"metal")
    for x in (0,4,8):fill(b,x,0,0,x,6,2,METAL,"metal")
    out.append(fixture("utility_shelving","mechanical","storage",(9,7,3),(4,0,1),b))
    b=[];fill(b,0,0,0,8,5,0,WOOD,"furniture_wood")
    for x,y in ((1,1),(3,3),(5,2),(7,4)):b.append(block((x,y,1),ACCENT,"tool"))
    out.append(fixture("tool_wall","mechanical","tools",(9,6,2),(4,0,0),b))
    b=[];fill(b,0,2,1,6,2,1,ACCENT,"metal");fill(b,3,0,1,3,5,1,ACCENT,"metal")
    for x in (1,5):b.append(block((x,2,0),"minecraft:polished_blackstone_button[face=wall,facing=south,powered=false]","control"))
    out.append(fixture("pipe_valve_bank","mechanical","pipes",(7,6,3),(3,0,1),b))
    b=[];fill(b,0,0,0,6,0,4,WOOD,"furniture_wood");fill(b,0,1,0,2,2,2,"minecraft:barrel[facing=north,open=false]","storage");fill(b,4,1,2,6,2,4,"minecraft:barrel[facing=north,open=false]","storage")
    out.append(fixture("crate_pallet","mechanical","storage",(7,3,5),(3,0,2),b))
    b=[]
    for y in range(0,7):b.append(block((1,y,1),CHAIN,"metal"))
    b.append(block((1,0,1),"minecraft:redstone_lamp[lit=true]","light"))
    out.append(fixture("cable_drop","mechanical","cables",(3,7,3),(1,6,1),b))

    # Secondary architecture.
    b=[];fill(b,0,0,0,10,3,0,WOOD,"furniture_wood");fill(b,0,4,0,10,4,0,STONE,"stone")
    out.append(fixture("wainscot_bay","architecture","wall_paneling",(11,5,1),(5,0,0),b))
    b=[];fill(b,0,0,0,10,7,0,STONE,"stone")
    for x in (0,5,10):fill(b,x,0,1,x,7,1,WOOD,"furniture_wood")
    for y in (0,4,7):fill(b,0,y,1,10,y,1,WOOD,"furniture_wood")
    out.append(fixture("wall_panel_bay","architecture","wall_paneling",(11,8,2),(5,0,0),b))
    b=[];fill(b,0,0,0,10,0,10,WOOD,"furniture_wood")
    for i in range(0,11,5):fill(b,i,1,0,i,1,10,WOOD2,"furniture_wood")
    out.append(fixture("ceiling_beam_bay","architecture","ceilings",(11,2,11),(5,1,5),b))
    b=[]
    fill(b,0,0,0,1,8,0,STONE,"stone");fill(b,5,0,0,6,8,0,STONE,"stone");fill(b,0,7,0,6,8,0,STONE,"stone")
    fill(b,0,0,1,0,8,1,WOOD,"furniture_wood");fill(b,6,0,1,6,8,1,WOOD,"furniture_wood")
    out.append(fixture("doorway_trim_simple","architecture","door_surrounds",(7,9,2),(3,0,0),b))
    b=[];fill(b,0,0,0,8,2,2,WOOD,"furniture_wood");fill(b,1,3,1,7,3,2,WOOD2,"upholstery")
    out.append(fixture("window_seat_bay","architecture","interior_bays",(9,4,3),(4,0,1),b))
    b=[];fill(b,0,0,0,10,0,0,STONE,"stone");fill(b,0,1,0,10,1,0,WOOD,"furniture_wood")
    out.append(fixture("picture_rail_bay","architecture","trim",(11,2,1),(5,0,0),b))
    return out

def write_lf(path:Path,text:str):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes((text.rstrip()+"\n").encode("utf-8"))

def main():
    SRC.mkdir(parents=True,exist_ok=True)
    OUT.mkdir(parents=True,exist_ok=True)
    PRE.mkdir(parents=True,exist_ok=True)
    defs=build_defs()
    ids={d["id"] for d in defs}

    for d in defs:
        src=SRC/f"{d['id']}.json"
        write_lf(src,json.dumps(d,indent=2))
        block_map={tuple(x["pos"]):x["state"] for x in d["blocks"]}
        lit=OUT/f"{d['id']}.litematic"
        make(
            lit,
            "BuildWright "+d["id"].replace("_"," ").title(),
            tuple(d["size"]),
            block_map,
            desc=f"BuildWright vanilla detail fixture: {d['category']}/{d['family']}"
        )
        render_iso(read_blocks(lit),PRE/f"{d['id']}.png",width=700,height=520)

    registry=json.loads(REG.read_text(encoding="utf-8"))
    kept=[x for x in registry["fixtures"] if x["id"] not in ids]
    added=[]
    for d in defs:
        lit=OUT/f"{d['id']}.litematic"
        block_map={tuple(x["pos"]):x["state"] for x in d["blocks"]}
        added.append({
          "id":d["id"],
          "stage":"vanilla",
          "category":d["category"],
          "family":d["family"],
          "size":d["size"],
          "blocks":len(block_map),
          "file":d["compiled"],
          "sha256":hashlib.sha256(lit.read_bytes()).hexdigest(),
          "source":str((SRC/f"{d['id']}.json").relative_to(ROOT)).replace("\\","/"),
          "preview":d["preview"],
          "detail_fixture":True
        })

    registry["fixtures"]=kept+added
    registry.setdefault("counts",{})["vanilla"]=sum(1 for x in registry["fixtures"] if x["stage"]=="vanilla")
    registry["counts"]["microblock"]=sum(1 for x in registry["fixtures"] if x["stage"]=="microblock")
    registry["counts"]["detail_vanilla"]=len(added)
    write_lf(REG,json.dumps(registry,indent=2))
    print("VANILLA DETAIL FIXTURES: WROTE",{"new":len(added),"vanilla_total":registry["counts"]["vanilla"]})

if __name__=="__main__":
    main()
