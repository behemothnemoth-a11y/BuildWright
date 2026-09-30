from __future__ import annotations
from collections import OrderedDict
from typing import Mapping

DIRS=('north','east','south','west')
VEC={'north':(0,-1),'east':(1,0),'south':(0,1),'west':(-1,0)}
INV={v:k for k,v in VEC.items()}

def transformed_size(size, rotation:int=0):
    w,h,d=size; r=rotation%4
    return (d,h,w) if r%2 else (w,h,d)

def transform_pos(pos,size,rotation:int=0,mirror:str='none'):
    x,y,z=pos; w,h,d=size; m=mirror.lower(); r=rotation%4
    if m=='x': x=w-1-x
    elif m=='z': z=d-1-z
    elif m not in ('none',''): raise ValueError(f'Unsupported mirror {mirror}')
    if r==0:return x,y,z
    if r==1:return d-1-z,y,x
    if r==2:return w-1-x,y,d-1-z
    return z,y,w-1-x

def transform_direction(direction:str, rotation:int=0, mirror:str='none')->str:
    if direction not in VEC:return direction
    x,z=VEC[direction]
    if mirror=='x':x=-x
    elif mirror=='z':z=-z
    for _ in range(rotation%4): x,z=-z,x
    return INV[(x,z)]

def parse_state(state:str):
    if '[' not in state:return state,OrderedDict()
    name,rest=state.split('[',1);rest=rest[:-1]
    props=OrderedDict()
    if rest:
        for kv in rest.split(','):
            k,v=kv.split('=',1);props[k]=v
    return name,props

def format_state(name:str,props:Mapping[str,str])->str:
    if not props:return name
    return name+'['+','.join(f'{k}={v}' for k,v in sorted(props.items()))+']'

def transform_state(state:str,rotation:int=0,mirror:str='none')->str:
    name,p=parse_state(state); p=dict(p); r=rotation%4
    if 'facing' in p and p['facing'] in VEC:p['facing']=transform_direction(p['facing'],r,mirror)
    if 'axis' in p and p['axis'] in ('x','z') and r%2:p['axis']='z' if p['axis']=='x' else 'x'
    cardinal={k:p[k] for k in DIRS if k in p}
    if cardinal:
        for k in cardinal:p.pop(k,None)
        for k,v in cardinal.items():p[transform_direction(k,r,mirror)]=v
    if 'rotation' in p:
        try:
            n=int(p['rotation'])%16
            if mirror=='x':n=(-n)%16
            elif mirror=='z':n=(8-n)%16
            n=(n+4*r)%16;p['rotation']=str(n)
        except ValueError:pass
    if mirror!='none' and 'hinge' in p and p['hinge'] in ('left','right'):
        p['hinge']='right' if p['hinge']=='left' else 'left'
    if mirror!='none' and 'shape' in p:
        p['shape']=p['shape'].replace('_left','__TMP__').replace('_right','_left').replace('__TMP__','_right')
    return format_state(name,p)

def transform_fixture_blocks(blocks:list[dict],size,rotation:int=0,mirror:str='none'):
    return [
        {'pos':list(transform_pos(tuple(b['pos']),tuple(size),rotation,mirror)),
         'state':transform_state(b['state'],rotation,mirror)}
        for b in blocks
    ]

def transform_grid_words(words:list[int],rotation:int=0,mirror:str='none')->list[int]:
    # Astra Microblocks uses x-fast, then z, then y.
    cells=set()
    for y in range(16):
        for z in range(16):
            for x in range(16):
                i=x|(z<<4)|(y<<8); wi=i>>6; bit=i&63
                if (words[wi]>>bit)&1:cells.add(transform_pos((x,y,z),(16,16,16),rotation,mirror))
    out=[0]*64
    for x,y,z in cells:
        i=x|(z<<4)|(y<<8);out[i>>6]|=1<<(i&63)
    return out
