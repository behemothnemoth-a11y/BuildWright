from __future__ import annotations
from typing import Any

from .model import ProjectPlan
from .solver import PlacedModule

Vec3=tuple[int,int,int]

def _put(blocks,pos,state,stats):
    if pos in blocks:return False
    blocks[pos]=state;stats["blocks"]+=1
    return True

def _side_length(m:PlacedModule,side:str):
    return m.size[0] if side in ("north","south") else m.size[2]

def _outside(m:PlacedModule,side:str,along:int,y:int,depth:int=1):
    ox,oy,oz=m.origin;w,h,d=m.size
    if side=="north":return (ox+along,oy+y,oz-depth)
    if side=="south":return (ox+along,oy+y,oz+d-1+depth)
    if side=="west":return (ox-depth,oy+y,oz+along)
    if side=="east":return (ox+w-1+depth,oy+y,oz+along)
    raise ValueError(f"Structural side must be cardinal: {side}")

def _buttress_run(node,m,blocks,stats,profile):
    side=str(node.get("side","south"))
    spacing=max(4,int(node.get("spacing",8)))
    depth=max(1,int(node.get("depth",2)))
    width=max(1,int(node.get("width",2)))
    height=max(3,int(node.get("height",max(3,m.size[1]-2))))
    state=node.get("state",profile.get("pier_state","minecraft:stone_bricks"))
    length=_side_length(m,side)
    positions=list(range(1,length-1,spacing))
    for along in positions:
        for y in range(height):
            step_depth=max(1,depth-(y*depth)//max(1,height))
            for lateral in range(-(width//2),-(width//2)+width):
                for dep in range(1,step_depth+1):
                    if side in ("north","south"):
                        p=_outside(m,side,along+lateral,y,dep)
                    else:
                        p=_outside(m,side,along+lateral,y,dep)
                    _put(blocks,p,state,stats)
    return len(positions)

def _porch(node,m,blocks,stats,profile):
    side=str(node.get("side","south"))
    length=_side_length(m,side)
    center=int(node.get("center",length//2))
    width=max(3,int(node.get("width",7)))
    depth=max(2,int(node.get("depth",4)))
    height=max(3,int(node.get("height",5)))
    floor=node.get("floor_state",profile.get("plinth_state","minecraft:stone_bricks"))
    structure=node.get("structure_state",profile.get("pier_state","minecraft:stone_bricks"))
    roof=node.get("roof_state",profile.get("roof_state","minecraft:dark_oak_planks"))
    half=width//2
    # Platform.
    for along in range(center-half,center-half+width):
        for dep in range(1,depth+1):
            _put(blocks,_outside(m,side,along,0,dep),floor,stats)
    # Outer columns.
    for along in (center-half,center-half+width-1):
        for y in range(1,height+1):
            _put(blocks,_outside(m,side,along,y,depth),structure,stats)
    # Quiet canopy plane.
    for along in range(center-half-1,center-half+width+1):
        for dep in range(1,depth+2):
            _put(blocks,_outside(m,side,along,height+1,dep),roof,stats)
    return 1

def _balcony(node,m,blocks,stats,profile):
    side=str(node.get("side","south"))
    length=_side_length(m,side)
    center=int(node.get("center",length//2))
    width=max(3,int(node.get("width",7)))
    depth=max(2,int(node.get("depth",3)))
    y=int(node.get("y",max(3,m.size[1]//2)))
    floor=node.get("floor_state",profile.get("trim_state","minecraft:spruce_planks"))
    rail=node.get("rail_state","minecraft:iron_bars")
    half=width//2
    for along in range(center-half,center-half+width):
        for dep in range(1,depth+1):
            _put(blocks,_outside(m,side,along,y,dep),floor,stats)
    for along in range(center-half,center-half+width):
        p=_outside(m,side,along,y+1,depth)
        _put(blocks,p,rail,stats)
    for dep in range(1,depth+1):
        for along in (center-half,center-half+width-1):
            _put(blocks,_outside(m,side,along,y+1,dep),rail,stats)
    return 1

def _tower(node,m,blocks,stats,profile):
    corner=str(node.get("corner","nw")).lower()
    tw=max(5,int(node.get("width",9)));td=max(5,int(node.get("depth",9)))
    th=max(m.size[1]+3,int(node.get("height",m.size[1]+8)))
    ox,oy,oz=m.origin;w,h,d=m.size
    if corner=="nw":tx,tz=ox-tw+1,oz-td+1
    elif corner=="ne":tx,tz=ox+w-1,oz-td+1
    elif corner=="sw":tx,tz=ox-tw+1,oz+d-1
    elif corner=="se":tx,tz=ox+w-1,oz+d-1
    else:raise ValueError(f"Unknown tower corner: {corner}")
    wall=node.get("wall_state",profile.get("wall_state","minecraft:stone_bricks"))
    trim=node.get("trim_state",profile.get("pier_state","minecraft:polished_andesite"))
    glass=node.get("glass_state",profile.get("glass_state","minecraft:glass"))
    roof=node.get("roof_state",profile.get("roof_state","minecraft:dark_oak_planks"))
    for y in range(th):
        for z in range(td):
            for x in range(tw):
                edge=x in (0,tw-1) or z in (0,td-1)
                if edge:_put(blocks,(tx+x,oy+y,tz+z),wall,stats)
    # Corners read as structural shafts.
    for x,z in ((0,0),(tw-1,0),(0,td-1),(tw-1,td-1)):
        for y in range(th):blocks.setdefault((tx+x,oy+y,tz+z),trim)
    # Sparse windows on outward faces.
    for y in range(4,th-3,5):
        for x,z in ((tw//2,0),(tw//2,td-1),(0,td//2),(tw-1,td//2)):
            blocks[(tx+x,oy+y,tz+z)]=glass
    # Roof cap; intentionally simple enough to accept a future style-specific roof node.
    for z in range(-1,td+1):
        for x in range(-1,tw+1):
            _put(blocks,(tx+x,oy+th,tz+z),roof,stats)
    return 1

def _dormer_row(node,m,blocks,stats,profile):
    side=str(node.get("side","south"))
    if side not in ("north","south"):raise ValueError("Dormer rows currently target north/south roof faces")
    count=max(1,int(node.get("count",2)))
    width=max(3,int(node.get("width",3)))
    depth=max(2,int(node.get("depth",3)))
    height=max(2,int(node.get("height",3)))
    wall=node.get("wall_state",profile.get("wall_state","minecraft:stone_bricks"))
    glass=node.get("glass_state",profile.get("glass_state","minecraft:glass"))
    roof=node.get("roof_state",profile.get("roof_state","minecraft:dark_oak_planks"))
    ox,oy,oz=m.origin;mw,mh,md=m.size
    top=oy+mh
    centers=[round((i+1)*mw/(count+1)) for i in range(count)]
    for center in centers:
        start=max(1,center-width//2)
        z0=oz-1 if side=="north" else oz+md-depth
        for x in range(start,min(mw-1,start+width)):
            wx=ox+x
            for zoff in range(depth):
                wz=z0+(-zoff if side=="north" else zoff)
                _put(blocks,(wx,top,wz),wall,stats)
                _put(blocks,(wx,top+height,wz),roof,stats)
        face_z=z0+(-depth+1 if side=="north" else depth-1)
        blocks[(ox+center,top+1,face_z)]=glass
    return len(centers)

def apply_structures(plan:ProjectPlan,placed:dict[str,PlacedModule],blocks:dict[Vec3,str],brief:dict[str,Any]):
    stats={"nodes":0,"blocks":0,"by_type":{}}
    profile=plan.facade_profile
    for node in plan.structures:
        kind=str(node.get("type","")).lower()
        module_id=str(node.get("module",""))
        if module_id not in placed:raise KeyError(f"Structural node references unknown module: {module_id}")
        m=placed[module_id]
        if kind=="buttress_run":count=_buttress_run(node,m,blocks,stats,profile)
        elif kind=="porch":count=_porch(node,m,blocks,stats,profile)
        elif kind=="balcony":count=_balcony(node,m,blocks,stats,profile)
        elif kind=="tower":count=_tower(node,m,blocks,stats,profile)
        elif kind=="dormer_row":count=_dormer_row(node,m,blocks,stats,profile)
        else:raise ValueError(f"Unknown structural node type: {kind}")
        stats["nodes"]+=1
        stats["by_type"][kind]=stats["by_type"].get(kind,0)+count
    return stats
