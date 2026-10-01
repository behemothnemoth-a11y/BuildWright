#!/usr/bin/env python3
from __future__ import annotations
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
required=[
 'README.md','AGENTS.md','PROJECT_STATE.md','buildwright.json','VANILLA_BUILD_LANGUAGE.md','MICROBLOCK_IMPLEMENTATION.md','CATALOG.md','VISUAL_CATALOG.md','MICROBLOCK_CATALOG.md','catalog/catalog.json','catalog/milestones.json','catalog/visual/visual_manifest.json',
 'docs/PACK_SYSTEM.md','docs/FIXTURE_SYSTEM.md','docs/COMPOSITION_COMPILER.md','docs/ROOM_BRIEF_CONTRACT.md','docs/CONNECTORS_AND_KEEPOUTS.md','docs/UNIVERSAL_STYLE_SYSTEM.md','docs/VANILLA_DETAIL_LAYER.md','docs/STRUCTURAL_SITE_INTELLIGENCE.md','docs/STYLE_FINISH_REFERENCE_FIT.md',
 'packs/registry.json','packs/index.json','packs/microblock/registry.json','packs/microblock/index.json',
 'fixtures/registry.json','fixtures/index.json','fixtures/corpus/transform_manifest.json',
 'composition/index.json','composition/detail.py','composition/detail_profiles.json','composition/templates/freeform.json','composition/templates/grand_hall.json','composition/templates/library.json',
 'project_graph/index.json','project_graph/style_registry.json','project_graph/style.py','project_graph/compiler.py','project_graph/solver.py','project_graph/facade.py','project_graph/roof.py','project_graph/site.py','project_graph/vanilla_finish.py','project_graph/foundation.py','project_graph/structures.py','project_graph/style_finish.py','project_graph/style_finish_profiles.json','project_graph/reference_fit.py',
 'schemas/fixture.schema.json','schemas/fixture_registry.schema.json','schemas/composition_brief.schema.json','schemas/composition_template.schema.json','schemas/composition_palette.schema.json','schemas/composition_manifest.schema.json','schemas/project_graph.schema.json','schemas/style_language.schema.json',
 'tools/validate_packs.py','tools/validate_microblocks.py','tools/validate_fixtures.py','tools/validate_composition.py','tools/compile_module.py','tools/plan_composition.py','tools/validate_project_graph.py','tools/compile_project.py','tools/compile_project_examples.py','tools/validate_style_system.py','tools/compile_style_showcases.py','tools/render_litematic_iso.py','tools/build_visual_catalog.py','tools/validate_vanilla_baseline.py','tools/build_vanilla_detail_fixtures.py','tools/compile_vanilla_detail_examples.py','tools/compile_vanilla_detail_projects.py','tools/compile_structural_site_examples.py','tools/compile_style_finish_examples.py',
 'projects/wayne-manor/PROJECT.md','projects/wayne-manor/module_registry.json'
]
err=[f'missing required file: {r}' for r in required if not (ROOT/r).is_file()]
try:
 cfg=json.loads((ROOT/'buildwright.json').read_text(encoding='utf-8'))
 if cfg.get('name')!='BuildWright':err.append('buildwright.json name must be BuildWright')
 if cfg.get('version')!='0.11.0':err.append('buildwright.json version must be 0.11.0 for DROP 0011')
 fixture=cfg.get('fixture_system',{})
 if fixture.get('vanilla_fixtures')!=85:err.append('fixture_system.vanilla_fixtures must be 85')
 if fixture.get('vanilla_detail_fixtures')!=45:err.append('fixture_system.vanilla_detail_fixtures must be 45')
 comp=cfg.get('composition_system',{})
 if comp.get('templates')!=11:err.append('composition_system.templates must be 11')
 if comp.get('palettes')!=8:err.append('composition_system.palettes must be 8')
 if comp.get('example_modules')!=7:err.append('composition_system.example_modules must be 7')
 if comp.get('vanilla_detail_profiles')!=10:err.append('composition_system.vanilla_detail_profiles must be 10')
 if comp.get('vanilla_detail_examples')!=10:err.append('composition_system.vanilla_detail_examples must be 10')
 if not comp.get('vanilla_detail_engine'):err.append('composition vanilla detail engine must be enabled')
 graph=cfg.get('project_graph_system',{})
 if graph.get('style_profiles')!=35:err.append('project_graph_system.style_profiles must be 35')
 if graph.get('style_families')!=14:err.append('project_graph_system.style_families must be 14')
 if graph.get('style_showcases')!=37:err.append('project_graph_system.style_showcases must be 37')
 if graph.get('vanilla_detail_projects')!=3:err.append('project_graph_system.vanilla_detail_projects must be 3')
 if graph.get('structural_site_examples')!=3:err.append('project_graph_system.structural_site_examples must be 3')
 if graph.get('style_finish_profiles')!=14:err.append('project_graph_system.style_finish_profiles must be 14')
 if graph.get('style_finish_examples')!=14:err.append('project_graph_system.style_finish_examples must be 14')
 if not graph.get('style_finish_engine'):err.append('project graph style finish engine must be enabled')
 if not graph.get('reference_fit_engine'):err.append('project graph reference fit engine must be enabled')
 if not graph.get('reference_fit_strict_mode'):err.append('project graph strict reference fit mode must be enabled')
 if not graph.get('vanilla_finish_engine'):err.append('project graph vanilla finish engine must be enabled')
 if not graph.get('routed_corridors'):err.append('project graph routed corridors must be enabled')
 if not graph.get('elevation_stairs'):err.append('project graph elevation stairs must be enabled')
 if not graph.get('structural_nodes'):err.append('project graph structural nodes must be enabled')
 if not graph.get('site_networks'):err.append('project graph site networks must be enabled')
 if not graph.get('foundation_engine'):err.append('project graph foundation engine must be enabled')
 visual=cfg.get('visual_catalog',{})
 if visual.get('vanilla_fixture_previews')!=85:err.append('visual_catalog.vanilla_fixture_previews must be 85')
 if visual.get('vanilla_room_renders')!=6:err.append('visual_catalog.vanilla_room_renders must be 6')
 if visual.get('vanilla_project_renders')!=3:err.append('visual_catalog.vanilla_project_renders must be 3')
 if visual.get('vanilla_style_baselines')!=37:err.append('visual_catalog.vanilla_style_baselines must be 37')
 if visual.get('vanilla_detail_room_renders')!=10:err.append('visual_catalog.vanilla_detail_room_renders must be 10')
 if visual.get('vanilla_detail_project_renders')!=3:err.append('visual_catalog.vanilla_detail_project_renders must be 3')
 if visual.get('structural_site_renders')!=3:err.append('visual_catalog.structural_site_renders must be 3')
 if visual.get('style_finish_renders')!=14:err.append('visual_catalog.style_finish_renders must be 14')
 if visual.get('microblock_fixture_previews')!=24:err.append('visual_catalog.microblock_fixture_previews must be 24')
 if visual.get('hybrid_room_renders')!=1:err.append('visual_catalog.hybrid_room_renders must be 1')
 if visual.get('base_policy')!='vanilla_only':err.append('visual catalog base policy must be vanilla_only')
 if graph.get('example_projects')!=3:err.append('project_graph_system.example_projects must be 3')
 if not graph.get('facade_compiler'):err.append('facade compiler must be enabled')
 if not graph.get('site_compiler'):err.append('site compiler must be enabled')
 if not graph.get('style_blending'):err.append('style blending must be enabled')
 if not graph.get('facade_zoning'):err.append('facade zoning must be enabled')
