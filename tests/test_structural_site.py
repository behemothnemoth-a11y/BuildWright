from __future__ import annotations
import json,sys,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
if str(ROOT/'tools') not in sys.path:sys.path.insert(0,str(ROOT/'tools'))

from project_graph.model import load_project
from project_graph.solver import solve_project
from litematic_codec import read

def load(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def manifests():
    return {load(p)['id']:load(p) for p in (ROOT/'project_graph/structural_examples').glob('*.manifest.json')}

class StructuralSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.m=manifests()

    def test_three_regression_projects(self):
        self.assertEqual(set(self.m),{'routed_gothic_estate','terraced_hillside_compound','modern_campus_network'})

    def test_routed_corridors(self):
        for ident in ('routed_gothic_estate','modern_campus_network'):
            c=self.m[ident]['circulation']
            self.assertEqual(c['routed'],1,ident)
            self.assertGreater(c['route_length'],20,ident)
            self.assertGreater(c['route_blocks'],100,ident)

    def test_hillside_stairs_and_foundation(self):
        m=self.m['terraced_hillside_compound']
        self.assertEqual(m['circulation']['stairs'],1)
        self.assertGreater(m['foundations']['blocks'],0)
        self.assertGreater(m['foundations']['max_drop'],0)
        self.assertGreater(m['site']['retaining_blocks'],0)

    def test_structural_nodes(self):
        gothic=self.m['routed_gothic_estate']['structures']
        self.assertGreaterEqual(gothic['nodes'],4)
        for kind in ('tower','buttress_run','porch','balcony'):
            self.assertIn(kind,gothic['by_type'])

    def test_site_networks(self):
        modern=self.m['modern_campus_network']['site']
        self.assertEqual(modern['networks'],3)
        self.assertGreater(modern['road_blocks'],0)
        self.assertGreater(modern['plaza_blocks'],0)
        self.assertGreater(modern['fence_blocks'],0)

    def test_routed_connections_preserve_explicit_origins(self):
        brief=ROOT/'examples/structural_site/routed_gothic_estate.json'
        data=load(brief);plan=load_project(ROOT,brief);placed=solve_project(plan)
        expected={m['id']:tuple(m['origin']) for m in data['modules']}
        self.assertEqual({k:v.origin for k,v in placed.items()},expected)

    def test_all_structural_examples_are_pure_vanilla(self):
        for path in (ROOT/'project_graph/structural_examples').glob('*.litematic'):
            root=read(path)
            for region in root['Regions'].values():
                names=[str(x.get('Name','')) for x in region['BlockStatePalette']]
                self.assertFalse(any(n.startswith('astra_microblocks:') for n in names),path.name)
                self.assertFalse(any(str(be.get('id','')).startswith('astra_microblocks:') for be in region.get('TileEntities',[])),path.name)

if __name__=='__main__':unittest.main()
