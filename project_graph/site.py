from __future__ import annotations

from .model import ProjectPlan
from .solver import PlacedModule, project_bounds

Vec3 = tuple[int, int, int]

CHARACTER_DEFAULTS = {
    "formal": ("minecraft:grass_block", "minecraft:stone_bricks"),
    "courtyard": ("minecraft:smooth_sandstone", "minecraft:cut_sandstone"),
    "garden": ("minecraft:moss_block", "minecraft:gravel"),
    "integrated_landscape": ("minecraft:grass_block", "minecraft:smooth_stone"),
    "lush_integrated": ("minecraft:moss_block", "minecraft:stone_bricks"),
    "forest": ("minecraft:podzol", "minecraft:gravel"),
    "cold_temperate": ("minecraft:grass_block", "minecraft:stone"),
    "mountain": ("minecraft:stone", "minecraft:gravel"),
    "farm": ("minecraft:grass_block", "minecraft:dirt_path"),
    "dusty_street": ("minecraft:coarse_dirt", "minecraft:gravel"),
    "desert": ("minecraft:sand", "minecraft:sandstone"),
    "dense_urban": ("minecraft:gray_concrete", "minecraft:smooth_stone"),
    "hardscape": ("minecraft:stone", "minecraft:polished_andesite"),
    "service_yard": ("minecraft:stone", "minecraft:gray_concrete"),
    "platform": ("minecraft:smooth_stone", "minecraft:iron_block"),
    "temple_garden": ("minecraft:grass_block", "minecraft:stone_bricks"),
    "monumental": ("minecraft:stone", "minecraft:polished_andesite"),
    "overgrown": ("minecraft:moss_block", "minecraft:mossy_cobblestone"),
    "submerged": ("minecraft:prismarine", "minecraft:dark_prismarine"),
    "minimal": ("minecraft:grass_block", "minecraft:smooth_quartz"),
    "generic": ("minecraft:grass_block", "minecraft:gravel"),
}

def _line_points(a, b):
    x, z = a
    tx, tz = b
    while x != tx:
        yield x, z
        x += 1 if tx > x else -1
    while z != tz:
        yield x, z
        z += 1 if tz > z else -1
    yield x, z

def _polyline(points):
    out=[]
    for i in range(len(points)-1):
        segment=list(_line_points(tuple(points[i]),tuple(points[i+1])))
        if i:segment=segment[1:]
        out.extend(segment)
    return out

def _edge_feature_state(character: str):
    if character in {"formal", "garden", "lush_integrated", "temple_garden"}:
        return "minecraft:oak_leaves"
    if character in {"courtyard", "monumental"}:
        return "minecraft:stone_bricks"
    if character in {"dense_urban", "hardscape", "service_yard", "platform"}:
        return "minecraft:polished_andesite"
    if character in {"desert", "dusty_street"}:
        return "minecraft:sandstone"
    if character in {"submerged"}:
        return "minecraft:dark_prismarine"
    return None

def _surface_route(blocks,centers,y,width,state):
    half=width//2;count=0
    for x,z in centers:
        for dx in range(-half,-half+width):
            for dz in range(-half,-half+width):
                pos=(x+dx,y,z+dz)
                if blocks.get(pos)!=state:
                    blocks[pos]=state;count+=1
    return count

def _wall_route(blocks,centers,base_y,height,state):
    count=0
    for x,z in centers:
        for y in range(base_y,base_y+height):
            pos=(x,y,z)
            if blocks.get(pos)!=state:
                blocks[pos]=state;count+=1
    return count

def _network_stairs(blocks,node):
    start=tuple(int(v) for v in node["from"])
    end=tuple(int(v) for v in node["to"])
    sx,sy,sz=start;ex,ey,ez=end
    if sx!=ex and sz!=ez:
        raise ValueError("Site stairs require cardinally aligned endpoints")
    dx=0 if sx==ex else (1 if ex>sx else -1)
    dz=0 if sz==ez else (1 if ez>sz else -1)
    dist=abs(ex-sx)+abs(ez-sz);rise=ey-sy
    if dist<abs(rise):raise ValueError("Site stair run is shorter than elevation change")
    width=max(1,int(node.get("width",3)));half=width//2
    stair=node.get("state","minecraft:stone_brick_stairs")
    landing=node.get("landing_state","minecraft:stone_bricks")
    facing={(1,0):"east",(-1,0):"west",(0,1):"south",(0,-1):"north"}.get((dx,dz),"north")
    opposite={"east":"west","west":"east","north":"south","south":"north"}
    if rise<0:facing=opposite[facing]
    lateral=((0,1) if dx else (1,0));count=0
    for i in range(dist+1):
        x=sx+dx*i;z=sz+dz*i
        y=sy if dist==0 else sy+round(rise*i/dist)
        ny=y if i==dist else (sy+round(rise*(i+1)/dist))
        state=(f"{stair}[facing={facing},half=bottom,shape=straight,waterlogged=false]" if ny!=y else landing)
        for off in range(-half,-half+width):
            pos=(x+lateral[0]*off,y,z+lateral[1]*off)
            blocks[pos]=state;count+=1
    return count