except Exception as e:err.append(f'buildwright.json invalid: {e}')
if err:
 print('BUILDWRIGHT VALIDATION: FAIL');[print(' -',x) for x in err];sys.exit(1)
checks=[
 ('validate_packs.py',[]),('build_pack_index.py',['--check']),
 ('validate_microblocks.py',[]),('build_microblock_index.py',['--check']),
 ('validate_fixtures.py',[]),('compile_fixtures.py',['--check']),('build_fixture_index.py',['--check']),('validate_transform_corpus.py',[]),
 ('validate_composition.py',[]),('build_composition_index.py',['--check']),('compile_composition_examples.py',['--check']),('compile_vanilla_detail_examples.py',['--check']),
 ('validate_project_graph.py',[]),('compile_project_examples.py',['--check']),('compile_vanilla_detail_projects.py',['--check']),('compile_structural_site_examples.py',['--check']),('compile_style_finish_examples.py',['--check']),
 ('validate_style_system.py',[]),('build_style_registry.py',['--check']),('compile_style_showcases.py',['--check']),
 ('build_catalog.py',['--check']),('build_visual_catalog.py',['--check']),('validate_vanilla_baseline.py',[])
]
for tool,args in checks:
 r=subprocess.run([sys.executable,str(ROOT/'tools'/tool),*args],cwd=ROOT)
 if r.returncode:sys.exit(r.returncode)
print('BUILDWRIGHT VALIDATION: PASS')
