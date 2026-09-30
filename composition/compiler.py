from __future__ import annotations
import json,sys
from pathlib import Path
from .planner import plan_brief
from .palette import PalettePlan
from .transforms import transform_fixture_blocks,transform_grid_words
from .geometry import box_for_connector
from .manifest import write_manifest
from .preview import render_plan_svg

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT/'tools') not in sys.path:sys.path.insert(0,str(ROOT/'tools'))
from litematic_codec import B,I,L,LT,TAG_COMPOUND,make,read,unpack,i64

DEFAULT_SHELL={
 'floor':'minecraft:polished_deepslate',
 'wall':'minecraft:tuff_bricks',
 'ceiling':'minecraft:dark_oak_planks'
}

def _load_json(p:Path):return json.loads(p.read_text(encoding='utf-8'))

def _write_text_lf(path:Path, text:str):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(text.replace('\r\n','\n').replace('\r','\n').encode('utf-8'))

def _palette(root:Path,palette_id:str|None):
    if not palette_id:return PalettePlan({'id':'composition.default','shell':DEFAULT_SHELL})
    slug=palette_id.split('.')[-1]
    p=root/'composition/palettes'/f'{slug}.json'
    if not p.is_file():raise FileNotFoundError(f'Composition palette not found: {palette_id}')
    return PalettePlan.load(p)

def _shell_blocks(size, shell_cfg, palette:PalettePlan):
    W,H,D=size; blocks={};cfg=dict(shell_cfg or {});ps=dict(DEFAULT_SHELL);ps.update(palette.shell)
    floor_state=cfg.get('floor_state',ps['floor']);wall_state=cfg.get('wall_state',ps['wall']);ceil_state=cfg.get('ceiling_state',ps['ceiling'])
    if cfg.get('floor',True):
        for z in range(D):
            for x in range(W):blocks[(x,0,z)]=floor_state
    wall_h=int(cfg.get('wall_height',H-2 if cfg.get('ceiling',False) else H-1));th=max(1,int(cfg.get('wall_thickness',1)))
    if cfg.get('walls',True):
        for y in range(1,min(H,wall_h+1)):
            for t in range(th):
                for x in range(W):blocks[(x,y,t)]=wall_state;blocks[(x,y,D-1-t)]=wall_state
                for z in range(D):blocks[(t,y,z)]=wall_state;blocks[(W-1-t,y,z)]=wall_state
    if cfg.get('ceiling',False):
        y=int(cfg.get('ceiling_y',H-1))
        for z in range(D):
            for x in range(W):blocks[(x,y,z)]=ceil_state
    return blocks

def _astra_be(pos,words,material):
    x,y,z=pos;oak=words if material=='oak' else [0]*64
    d={'id':'astra_microblocks:test_host','x':I(x),'y':I(y),'z':I(z),'astra_orientation':I(0),'grid_format_v1':B(1),'revision':L(1),'has_undo':B(0),'materials_v2':B(1)}
    for n,v in enumerate(words):d[f'grid_{n}']=L(i64(v))
    for n,v in enumerate(oak):d[f'oak_{n}']=L(i64(v))
    return d

def _fixture_payload(root,fixture_id,placement,palette):
    src=None
    # source path is looked up from registry for future-proofing
    reg=_load_json(root/'fixtures/registry.json')
    item=next(x for x in reg['fixtures'] if x['id']==fixture_id);src=_load_json(root/item['source'])
    ox,oy,oz=placement.origin
    if src['stage']=='vanilla':
        transformed=transform_fixture_blocks(src['blocks'],tuple(src['size']),placement.rotation,placement.mirror)
        out={}
        for b in transformed:
            x,y,z=b['pos'];out[(ox+x,oy+y,oz+z)]=palette.remap(b['state'])
        return out,[],None
    words=[int(h,16) for h in src['occupancy_words_hex']]
    words=transform_grid_words(words,placement.rotation,placement.mirror)
    host='astra_microblocks:oak_host' if src.get('host_material')=='oak' else 'astra_microblocks:test_host'
    pos=(ox,oy,oz);blocks={pos:host+'[orientation=0]'};be=_astra_be(pos,words,src.get('host_material','stone'))
    source={'pos':list(pos),'fixture_id':fixture_id,'provider':'astra_microblocks','host_material':src.get('host_material','stone'),'occupancy_words_hex':[f'{w & ((1<<64)-1):016x}' for w in words]}
    return blocks,[be],source

