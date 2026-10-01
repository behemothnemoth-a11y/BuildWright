from __future__ import annotations
from collections import Counter
import heapq
from typing import Any

from composition.compiler import _astra_be
from composition.transforms import transform_fixture_blocks, transform_grid_words, transform_pos, transform_state

from .model import CARDINAL, Connection, ModuleSpec, ProjectPlan, Port, port_for
from .solver import OUT, PlacedModule, world_port

Vec3 = tuple[int, int, int]

def _add(a: Vec3, b: Vec3) -> Vec3:
    return tuple(a[i] + b[i] for i in range(3))

def module_payload(module: ModuleSpec, placement: PlacedModule):
    ox, oy, oz = placement.origin
    transformed = transform_fixture_blocks(module.source["blocks"], module.source_size, module.rotation, module.mirror)
    blocks = {}
    for block in transformed:
        x, y, z = block["pos"]
        blocks[(ox + x, oy + y, oz + z)] = block["state"]

    block_entities = []
    for host in module.source.get("microblock_hosts", []):
        local = transform_pos(tuple(host["pos"]), module.source_size, module.rotation, module.mirror)
        pos = (ox + local[0], oy + local[1], oz + local[2])
        words = [int(h, 16) for h in host["occupancy_words_hex"]]
        words = transform_grid_words(words, module.rotation, module.mirror)
        block_entities.append(_astra_be(pos, words, host.get("host_material", "stone")))
    return blocks, block_entities

def merge_modules(plan: ProjectPlan, placed: dict[str, PlacedModule]):
    blocks: dict[Vec3, str] = {}
    block_entities: list[dict[str, Any]] = []
    conflicts = Counter()
    for module_id in plan.modules:
        module = plan.modules[module_id]
        payload, entities = module_payload(module, placed[module_id])
        for pos, state in payload.items():
            if pos in blocks and blocks[pos] != state:
                conflicts[(blocks[pos], state)] += 1
            blocks[pos] = state
        block_entities.extend(entities)
    warnings = []
    if conflicts:
        total = sum(conflicts.values())
        warnings.append(f"{total} overlapping module block-state conflicts reconciled by graph order")
    return blocks, block_entities, warnings

