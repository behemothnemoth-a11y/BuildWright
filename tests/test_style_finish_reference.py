from __future__ import annotations
import json,sys,tempfile,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
if str(ROOT/"tools") not in sys.path:sys.path.insert(0,str(ROOT/"tools"))

from project_graph.compiler import compile_project
from project_graph.reference_fit import inject_reference_origins
from litematic_codec import read

def load(path):return json.loads(Path(path).read_text(encoding="utf-8"))
def manifests():
    return {load(p)["id"]:load(p) for p in (ROOT/"project_graph/style_finish_examples").glob("*.manifest.json")}

class StyleFinishTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.m=manifests()

    def test_all_14_families_have_regressions(self):
        expected={"ancient","classical","desert","east_asian","fantasy","gothic","historic_european","industrial","mediterranean","modern","modern_historic","organic","speculative","vernacular"}
        actual={m["style_finish"]["family"] for m in self.m.values()}
        self.assertEqual(actual,expected)
        self.assertEqual(len(self.m),14)

    def test_every_family_adds_visible_vanilla_finish(self):
        for ident,m in self.m.items():
            sf=m["style_finish"]
            self.assertTrue(sf["enabled"],ident)
            self.assertEqual(sf["status"],"VANILLA_STYLE_FINISH_COMPLETE",ident)
            self.assertGreater(sf["total_blocks"],50,ident)
            self.assertFalse(sf["astra_microblocks"],ident)

    def test_family_finishes_are_not_all_same_shape(self):
        signatures={
            (
              m["style_finish"]["band_blocks"],m["style_finish"]["corner_blocks"],
              m["style_finish"]["eave_blocks"],m["style_finish"]["service_blocks"],
              m["style_finish"]["parapet_blocks"],m["style_finish"]["finial_blocks"]
            )
            for m in self.m.values()
        }
        self.assertGreaterEqual(len(signatures),10)

    def test_style_finish_outputs_are_pure_vanilla(self):
        for path in (ROOT/"project_graph/style_finish_examples").glob("*.litematic"):
            root=read(path)
            for region in root["Regions"].values():
                names=[str(x.get("Name","")) for x in region["BlockStatePalette"]]
                self.assertFalse(any(n.startswith("astra_microblocks:") for n in names),path.name)
                self.assertFalse(any(str(be.get("id","")).startswith("astra_microblocks:") for be in region.get("TileEntities",[])),path.name)

class ReferenceFitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m=manifests()

    def test_committed_strict_reference_fit_passes(self):
        m=self.m["style_finish_classical"]
        ref=m["reference_fit"]
        self.assertEqual(ref["status"],"PASS")
        self.assertTrue(ref["strict"])
        self.assertEqual(ref["max_error"],0)
        self.assertGreaterEqual(ref["checks"],4)

    def test_strict_reference_fit_rejects_drift(self):
        brief=load(ROOT/"examples/style_finish/classical.json")
        brief["id"]="reference_drift_test"
        brief["reference_fit"]["target_size"]=[99,13,27]
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):
                compile_project(ROOT,brief,Path(td))

    def test_reference_fit_can_inject_measured_origin(self):
        brief={
          "schema_version":1,"id":"origin_inject",
          "modules":[{"id":"room","source":"composition/detailed_examples/bedroom_detail_complete.source.json"}],
          "reference_fit":{"enabled":True,"apply_module_origins":True,"module_targets":[{"module":"room","origin":[12,3,9]}]}
        }
        out=inject_reference_origins(brief)
        self.assertEqual(out["modules"][0]["origin"],[12,3,9])

if __name__=="__main__":unittest.main()