def _validate_bounds(blocks,size):
    W,H,D=size;bad=[]
    for p in blocks:
        x,y,z=p
        if not (0<=x<W and 0<=y<H and 0<=z<D):bad.append(p)
    if bad:raise ValueError(f'{len(bad)} blocks outside module bounds; first={bad[0]}')

def _validate_litematic(path:Path,expected_nonair:int):
    root=read(path);meta=root['Metadata'];regions=root['Regions']
    if len(regions)!=1:raise ValueError('composition output must contain exactly one region')
    reg=next(iter(regions.values()));s=reg['Size'];count=s['x']*s['y']*s['z'];palette=reg['BlockStatePalette'];idx=unpack(reg['BlockStates'],count,len(palette));nonair=sum(i!=0 for i in idx)
    if nonair!=expected_nonair or meta['TotalBlocks']!=expected_nonair:raise ValueError(f'composition readback mismatch {nonair}/{meta["TotalBlocks"]} != {expected_nonair}')
    return {'regions':1,'nonair':nonair,'volume':count,'palette':len(palette)}

def compile_brief(root:Path, brief:dict|Path, output_dir:Path|None=None):
    root=Path(root)
    if isinstance(brief,Path):brief=_load_json(brief)
    plan=plan_brief(root,brief);palette=_palette(root,plan.palette)
    outdir=Path(output_dir) if output_dir else root/'composition/compiled_examples';outdir.mkdir(parents=True,exist_ok=True)
    template_path=root/'composition/templates'/f'{plan.template_id}.json';template=_load_json(template_path) if template_path.is_file() else {}
    shell_cfg=dict(template.get('shell',{}));shell_cfg.update(brief.get('shell',{}))
    module_id=brief['id'];blocks=_shell_blocks(plan.room_size,shell_cfg,palette);block_entities=[];micro_sources=[]
    # Open declared connectors before fixture placement so wall-integrated pieces do not hide them.
    for c in plan.connectors:
        for p in box_for_connector(c,plan.room_size,keepout=False).cells():blocks.pop(p,None)
    warnings=list(plan.warnings)
    for p in plan.placements:
        fblocks,fbe,msrc=_fixture_payload(root,p.fixture_id,p,palette)
        if p.placement_mode=='carve_and_place':
            for cell in p.declared_box.cells():blocks.pop(cell,None)
        if p.placement_mode=='add':
            fblocks={k:v for k,v in fblocks.items() if k not in blocks}
        blocks.update(fblocks);block_entities.extend(fbe)
        if msrc:micro_sources.append(msrc)
    # Connector clearance is authoritative and is re-carved after all fixtures.
    for c in plan.connectors:
        for p in box_for_connector(c,plan.room_size,keepout=False).cells():blocks.pop(p,None)
    _validate_bounds(blocks,plan.room_size)
    source_path=outdir/f'{module_id}.source.json';lit_path=outdir/f'{module_id}.litematic';manifest_path=outdir/f'{module_id}.manifest.json';svg_path=outdir/f'{module_id}.plan.svg'
    source={
      'schema_version':1,'id':module_id,'stage':brief.get('stage','vanilla'),'size':list(plan.room_size),
      'blocks':[{'pos':list(pos),'state':state} for pos,state in sorted(blocks.items(),key=lambda x:(x[0][1],x[0][2],x[0][0]))],
      'microblock_hosts':micro_sources,'connectors':plan.connectors
    }
    _write_text_lf(source_path,json.dumps(source,indent=2)+'\n')
    make(lit_path,'BuildWright '+brief.get('name',module_id),plan.room_size,blocks,block_entities,desc=f'BuildWright composed module: {module_id}',dataversion=int(brief.get('data_version',4903)))
    readback=_validate_litematic(lit_path,len(blocks));render_plan_svg(plan,svg_path)
    manifest=write_manifest(manifest_path,plan=plan,litematic_path=lit_path,source_path=source_path,block_count=len(blocks),palette_id=plan.palette,microblock_hosts=len(micro_sources),warnings=warnings)
    # write_manifest hashes relative path only if current process cwd matches root; correct it here deterministically
    import hashlib
    manifest['litematic']=lit_path.name
    manifest['source']=source_path.name
    manifest['preview']=svg_path.name
    manifest['litematic_sha256']=hashlib.sha256(lit_path.read_bytes()).hexdigest();manifest['readback']=readback
    _write_text_lf(manifest_path,json.dumps(manifest,indent=2)+'\n')
    return {'plan':plan,'litematic':lit_path,'source':source_path,'manifest':manifest_path,'preview':svg_path,'readback':readback}
