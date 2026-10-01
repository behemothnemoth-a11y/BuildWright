#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT/"tools") not in sys.path:
    sys.path.insert(0,str(ROOT/"tools"))
from litematic_codec import read, unpack

DYE={
 "white":(230,232,230),"orange":(216,127,51),"magenta":(178,76,216),
 "light_blue":(102,153,216),"yellow":(229,229,51),"lime":(127,204,25),
 "pink":(242,127,165),"gray":(76,76,76),"light_gray":(153,153,153),
 "cyan":(76,127,153),"purple":(127,63,178),"blue":(51,76,178),
 "brown":(102,76,51),"green":(102,127,51),"red":(153,51,51),
 "black":(25,25,25),
}

def clamp(v): return max(0,min(255,int(v)))
def shade(c,f): return tuple(clamp(v*f) for v in c)
def state_name(entry):
    if isinstance(entry,dict): return str(entry.get("Name","minecraft:air"))
    return str(entry)

def block_color(state:str):
    n=state.split("[",1)[0].replace("minecraft:","")
    if n=="air": return None
    if "water" in n: return (54,105,170)
    if "lava" in n: return (230,90,25)
    if "sea_lantern" in n: return (190,225,215)
    if "glowstone" in n: return (205,160,85)
    if "glass" in n:
        for k,c in DYE.items():
            if n.startswith(k+"_") or ("_"+k+"_") in n: return shade(c,1.25)
        return (175,205,215)
    for k,c in DYE.items():
        if n.startswith(k+"_concrete") or n.startswith(k+"_terracotta") or n.startswith(k+"_wool"):
            return c
    if "prismarine" in n: return (70,135,125) if "dark_" not in n else (45,90,85)
    if "copper" in n:
        if "oxidized" in n: return (65,145,125)
        if "weathered" in n: return (80,135,105)
        if "exposed" in n: return (175,110,80)
        return (185,105,70)
    if "gold" in n: return (220,175,45)
    if "iron" in n: return (195,198,195)
    if "quartz" in n: return (225,220,205)
    if "calcite" in n: return (218,216,205)
    if "sandstone" in n: return (205,185,125) if "red_" not in n else (185,105,55)
    if "brick" in n and "stone" not in n and "tuff" not in n and "deepslate" not in n:
        return (145,75,60)
    if "deepslate" in n: return (65,67,70)
    if "blackstone" in n: return (45,42,48)
    if "tuff" in n: return (95,100,92)
    if "stone" in n or "andesite" in n: return (125,125,120)
    if "diorite" in n: return (190,190,185)
    if "granite" in n: return (150,105,90)
    if "cobblestone" in n: return (115,115,110)
    if "moss" in n or "leaves" in n or "vine" in n: return (70,120,58)
    if "grass" in n: return (90,145,62)
    if "podzol" in n: return (95,70,45)
    if "dirt" in n: return (115,80,55)
    if "gravel" in n: return (125,120,115)
    if "sand" in n: return (205,190,135)
    woods={
      "dark_oak":(70,48,30),"spruce":(95,65,40),"oak":(135,100,58),
      "birch":(190,170,110),"jungle":(150,105,65),"acacia":(155,80,55),
      "mangrove":(110,55,50),"bamboo":(170,165,70),"cherry":(205,145,145)
    }
    for k,c in woods.items():
        if k in n: return c
    if "obsidian" in n: return (40,28,55)
    if "amethyst" in n: return (135,90,180)
    if "redstone" in n: return (155,35,25)
    if "lantern" in n or "torch" in n: return (220,150,55)
    return (135,135,132)

def read_blocks(path:Path):
    root=read(path)
    blocks={}
    for region in root["Regions"].values():
        size=region["Size"]; w,h,d=size["x"],size["y"],size["z"]
        pos=region.get("Position",{"x":0,"y":0,"z":0})
        ox,oy,oz=pos.get("x",0),pos.get("y",0),pos.get("z",0)
        palette=[state_name(x) for x in region["BlockStatePalette"]]
        idx=unpack(region["BlockStates"],w*h*d,len(palette))
        i=0
        for y in range(h):
            for z in range(d):
                for x in range(w):
                    state=palette[idx[i]]; i+=1
                    if state!="minecraft:air":
                        blocks[(ox+x,oy+y,oz+z)]=state
    return blocks