def _opening_cells(anchor: Vec3, port: Port, width: int | None = None, height: int | None = None):
    x, y, z = anchor
    width = int(width or port.width)
    height = int(height or port.height)
    half = width // 2
    if port.side in ("north", "south"):
        for yy in range(y, y + height):
            for xx in range(x - half, x - half + width):
                for zz in range(z - 1, z + 2):
                    yield (xx, yy, zz)
    elif port.side in ("west", "east"):
        for yy in range(y, y + height):
            for zz in range(z - half, z - half + width):
                for xx in range(x - 1, x + 2):
                    yield (xx, yy, zz)
    else:
        depth = max(1, port.depth)
        for yy in range(y - 1, y + 2):
            for xx in range(x - half, x - half + width):
                for zz in range(z - depth // 2, z - depth // 2 + depth):
                    yield (xx, yy, zz)
def carve_connections(plan: ProjectPlan, placed: dict[str, PlacedModule], blocks: dict[Vec3, str]):
    for connection in plan.connections:
        a_mod = plan.modules[connection.a_module]
        b_mod = plan.modules[connection.b_module]
        a = world_port(placed[a_mod.id].origin, port_for(a_mod, connection.a_port))
        b = world_port(placed[b_mod.id].origin, port_for(b_mod, connection.b_port))
        width = int(connection.width or min(a.width, b.width))
        height = int(connection.height or min(a.height, b.height))
        for pos in _opening_cells(a.pos, a, width, height):
            blocks.pop(pos, None)
        for pos in _opening_cells(b.pos, b, width, height):
            blocks.pop(pos, None)

def build_straight_corridors(plan: ProjectPlan, placed: dict[str, PlacedModule], blocks: dict[Vec3, str]):
    stats={"straight":0,"routed":0,"stairs":0,"route_blocks":0,"route_length":0}
    for connection in plan.connections:
        if connection.mode not in {"corridor","route","stairs"}:
            continue
        a_mod = plan.modules[connection.a_module]
        b_mod = plan.modules[connection.b_module]
        a = world_port(placed[a_mod.id].origin, port_for(a_mod, connection.a_port))
        b = world_port(placed[b_mod.id].origin, port_for(b_mod, connection.b_port))
        width = int(connection.width or min(a.width, b.width))
        height = int(connection.height or min(a.height, b.height))
        opts=dict(connection.options or {})
        floor_state=opts.get("floor_state","minecraft:polished_deepslate")
        wall_state=opts.get("wall_state","minecraft:tuff_bricks")
        ceiling_state=opts.get("ceiling_state","minecraft:dark_oak_planks")
        before=len(blocks)
        if connection.mode=="corridor":
            _corridor_between(blocks,a.pos,b.pos,a.side,width,height,floor_state,wall_state,ceiling_state)
            stats["straight"]+=1
        elif connection.mode=="route":
            path=_route_corridor(plan,placed,a,b,width,opts)
            _corridor_from_path(blocks,path,a.pos[1],width,height,floor_state,wall_state,ceiling_state)
            stats["routed"]+=1
            stats["route_length"]+=len(path)
        else:
            length=_stair_connection(blocks,a,b,width,height,opts)
            stats["stairs"]+=1
            stats["route_length"]+=length
        stats["route_blocks"]+=max(0,len(blocks)-before)
    return stats

def _corridor_between(blocks, start: Vec3, end: Vec3, side: str, width: int, height: int, floor_state: str, wall_state: str, ceiling_state: str):
    sx, sy, sz = start
    ex, ey, ez = end
    if sy != ey:
        raise ValueError("Straight corridor endpoints must share connector floor elevation")
    half = width // 2
    base_y = sy - 1
    if side in ("east", "west"):
        lo, hi = sorted((sx, ex))
        for x in range(lo, hi + 1):
            for z in range(sz - half, sz - half + width):
                blocks[(x, base_y, z)] = floor_state
                blocks[(x, base_y + height + 1, z)] = ceiling_state
                for y in range(base_y + 1, base_y + height + 1):
                    if z in (sz - half, sz - half + width - 1):
                        blocks[(x, y, z)] = wall_state
                    else:
                        blocks.pop((x, y, z), None)
    elif side in ("north", "south"):
        lo, hi = sorted((sz, ez))
        for z in range(lo, hi + 1):
            for x in range(sx - half, sx - half + width):
                blocks[(x, base_y, z)] = floor_state
                blocks[(x, base_y + height + 1, z)] = ceiling_state
                for y in range(base_y + 1, base_y + height + 1):
                    if x in (sx - half, sx - half + width - 1):
                        blocks[(x, y, z)] = wall_state
                    else:
                        blocks.pop((x, y, z), None)
    else:
        raise ValueError(f"Corridor mode requires cardinal ports, got {side}")


def _route_corridor(plan: ProjectPlan, placed: dict[str, PlacedModule], a: Port, b: Port, width: int, opts: dict):
    if a.pos[1] != b.pos[1]:
        raise ValueError("Routed corridor endpoints must share floor elevation; use stairs for elevation changes")
    start3=_add(a.pos,OUT[a.side])
    end3=_add(b.pos,OUT[b.side])
    start=(start3[0],start3[2]);end=(end3[0],end3[2])
    half=width//2
    pad=half+1
    blocked=set()
    for module in placed.values():
        x0,y0,z0,x1,y1,z1=module.box
        for x in range(x0-pad,x1+pad+1):
            for z in range(z0-pad,z1+pad+1):
                blocked.add((x,z))
    # Endpoint approach zones are intentionally clear so the route can meet each port.
    clear=max(2,pad+1)
    for cx,cz in (start,end):
        for x in range(cx-clear,cx+clear+1):
            for z in range(cz-clear,cz+clear+1):
                blocked.discard((x,z))
    margin=max(8,int(opts.get("max_detour",24)))
    xs=[start[0],end[0]]+[v for m in placed.values() for v in (m.box[0],m.box[3])]
    zs=[start[1],end[1]]+[v for m in placed.values() for v in (m.box[2],m.box[5])]
    minx,maxx=min(xs)-margin,max(xs)+margin
    minz,maxz=min(zs)-margin,max(zs)+margin
    dirs=((1,0),(0,1),(-1,0),(0,-1))
    heap=[(abs(start[0]-end[0])+abs(start[1]-end[1]),0,start)]
    came={};cost={start:0};seen=set()
    while heap:
        _,g,current=heapq.heappop(heap)
        if current in seen:continue
        seen.add(current)
        if current==end:break
        for dx,dz in dirs:
            nxt=(current[0]+dx,current[1]+dz)
            if not (minx<=nxt[0]<=maxx and minz<=nxt[1]<=maxz):continue
            if nxt in blocked and nxt not in {start,end}:continue
            ng=g+1
            if ng>=cost.get(nxt,10**9):continue
            cost[nxt]=ng;came[nxt]=current
            h=abs(nxt[0]-end[0])+abs(nxt[1]-end[1])
            heapq.heappush(heap,(ng+h,ng,nxt))
    if end not in cost:
        raise ValueError(f"No collision-free routed corridor path from {start} to {end}")
    path=[end];cur=end
    while cur!=start:
        cur=came[cur];path.append(cur)
    path.reverse()
    return path

def _corridor_from_path(blocks, path, floor_y_port: int, width: int, height: int, floor_state: str, wall_state: str, ceiling_state: str):
    half=width//2
    footprint=set()
    for cx,cz in path:
        for dx in range(-half,-half+width):
            for dz in range(-half,-half+width):
                footprint.add((cx+dx,cz+dz))
    base_y=floor_y_port-1
    for x,z in footprint:
        blocks[(x,base_y,z)]=floor_state
        blocks[(x,base_y+height+1,z)]=ceiling_state
        for y in range(base_y+1,base_y+height+1):
            blocks.pop((x,y,z),None)
    for x,z in footprint:
        for dx,dz in ((1,0),(-1,0),(0,1),(0,-1)):
            edge=(x+dx,z+dz)
            if edge in footprint:continue
            for y in range(base_y+1,base_y+height+1):
                blocks.setdefault((edge[0],y,edge[1]),wall_state)

def _stair_connection(blocks, a: Port, b: Port, width: int, height: int, opts: dict):
    start3=_add(a.pos,OUT[a.side]);end3=_add(b.pos,OUT[b.side])
    sx,sy,sz=start3;ex,ey,ez=end3
    if sx!=ex and sz!=ez:
        raise ValueError("Stair connections currently require cardinally aligned endpoints")
    dx=0 if sx==ex else (1 if ex>sx else -1)
    dz=0 if sz==ez else (1 if ez>sz else -1)
    dist=abs(ex-sx)+abs(ez-sz)
    rise=ey-sy
    if dist<abs(rise):
        raise ValueError(f"Stair run {dist} is too short for elevation change {rise}")
    if dist==0 and rise!=0:
        raise ValueError("Stair endpoints need horizontal run")
    floor_state=opts.get("landing_state","minecraft:stone_bricks")
    stair_block=opts.get("stair_block","minecraft:stone_brick_stairs")
    rail_state=opts.get("rail_state","minecraft:iron_bars")
    dirs={(1,0):"east",(-1,0):"west",(0,1):"south",(0,-1):"north"}
    opposite={"east":"west","west":"east","north":"south","south":"north"}
    move_facing=dirs.get((dx,dz),"north")
    stair_facing=move_facing if rise>=0 else opposite[move_facing]
    half=width//2
    points=[]
    for i in range(dist+1):
        x=sx+dx*i;z=sz+dz*i
        level=(sy-1) if dist==0 else (sy-1)+round((rise*i)/dist)
        points.append((x,level,z))
    for i,(x,level,z) in enumerate(points):
        next_level=points[i+1][1] if i+1<len(points) else level
        prev_level=points[i-1][1] if i>0 else level
        climbing=(next_level!=level) or (prev_level!=level)
        state=(f"{stair_block}[facing={stair_facing},half=bottom,shape=straight,waterlogged=false]" if climbing else floor_state)
        lateral=((0,1) if dx else (1,0))
        for off in range(-half,-half+width):
            px=x+lateral[0]*off;pz=z+lateral[1]*off
            blocks[(px,level,pz)]=state
            for yy in range(level+1,level+height+1):
                blocks.pop((px,yy,pz),None)
        for off in (-half-1,-half+width):
            px=x+lateral[0]*off;pz=z+lateral[1]*off
            blocks.setdefault((px,level+1,pz),rail_state)
            blocks.setdefault((px,level+2,pz),rail_state)
    return len(points)

def exterior_sides(plan: ProjectPlan):
    interior = set()
    for c in plan.connections:
        if c.mode == "attach":
            interior.add((c.a_module, port_for(plan.modules[c.a_module], c.a_port).side))
            interior.add((c.b_module, port_for(plan.modules[c.b_module], c.b_port).side))
    return {
        m.id: [side for side in ("north", "south", "east", "west") if (m.id, side) not in interior]
        for m in plan.modules.values()
    }