def _apply_networks(blocks,cfg,ground_y,default_path):
    stats={"road_blocks":0,"plaza_blocks":0,"wall_blocks":0,"fence_blocks":0,"retaining_blocks":0,"stair_blocks":0}
    for node in cfg.get("networks",[]):
        kind=str(node.get("type","path")).lower()
        if kind in {"path","road"}:
            points=node.get("points")
            if not points:
                points=[node["from"],node["to"]]
            centers=_polyline([(int(p[0]),int(p[-1])) for p in points])
            width=max(1,int(node.get("width",5 if kind=="road" else 3)))
            state=node.get("state",default_path)
            count=_surface_route(blocks,centers,int(node.get("y",ground_y)),width,state)
            stats["road_blocks"]+=count
        elif kind=="plaza":
            center=node.get("center",[0,0]);size=node.get("size",[11,11])
            cx,cz=int(center[0]),int(center[-1]);w,d=max(1,int(size[0])),max(1,int(size[-1]))
            state=node.get("state",default_path);y=int(node.get("y",ground_y))
            centers=[(x,z) for x in range(cx-w//2,cx-w//2+w) for z in range(cz-d//2,cz-d//2+d)]
            count=0
            for x,z in centers:
                if blocks.get((x,y,z))!=state:blocks[(x,y,z)]=state;count+=1
            stats["plaza_blocks"]+=count
        elif kind in {"wall","fence","retaining_wall"}:
            points=node.get("points") or [node["from"],node["to"]]
            centers=_polyline([(int(p[0]),int(p[-1])) for p in points])
            state=node.get("state","minecraft:stone_bricks" if kind!="fence" else "minecraft:oak_fence")
            if kind=="retaining_wall":
                base=int(node.get("base_y",ground_y+1));top=int(node.get("top_y",base+3));height=max(1,top-base+1)
                count=_wall_route(blocks,centers,base,height,state);stats["retaining_blocks"]+=count
            else:
                base=int(node.get("y",ground_y+1));height=max(1,int(node.get("height",2 if kind=="wall" else 1)))
                count=_wall_route(blocks,centers,base,height,state)
                stats["wall_blocks" if kind=="wall" else "fence_blocks"]+=count
        elif kind=="stairs":
            stats["stair_blocks"]+=_network_stairs(blocks,node)
        else:
            raise ValueError(f"Unknown site network type: {kind}")
    stats["networks"]=len(cfg.get("networks",[]))
    return stats


def apply_site(plan: ProjectPlan, placed: dict[str, PlacedModule], blocks: dict[Vec3, str]):
    cfg = plan.site
    if not cfg.get("enabled", False):
        return {
            "ground_blocks": 0, "path_blocks": 0, "edge_blocks": 0,
            "character": cfg.get("character", "generic"),
            "networks": 0,
        }

    x0, y0, z0, x1, y1, z1 = project_bounds(placed.values())
    margin = max(0, int(cfg.get("margin", 8)))
    ground_y = int(cfg.get("ground_y", y0 - 1))
    character = str(cfg.get("character", "generic"))
    default_ground, default_path = CHARACTER_DEFAULTS.get(character, CHARACTER_DEFAULTS["generic"])
    ground_state = cfg.get("ground_state", default_ground)
    path_state = cfg.get("path_state", default_path)

    ground_count = 0
    for z in range(z0 - margin, z1 + margin + 1):
        for x in range(x0 - margin, x1 + margin + 1):
            pos = (x, ground_y, z)
            if pos not in blocks:
                blocks[pos] = ground_state
                ground_count += 1

    path_count = 0
    for route in cfg.get("paths", []):
        start = tuple(int(v) for v in route["from"])
        end = tuple(int(v) for v in route["to"])
        width = max(1, int(route.get("width", 3)))
        centers=list(_line_points((start[0],start[-1]),(end[0],end[-1])))
        path_count += _surface_route(blocks,centers,int(route.get("y",ground_y)),width,route.get("state",path_state))

    edge_count = 0
    if cfg.get("edge_feature", True):
        edge_state = cfg.get("edge_state", _edge_feature_state(character))
        if edge_state and margin >= 3:
            ex0, ex1 = x0 - margin + 2, x1 + margin - 2
            ez0, ez1 = z0 - margin + 2, z1 + margin - 2
            spacing = max(2, int(cfg.get("edge_spacing", 3)))
            for x in range(ex0, ex1 + 1, spacing):
                for z in (ez0, ez1):
                    blocks[(x, ground_y + 1, z)] = edge_state
                    edge_count += 1
            for z in range(ez0, ez1 + 1, spacing):
                for x in (ex0, ex1):
                    blocks[(x, ground_y + 1, z)] = edge_state
                    edge_count += 1

    networks=_apply_networks(blocks,cfg,ground_y,path_state)
    return {
        "ground_blocks": ground_count,
        "path_blocks": path_count,
        "edge_blocks": edge_count,
        "character": character,
        "vegetation_profile": cfg.get("vegetation_profile", "temperate"),
        **networks,
    }
