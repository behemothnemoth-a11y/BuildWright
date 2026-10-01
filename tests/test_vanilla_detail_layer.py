from __future__ import annotations
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
if str(ROOT/'tools') not in sys.path:
    sys.path.insert(0,str(ROOT/'tools'))

from litematic_codec import read
from composition.compiler import compile_brief

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def manifest_map(folder):
    out={}
    for p in Path(folder).glob('*.manifest.json'):
        data=load(p)
        out[data.get('id') or data.get('brief_id')]=data
    return out

class VanillaDetailFixtureTests(unittest.TestCase):
    def test_detail_fixture_counts(self):
        reg=load(ROOT/'fixtures/registry.json')
        self.assertEqual(reg['counts']['vanilla'],85)
        self.assertEqual(reg['counts']['detail_vanilla'],45)
        detail=[x for x in reg['fixtures'] if x.get('detail_fixture')]
        self.assertEqual(len(detail),45)
        self.assertTrue(all(x['stage']=='vanilla' for x in detail))

    def test_detail_fixture_sources_are_vanilla_only(self):
        reg=load(ROOT/'fixtures/registry.json')
        for item in reg['fixtures']:
            if not item.get('detail_fixture'):
                continue
            src=load(ROOT/item['source'])
            self.assertEqual(src['stage'],'vanilla',item['id'])
            for block in src['blocks']:
                self.assertTrue(block['state'].startswith('minecraft:'),f"{item['id']} {block['state']}")
                self.assertNotIn('astra_microblocks:',block['state'])

class VanillaDetailProfileTests(unittest.TestCase):
    def test_role_profile_coverage(self):
        data=load(ROOT/'composition/detail_profiles.json')
        expected={'default','bedroom','dining','gallery','garden','hall','industrial','library','tavern','workshop'}
        self.assertEqual(set(data['profiles']),expected)
        for role,profile in data['profiles'].items():
            self.assertGreaterEqual(float(profile['density']),0)
            self.assertLessEqual(float(profile['density']),1)
            self.assertIn('surfaces',profile)
            self.assertIn('recipes',profile)

class DetailedExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.detail=manifest_map(ROOT/'composition/detailed_examples')
        cls.base=manifest_map(ROOT/'composition/compiled_examples')

    def test_ten_room_role_examples(self):
        self.assertEqual(len(self.detail),10)
        roles=set()
        for ident,m in self.detail.items():
            self.assertEqual(m['detail_status'],'VANILLA_DETAIL_COMPLETE',ident)
            self.assertEqual(int(m.get('microblock_hosts',0) or 0),0,ident)
            d=m['vanilla_detail']
            self.assertTrue(d['enabled'],ident)
            self.assertFalse(d['astra_microblocks'],ident)
            self.assertGreater(d['fixtures_placed']+d['surface_blocks'],0,ident)
            roles.add(d['role'])
        self.assertEqual(roles,{'bedroom','dining','gallery','garden','hall','industrial','library','tavern','workshop'})

    def test_detail_outputs_have_substantial_vanilla_geometry(self):
        for ident,m in self.detail.items():
            self.assertGreater(m['block_count'],1000,ident)
            self.assertGreater(m['readback']['nonair'],1000,ident)

    def test_cross_style_detail_smoke(self):
        cases=[
          ('style.modern_luxury','composition.modern_neutral'),
          ('style.japanese_traditional','composition.garden_estate'),
          ('style.ancient_ruin','composition.ancient_ruin'),
          ('style.coastal_mediterranean','composition.garden_estate'),
        ]
        for index,(style,palette) in enumerate(cases):
            brief={
              'schema_version':1,
              'id':f'cross_style_detail_{index}',
              'name':f'Cross Style Detail {index}',
              'stage':'vanilla',
              'template':'bedroom_suite',
              'size':[31,13,27],
              'seed':22000+index,
              'style_profile':style,
              'palette':palette,
              'fixture_policy':{'density':0.82,'max_repeats':3},
              'vanilla_detail':{'enabled':True,'role':'bedroom','density':0.8}
            }
            with tempfile.TemporaryDirectory() as td:
                result=compile_brief(ROOT,brief,Path(td))
                manifest=load(result['manifest'])
                self.assertEqual(manifest['detail_status'],'VANILLA_DETAIL_COMPLETE',style)
                self.assertEqual(int(manifest.get('microblock_hosts',0) or 0),0,style)
                self.assertFalse(manifest['vanilla_detail']['astra_microblocks'],style)
                self.assertGreater(manifest['vanilla_detail']['fixtures_placed']+manifest['vanilla_detail']['surface_blocks'],0,style)

class DetailedProjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.detail=manifest_map(ROOT/'project_graph/detailed_examples')
        cls.base=manifest_map(ROOT/'project_graph/compiled_examples')

    def test_three_detailed_projects(self):
        self.assertEqual(len(self.detail),3)
        for ident,m in self.detail.items():
            self.assertEqual(m['detail_status'],'VANILLA_DETAIL_COMPLETE',ident)
            self.assertEqual(int(m.get('block_entities',0) or 0),0,ident)
            finish=m['vanilla_finish']
            self.assertTrue(finish['enabled'],ident)
            self.assertFalse(finish['astra_microblocks'],ident)
            added=sum(int(finish.get(k,0) or 0) for k in ('entrance_blocks','lighting_blocks','vegetation_blocks','roof_detail_blocks','service_blocks'))
            self.assertGreater(added,0,ident)

    def test_project_finish_records_added_geometry(self):
        for ident,m in self.detail.items():
            finish=m['vanilla_finish']
            added=sum(int(finish.get(k,0) or 0) for k in (
                'entrance_blocks','lighting_blocks','vegetation_blocks',
                'roof_detail_blocks','service_blocks'
            ))
            self.assertGreater(added,0,ident)

if __name__=='__main__':
    unittest.main()
