#!/usr/bin/env python3
from __future__ import annotations
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
required=[
 'README.md','AGENTS.md','PROJECT_STATE.md','buildwright.json','VANILLA_BUILD_LANGUAGE.md','MICROBLOCK_IMPLEMENTATION.md',
 'docs/PACK_SYSTEM.md','docs/FIXTURE_SYSTEM.md','docs/COMPOSITION_COMPILER.md','docs/ROOM_BRIEF_CONTRACT.md','docs/CONNECTORS_AND_KEEPOUTS.md',
 'packs/registry.json','packs/index.json','packs/microblock/registry.json','packs/microblock/index.json',
 'fixtures/registry.json','fixtures/index.json','fixtures/corpus/transform_manifest.json',
 'composition/index.json','composition/templates/freeform.json','composition/templates/grand_hall.json','composition/templates/library.json',
 'project_graph/index.json','project_graph/compiler.py','project_graph/solver.py','project_graph/facade.py','project_graph/roof.py','project_graph/site.py',
 'schemas/fixture.schema.json','schemas/fixture_registry.schema.json','schemas/composition_brief.schema.json','schemas/composition_template.schema.json','schemas/composition_palette.schema.json','schemas/composition_manifest.schema.json','schemas/project_graph.schema.json',
 'tools/validate_packs.py','tools/validate_microblocks.py','tools/validate_fixtures.py','tools/validate_composition.py','tools/compile_module.py','tools/plan_composition.py','tools/validate_project_graph.py','tools/compile_project.py','tools/compile_project_examples.py',
 'projects/wayne-manor/PROJECT.md','projects/wayne-manor/module_registry.json'
]
err=[f'missing required file: {r}' for r in required if not (ROOT/r).is_file()]
try:
 cfg=json.loads((ROOT/'buildwright.json').read_text(encoding='utf-8'))
 if cfg.get('name')!='BuildWright':err.append('buildwright.json name must be BuildWright')
 if cfg.get('version')!='0.7.0':err.append('buildwright.json version must be 0.7.0 for DROP 0007')
 comp=cfg.get('composition_system',{})
 if comp.get('templates')!=11:err.append('composition_system.templates must be 11')
 if comp.get('palettes')!=8:err.append('composition_system.palettes must be 8')
 if comp.get('example_modules')!=7:err.append('composition_system.example_modules must be 7')
 graph=cfg.get('project_graph_system',{})
 if graph.get('facade_profiles')!=4:err.append('project_graph_system.facade_profiles must be 4')
 if graph.get('example_projects')!=3:err.append('project_graph_system.example_projects must be 3')
 if not graph.get('facade_compiler'):err.append('facade compiler must be enabled')
 if not graph.get('site_compiler'):err.append('site compiler must be enabled')
except Exception as e:err.append(f'buildwright.json invalid: {e}')
if err:
 print('BUILDWRIGHT VALIDATION: FAIL');[print(' -',x) for x in err];sys.exit(1)
checks=[
 ('validate_packs.py',[]),('build_pack_index.py',['--check']),
 ('validate_microblocks.py',[]),('build_microblock_index.py',['--check']),
 ('validate_fixtures.py',[]),('compile_fixtures.py',['--check']),('build_fixture_index.py',['--check']),('validate_transform_corpus.py',[]),
 ('validate_composition.py',[]),('build_composition_index.py',['--check']),('compile_composition_examples.py',['--check']),
 ('validate_project_graph.py',[]),('compile_project_examples.py',['--check'])
]
for tool,args in checks:
 r=subprocess.run([sys.executable,str(ROOT/'tools'/tool),*args],cwd=ROOT)
 if r.returncode:sys.exit(r.returncode)
print('BUILDWRIGHT VALIDATION: PASS')
