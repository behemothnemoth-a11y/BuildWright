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

from project_graph.compiler import compile_project
from project_graph.model import load_project
from project_graph.style import blend_profiles, load_profile, resolve_style

class StyleRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry=json.loads((ROOT/"project_graph/style_registry.json").read_text(encoding="utf-8"))

    def test_broad_profile_coverage(self):
        self.assertGreaterEqual(self.registry["count"],30)
        self.assertGreaterEqual(len(self.registry["families"]),12)

    def test_material_roles_and_semantics(self):
        required={"wall","structure","trim","accent","glass","plinth","roof"}
        for item in self.registry["profiles"]:
            p=load_profile(ROOT,item["id"])
            self.assertTrue(required.issubset(p["material_roles"]),item["id"])
            self.assertIn("window_shape",p)
            self.assertIn("facade_rhythm",p)
            self.assertIn("default_roof",p)
            self.assertIn("zone_presets",p)
            self.assertIn("massing",p)

    def test_styles_are_not_project_scoped(self):
        # Core profile IDs describe architecture, not a specific BuildWright project.
        project_words={"wayne","blackglass","cthulhu","fort_garry","redfield"}
        for item in self.registry["profiles"]:
            self.assertFalse(any(word in item["id"] for word in project_words),item["id"])

class StyleBlendTests(unittest.TestCase):
    def test_blend_keeps_primary_language_and_blends_numeric_bias(self):
        a=load_profile(ROOT,"modern")
        b=load_profile(ROOT,"industrial")
        mixed=blend_profiles(a,b,0.4)
        self.assertEqual(mixed["window_shape"],a["window_shape"])
        self.assertEqual(len(mixed["style_influences"]),2)
        self.assertNotEqual(mixed["ornament_density"],a["ornament_density"])

    def test_explicit_material_role_override(self):
        brief={
            "id":"blend_test","modules":[{"id":"room","source":"composition/compiled_examples/victorian_bedroom_demo.source.json","origin":[0,0,0]}],
            "style":{"primary":"japanese_traditional","secondary":"modern","blend":0.3,
                     "material_roles":{"accent":"minecraft:gold_block"}}
        }
        style=resolve_style(ROOT,brief)
        self.assertEqual(style["accent_state"],"minecraft:gold_block")
        self.assertIn("style_influences",style)

class StyleCompileSmokeTests(unittest.TestCase):
    def test_every_registered_style_compiles(self):
        registry=json.loads((ROOT/"project_graph/style_registry.json").read_text(encoding="utf-8"))
        for item in registry["profiles"]:
            pid=item["id"]
            brief={
                "schema_version":1,"id":"style_"+pid,"facade_profile":pid,
                "modules":[{"id":"room","source":"composition/compiled_examples/victorian_bedroom_demo.source.json","origin":[0,0,0]}],
                "connections":[],"site":{"enabled":False}
            }
            with tempfile.TemporaryDirectory() as td:
                result=compile_project(ROOT,brief,Path(td))
                manifest=json.loads(Path(result["manifest"]).read_text(encoding="utf-8"))
                self.assertGreater(manifest["blocks"],1000,pid)
                self.assertGreater(manifest["facade"]["sides"],0,pid)
                self.assertGreater(manifest["roof"]["modules"],0,pid)

if __name__=="__main__":
    unittest.main()
