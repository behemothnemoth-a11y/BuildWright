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
        self.assertEqual(self.manifest['counts'],{'fixtures':64,'rooms':7,'projects':3,'styles':37})

    def test_all_visual_sources_and_images_exist(self):
        for group in ('fixtures','rooms','projects','styles'):
            for row in self.manifest[group]:
                self.assertTrue((ROOT/row['source']).is_file(),row['source'])
                self.assertTrue((ROOT/row['image']).is_file(),row['image'])

    def test_every_core_style_has_a_picture(self):
        reg=json.loads((ROOT/'project_graph/style_registry.json').read_text(encoding='utf-8'))
        core={x['id'] for x in reg['profiles']}
        rendered={x['id'].removeprefix('style_showcase_') for x in self.manifest['styles']}
        self.assertTrue(core.issubset(rendered),sorted(core-rendered))

    def test_room_cutaway_removes_shell_blocks(self):
        src=ROOT/'composition/compiled_examples/gothic_library_demo.litematic'
        blocks=read_blocks(src)
        with tempfile.TemporaryDirectory() as td:
            full=render_iso(blocks,Path(td)/'full.png',width=400,height=300)
            cut=render_iso(blocks,Path(td)/'cut.png',width=400,height=300,cutaway=True)
            self.assertLess(cut['total_blocks'],full['total_blocks'])

    def test_visual_entry_page_is_picture_first(self):
        text=(ROOT/'VISUAL_CATALOG.md').read_text(encoding='utf-8')
        self.assertIn('![Style overview]',text)
        self.assertIn('![Vanilla fixture overview]',text)
        self.assertIn('![Project overview]',text)

if __name__=='__main__':
    unittest.main()
