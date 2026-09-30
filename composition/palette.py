from __future__ import annotations
import json
from pathlib import Path
from .transforms import parse_state,format_state

STONE_FAMILIES={
 'stone_bricks':{'block':'stone_bricks','stairs':'stone_brick_stairs','slab':'stone_brick_slab','wall':'stone_brick_wall'},
 'tuff_bricks':{'block':'tuff_bricks','stairs':'tuff_brick_stairs','slab':'tuff_brick_slab','wall':'tuff_brick_wall'},
 'deepslate_tiles':{'block':'deepslate_tiles','stairs':'deepslate_tile_stairs','slab':'deepslate_tile_slab','wall':'deepslate_tile_wall'},
 'deepslate_bricks':{'block':'deepslate_bricks','stairs':'deepslate_brick_stairs','slab':'deepslate_brick_slab','wall':'deepslate_brick_wall'},
 'polished_blackstone_bricks':{'block':'polished_blackstone_bricks','stairs':'polished_blackstone_brick_stairs','slab':'polished_blackstone_brick_slab','wall':'polished_blackstone_brick_wall'},
 'quartz':{'block':'quartz_block','stairs':'quartz_stairs','slab':'quartz_slab','wall':None},
}
WOOD_SUFFIXES=('planks','stairs','slab','fence','fence_gate','door','trapdoor','button','pressure_plate','log','wood','leaves')
WOOD_SPECIES=('oak','spruce','birch','jungle','acacia','dark_oak','mangrove','cherry','pale_oak')

def stone_shape(name:str):
    n=name.removeprefix('minecraft:')
    for fam,m in STONE_FAMILIES.items():
        for shape,b in m.items():
            if b and n==b:return fam,shape
    return None,None

def wood_shape(name:str):
    n=name.removeprefix('minecraft:')
    for sp in WOOD_SPECIES:
        if n==sp+'_planks':return sp,'planks'
        if n==sp+'_stairs':return sp,'stairs'
        if n==sp+'_slab':return sp,'slab'
        if n==sp+'_fence':return sp,'fence'
        if n==sp+'_fence_gate':return sp,'fence_gate'
        if n==sp+'_door':return sp,'door'
        if n==sp+'_trapdoor':return sp,'trapdoor'
        if n==sp+'_button':return sp,'button'
        if n==sp+'_pressure_plate':return sp,'pressure_plate'
        if n==sp+'_log':return sp,'log'
        if n==sp+'_wood':return sp,'wood'
        if n==sp+'_leaves':return sp,'leaves'
    return None,None

class PalettePlan:
    def __init__(self,data:dict):self.data=data
    @classmethod
    def load(cls,path:Path):return cls(json.loads(path.read_text(encoding='utf-8')))
    @property
    def shell(self):return self.data.get('shell',{})
    def remap(self,state:str)->str:
        name,props=parse_state(state)
        exact=self.data.get('exact',{})
        if name in exact:name=exact[name]
        sf,shape=stone_shape(name)
        if sf:
            target=self.data.get('stone_families',{}).get(sf)
            if target and target in STONE_FAMILIES:
                new=STONE_FAMILIES[target].get(shape)
                if new:name='minecraft:'+new
        sp,wshape=wood_shape(name)
        if sp:
            target=self.data.get('wood_species',{}).get(sp)
            if target:
                suffix={'planks':'planks','stairs':'stairs','slab':'slab','fence':'fence','fence_gate':'fence_gate','door':'door','trapdoor':'trapdoor','button':'button','pressure_plate':'pressure_plate','log':'log','wood':'wood','leaves':'leaves'}[wshape]
                name=f'minecraft:{target}_{suffix}'
        return format_state(name,props)
