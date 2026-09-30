from __future__ import annotations
from dataclasses import dataclass,asdict
import json,random
from pathlib import Path
from .fixture_library import FixtureLibrary,Fixture
from .geometry import Box,resolve_coord,box_for_connector
from .style import load_style
from .transforms import transformed_size,transform_pos

@dataclass
class Placement:
    slot_id:str
    fixture_id:str
    stage:str
    target:tuple[int,int,int]
    origin:tuple[int,int,int]
    rotation:int
    mirror:str
    size:tuple[int,int,int]
    box:Box
    declared_box:Box
    placement_mode:str='overlay'
    required:bool=False

    def to_dict(self):
        d=asdict(self);d['box']=asdict(self.box);d['declared_box']=asdict(self.declared_box);return d

@dataclass
class Plan:
    brief_id:str
    template_id:str
    room_size:tuple[int,int,int]
    placements:list[Placement]
    connectors:list[dict]
    keepouts:list[Box]
    warnings:list[str]
    seed:int
    style_profile:str|None
    palette:str|None

    def to_dict(self):
        return {
            'brief_id':self.brief_id,'template_id':self.template_id,'room_size':list(self.room_size),
            'placements':[p.to_dict() for p in self.placements],
            'connectors':self.connectors,'keepouts':[asdict(b) for b in self.keepouts],
            'warnings':self.warnings,'seed':self.seed,'style_profile':self.style_profile,'palette':self.palette
        }

def _load_json(p:Path):return json.loads(p.read_text(encoding='utf-8'))

def _resolve_target(target:dict,room_size):
    W,H,D=room_size
    return (
        resolve_coord(target.get('x','center'),W,ceiling=W-1),
        resolve_coord(target.get('y',1),H,ceiling=H-1),
        resolve_coord(target.get('z','center'),D,ceiling=D-1),
    )

def _placement_for(f:Fixture,slot_id,target,rotation,mirror,mode,required):
    tsize=transformed_size(f.size,rotation)
    anchor=transform_pos(f.anchor,f.size,rotation,mirror)
    origin=tuple(target[i]-anchor[i] for i in range(3))
    declared=Box.from_origin_size(origin,tsize)
    local=f.occupied_local_box(rotation,mirror);actual=local.translated(origin)
    return Placement(slot_id,f.id,f.stage,target,origin,rotation%4,mirror,tsize,actual,declared,mode,required)

def _inside_room(box:Box,room_size,allow_outside=False):
    if allow_outside:return True
    W,H,D=room_size
    return box.min_x>=0 and box.min_y>=0 and box.min_z>=0 and box.max_x<W and box.max_y<H and box.max_z<D

def _slot_targets(slot:dict):
    if 'targets' in slot:return slot['targets']
    return [slot.get('target',{'x':'center','y':1,'z':'center'})]

def plan_brief(root:Path,brief:dict|Path)->Plan:
    root=Path(root)
    if isinstance(brief,Path):brief=_load_json(brief)
    template_id=brief.get('template','freeform')
    tp=root/'composition/templates'/f'{template_id}.json'
    template=_load_json(tp) if tp.is_file() else {'id':template_id,'slots':[]}
    room_size=tuple(brief['size']);seed=int(brief.get('seed',0));rng=random.Random(seed)
    style_id=brief.get('style_profile') or template.get('style_profile')
    style=load_style(root,style_id)
    library=FixtureLibrary(root)
    density=float(brief.get('fixture_policy',{}).get('density',template.get('density',1.0)))
    global_repeat=int(brief.get('fixture_policy',{}).get('max_repeats',4))
    connectors=list(template.get('connectors',[]))+list(brief.get('connectors',[]))
    keepouts=[box_for_connector(c,room_size,keepout=True) for c in connectors]
    for k in brief.get('keepouts',[]):
        keepouts.append(Box(*k))
    placements=[];occupied=[];warnings=[];usage={}
    slots=list(template.get('slots',[]))+list(brief.get('slots',[]))
    excluded=set(brief.get('fixture_policy',{}).get('exclude',[]))
    allowed=set(brief.get('fixture_policy',{}).get('allow',[]))
    for slot in slots:
        required=bool(slot.get('required',False));prob=float(slot.get('probability',1.0))
        if not required and rng.random()>min(1.0,prob*density):continue
        selector=dict(slot.get('selector',{}))
        for key in ('preferred_ids','max_repeats','stage','category','families'):
            if key in slot and key not in selector:selector[key]=slot[key]
        if 'stage' not in selector:selector['stage']='vanilla' if brief.get('stage','vanilla')=='vanilla' else selector.get('stage','vanilla')
        selector['max_repeats']=min(int(selector.get('max_repeats',global_repeat)),global_repeat)
        rotation=int(slot.get('rotation',0))%4;mirror=slot.get('mirror','none');mode=slot.get('placement_mode','overlay')
        for idx,tdef in enumerate(_slot_targets(slot)):
            target=_resolve_target(tdef,room_size);sid=slot['id'] if len(_slot_targets(slot))==1 else f"{slot['id']}[{idx}]"
            ranked=library.rank(selector,style=style,rng=rng,usage=usage,rotation=rotation,max_size=room_size)
            if allowed:ranked=[f for f in ranked if f.id in allowed or f.family in allowed]
            ranked=[f for f in ranked if f.id not in excluded and f.family not in excluded]
            chosen=None
            for f in ranked:
                p=_placement_for(f,sid,target,rotation,mirror,mode,required)
                if not _inside_room(p.declared_box,room_size,bool(slot.get('allow_outside',False))):continue
                if not slot.get('allow_connector_overlap',False) and any(p.box.intersects(k) for k in keepouts):continue
                margin=int(slot.get('collision_margin',0));test=p.box.inflated(margin,0)
                if any(test.intersects(o) for o in occupied):continue
                chosen=p;break
            if chosen is None:
                msg=f"No fixture placement for slot {sid}"
                if required:warnings.append('REQUIRED: '+msg)
                continue
            placements.append(chosen);occupied.append(chosen.box);usage[chosen.fixture_id]=usage.get(chosen.fixture_id,0)+1
    return Plan(brief['id'],template_id,room_size,placements,connectors,keepouts,warnings,seed,style_id,brief.get('palette') or template.get('palette'))
