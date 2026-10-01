from __future__ import annotations
from dataclasses import dataclass
import json,random
from pathlib import Path
from .transforms import transformed_size

@dataclass
class Fixture:
    id:str; stage:str; category:str; family:str; size:tuple[int,int,int]; source_path:Path; data:dict
    @property
    def anchor(self):return tuple(self.data.get('anchor',[0,0,0]))
    @property
    def tags(self):
        toks=set(self.id.replace('-','_').split('_'))|{self.category,self.family,self.stage}
        return toks
    @property
    def detail_fixture(self):
        return bool(self.data.get('detail_fixture',False))
    def occupied_local_box(self,rotation=0,mirror='none'):
        from .geometry import Box
        from .transforms import transform_pos
        if self.stage!='vanilla':return Box(0,0,0,0,0,0)
        pts=[transform_pos(tuple(b['pos']),self.size,rotation,mirror) for b in self.data.get('blocks',[])]
        if not pts:return Box(0,0,0,0,0,0)
        xs=[p[0] for p in pts];ys=[p[1] for p in pts];zs=[p[2] for p in pts]
        return Box(min(xs),min(ys),min(zs),max(xs),max(ys),max(zs))

class FixtureLibrary:
    def __init__(self,root:Path):
        self.root=root
        reg=json.loads((root/'fixtures/registry.json').read_text(encoding='utf-8'))
        self.items={}
        for x in reg['fixtures']:
            src=root/x['source'];d=json.loads(src.read_text(encoding='utf-8'))
            self.items[x['id']]=Fixture(x['id'],x['stage'],x['category'],x['family'],tuple(x['size']),src,d)
    def get(self,id):return self.items[id]
    def search(self,*,stage=None,category=None,families=None,preferred_ids=None,max_size=None,rotation=0,include_detail_fixtures=False):
        families=set(families or []); preferred=set(preferred_ids or [])
        out=[]
        for f in self.items.values():
            if f.detail_fixture and not include_detail_fixtures:continue
            if stage and f.stage!=stage:continue
            if category and f.category!=category:continue
            if families and f.family not in families:continue
            if max_size:
                s=transformed_size(f.size,rotation)
                if any(a>b for a,b in zip(s,max_size)):continue
            out.append(f)
        return out
    def rank(self,selector:dict,*,style:dict|None,rng:random.Random,usage:dict[str,int],rotation:int=0,max_size=None):
        c=self.search(stage=selector.get('stage'),category=selector.get('category'),families=selector.get('families'),preferred_ids=selector.get('preferred_ids'),max_size=max_size,rotation=rotation,include_detail_fixtures=bool(selector.get('include_detail_fixtures',False)))
        preferred=set(selector.get('preferred_ids',[])); style_tags=set((style or {}).get('selection_tags',[])); pref_families=set((style or {}).get('preferred_architecture_families',[]))
        max_repeats=int(selector.get('max_repeats',999));scored=[]
        for f in c:
            if usage.get(f.id,0)>=max_repeats:continue
            score=0.0
            if f.id in preferred:score+=100
            if f.family in pref_families:score+=12
            score+=3*len(f.tags&style_tags)
            score-=usage.get(f.id,0)*8
            score+=rng.random()*0.01
            scored.append((score,f))
        scored.sort(key=lambda t:t[0],reverse=True)
        return [f for _,f in scored]
    def choose(self,selector:dict,**kwargs):
        ranked=self.rank(selector,**kwargs)
        return ranked[0] if ranked else None