def render_iso(blocks, output:Path, width=900, height=620, margin=28, background=(20,22,26), cutaway=False):
    if not blocks:
        raise ValueError("No non-air blocks to render")
    if cutaway:
        xs=[p[0] for p in blocks]; ys=[p[1] for p in blocks]; zs=[p[2] for p in blocks]
        max_x,max_y,max_z=max(xs),max(ys),max(zs)
        blocks={
            pos:state for pos,state in blocks.items()
            if not (
                pos[1]==max_y or
                (pos[0]==max_x and pos[1]>0) or
                (pos[2]==max_z and pos[1]>0)
            )
        }
    cells=set(blocks)
    visible=[]
    for pos,state in blocks.items():
        x,y,z=pos
        top=(x,y+1,z) not in cells
        east=(x+1,y,z) not in cells
        south=(x,y,z+1) not in cells
        if top or east or south:
            visible.append((pos,state,top,east,south))

    def projected_points(x,y,z):
        cx=(x-z)*2.0
        base=(x+z)-y*2.0
        top=[(cx,base-3.0),(cx+2.0,base-2.0),(cx,base-1.0),(cx-2.0,base-2.0)]
        east=[(cx+2.0,base-2.0),(cx+2.0,base),(cx,base+1.0),(cx,base-1.0)]
        south=[(cx-2.0,base-2.0),(cx,base-1.0),(cx,base+1.0),(cx-2.0,base)]
        return top,east,south

    xs=[];ys=[]
    for (x,y,z),_,top,east,south in visible:
        faces=projected_points(x,y,z)
        for enabled,face in zip((top,east,south),faces):
            if enabled:
                xs.extend(p[0] for p in face);ys.extend(p[1] for p in face)
    minx,maxx=min(xs),max(xs);miny,maxy=min(ys),max(ys)
    spanx=max(1.0,maxx-minx);spany=max(1.0,maxy-miny)
    scale=min((width-2*margin)/spanx,(height-2*margin)/spany)
    scale=max(1.0,scale)

    ss=2
    img=Image.new("RGB",(width*ss,height*ss),background)
    draw=ImageDraw.Draw(img)
    offset_x=(width-(spanx*scale))/2-minx*scale
    offset_y=(height-(spany*scale))/2-miny*scale
    def tx(face):
        return [((px*scale+offset_x)*ss,(py*scale+offset_y)*ss) for px,py in face]

    # Painter order: distant/lower geometry first.
    visible.sort(key=lambda item:(item[0][0]+item[0][2],item[0][1],item[0][0]))
    for (x,y,z),state,top,east,south in visible:
        color=block_color(state)
        if color is None: continue
        ftop,feast,fsouth=projected_points(x,y,z)
        outline=shade(color,0.42)
        if south:
            draw.polygon(tx(fsouth),fill=shade(color,0.72),outline=outline)
        if east:
            draw.polygon(tx(feast),fill=shade(color,0.58),outline=outline)
        if top:
            draw.polygon(tx(ftop),fill=shade(color,1.08),outline=outline)

    img=img.resize((width,height),Image.Resampling.LANCZOS)
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    img.save(output,optimize=True)
    return {"visible_blocks":len(visible),"total_blocks":len(blocks),"size":img.size}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("litematic",type=Path)
    ap.add_argument("output",type=Path)
    ap.add_argument("--width",type=int,default=900)
    ap.add_argument("--height",type=int,default=620)
    ap.add_argument("--cutaway",action="store_true")
    args=ap.parse_args()
    blocks=read_blocks(args.litematic)
    result=render_iso(blocks,args.output,args.width,args.height,cutaway=args.cutaway)
    print("ISO RENDER: PASS",result)

if __name__=="__main__":
    main()
