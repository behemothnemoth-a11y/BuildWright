from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Iterator

Vec3 = tuple[int, int, int]

@dataclass(frozen=True)
class Box:
    min_x: int
    min_y: int
    min_z: int
    max_x: int
    max_y: int
    max_z: int

    @classmethod
    def from_origin_size(cls, origin: Vec3, size: Vec3) -> "Box":
        x,y,z = origin; w,h,d = size
        return cls(x,y,z,x+w-1,y+h-1,z+d-1)

    @property
    def size(self) -> Vec3:
        return (self.max_x-self.min_x+1, self.max_y-self.min_y+1, self.max_z-self.min_z+1)

    def intersects(self, other: "Box") -> bool:
        return not (
            self.max_x < other.min_x or other.max_x < self.min_x or
            self.max_y < other.min_y or other.max_y < self.min_y or
            self.max_z < other.min_z or other.max_z < self.min_z
        )

    def contains(self, pos: Vec3) -> bool:
        x,y,z = pos
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y and self.min_z <= z <= self.max_z

    def translated(self, delta: Vec3) -> "Box":
        dx,dy,dz = delta
        return Box(self.min_x+dx,self.min_y+dy,self.min_z+dz,self.max_x+dx,self.max_y+dy,self.max_z+dz)

    def inflated(self, xz: int=0, y: int=0) -> "Box":
        return Box(self.min_x-xz,self.min_y-y,self.min_z-xz,self.max_x+xz,self.max_y+y,self.max_z+xz)

    def cells(self) -> Iterator[Vec3]:
        for y in range(self.min_y,self.max_y+1):
            for z in range(self.min_z,self.max_z+1):
                for x in range(self.min_x,self.max_x+1):
                    yield x,y,z


def clamp(v:int, lo:int, hi:int)->int:
    return max(lo,min(hi,v))


def resolve_coord(value, axis_size:int, *, floor:int=0, ceiling:int|None=None) -> int:
    """Resolve compact template coordinates such as center, 25%, max-2, ceiling-1."""
    ceiling = axis_size-1 if ceiling is None else ceiling
    if isinstance(value, int): return value
    if isinstance(value, float): return int(round(value))
    if not isinstance(value, str): raise TypeError(f"Unsupported coordinate: {value!r}")
    s=value.strip().lower().replace(' ','')
    if s in {'center','50%'}: return (axis_size-1)//2
    if s in {'min','floor'}: return floor
    if s in {'max','ceiling'}: return ceiling
    if s.endswith('%'):
        p=float(s[:-1])/100.0
        return int(round((axis_size-1)*p))
    for base_name,base in [('min',0),('floor',floor),('max',axis_size-1),('ceiling',ceiling),('center',(axis_size-1)//2)]:
        if s.startswith(base_name+'+') or s.startswith(base_name+'-'):
            sign=1 if '+' in s[len(base_name):len(base_name)+1] else -1
            n=int(s[len(base_name)+1:])
            return base + sign*n
    return int(s)


def box_for_connector(conn:dict, room_size:Vec3, keepout:bool=False) -> Box:
    W,H,D=room_size
    side=conn.get('side','south').lower()
    width=int(conn.get('width',3)); height=int(conn.get('height',4)); depth=int(conn.get('depth',2))
    clearance=int(conn.get('clearance',3)) if keepout else 0
    y0=int(conn.get('y',1)); y1=min(H-1,y0+height-1)
    if side in ('north','south'):
        center=resolve_coord(conn.get('center','center'),W)
        x0=clamp(center-width//2,0,W-1); x1=clamp(x0+width-1,0,W-1)
        if side=='north': z0=0; z1=min(D-1,depth-1+clearance)
        else: z1=D-1; z0=max(0,D-depth-clearance)
        return Box(x0,y0,z0,x1,y1,z1)
    center=resolve_coord(conn.get('center','center'),D)
    z0=clamp(center-width//2,0,D-1); z1=clamp(z0+width-1,0,D-1)
    if side=='west': x0=0; x1=min(W-1,depth-1+clearance)
    else: x1=W-1; x0=max(0,W-depth-clearance)
    return Box(x0,y0,z0,x1,y1,z1)


def boxes_intersect_any(box:Box, others:Iterable[Box])->bool:
    return any(box.intersects(o) for o in others)
