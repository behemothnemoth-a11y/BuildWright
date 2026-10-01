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

from render_litematic_iso import read_blocks, render_iso

class VisualCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=json.loads((ROOT/'catalog/visual/visual_manifest.json').read_text(encoding='utf-8'))

    def test_expected_counts(self):
        self.assertEqual(self.manifest['counts'],{
            'vanilla_fixtures':85,
            'vanilla_rooms':6,
            'vanilla_projects':3,
            'vanilla_style_baselines':37,
            'vanilla_detail_rooms':10,
            'vanilla_detail_projects':3,
            'microblock_fixtures':24,
            'hybrid_rooms':1
        })

    def test_all_visual_sources_and_images_exist(self):
        groups=[
            self.manifest['vanilla']['fixtures'],
            self.manifest['vanilla']['rooms'],
            self.manifest['vanilla']['projects'],
            self.manifest['vanilla']['style_baselines'],
            self.manifest['vanilla']['detail_complete_rooms'],
            self.manifest['vanilla']['detail_complete_projects'],
            self.manifest['optional_microblock']['fixtures'],
            self.manifest['optional_microblock']['hybrid_rooms']
        ]
        for rows in groups:
            for row in rows:
                self.assertTrue((ROOT/row['source']).is_file(),row['source'])
                self.assertTrue((ROOT/row['image']).is_file(),row['image'])

    def test_main_catalogue_is_vanilla_only(self):
        for row in self.manifest['vanilla']['fixtures']:
            self.assertEqual(row['stage'],'vanilla')
        for key in ('rooms','projects','style_baselines','detail_complete_rooms','detail_complete_projects'):
            for row in self.manifest['vanilla'][key]:
                self.assertFalse(row.get('uses_astra_microblocks',False),row['id'])

    def test_microblock_assets_are_separate(self):
        self.assertEqual(len(self.manifest['optional_microblock']['fixtures']),24)
        self.assertEqual(len(self.manifest['optional_microblock']['hybrid_rooms']),1)
        text=(ROOT/'MICROBLOCK_CATALOG.md').read_text(encoding='utf-8')
        self.assertIn('optional refinement layer',text.lower())

    def test_every_core_style_has_a_picture(self):
        reg=json.loads((ROOT/'project_graph/style_registry.json').read_text(encoding='utf-8'))
        core={x['id'] for x in reg['profiles']}
        rendered={x['id'].removeprefix('style_showcase_') for x in self.manifest['vanilla']['style_baselines']}
        self.assertTrue(core.issubset(rendered),sorted(core-rendered))

    def test_room_cutaway_removes_shell_blocks(self):
        src=ROOT/'composition/compiled_examples/gothic_library_demo.litematic'
        blocks=read_blocks(src)
        with tempfile.TemporaryDirectory() as td:
            full=render_iso(blocks,Path(td)/'full.png',width=400,height=300)
            cut=render_iso(blocks,Path(td)/'cut.png',width=400,height=300,cutaway=True)
            self.assertLess(cut['total_blocks'],full['total_blocks'])

    def test_visual_entry_page_explains_baseline(self):
        text=(ROOT/'VISUAL_CATALOG.md').read_text(encoding='utf-8')
        self.assertIn('vanilla foundation',text.lower())
        self.assertIn('not the completed vanilla detail layer',text.lower())
        self.assertIn('vanilla detail complete',text.lower())
        self.assertIn('MICROBLOCK_CATALOG.md',text)

if __name__=='__main__':
    unittest.main()
