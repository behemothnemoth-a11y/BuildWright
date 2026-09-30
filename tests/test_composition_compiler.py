from __future__ import annotations
import json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
if str(ROOT/'tools') not in sys.path:sys.path.insert(0,str(ROOT/'tools'))
from composition.transforms import transform_pos,transformed_size,transform_state,transform_grid_words
from composition.palette import PalettePlan
from composition.planner import plan_brief
from composition.compiler import compile_brief
from composition.geometry import box_for_connector
from litematic_codec import read

class TransformTests(unittest.TestCase):
    def test_horizontal_position_rotation(self):
        self.assertEqual(transformed_size((9,11,3),1),(3,11,9))
        self.assertEqual(transform_pos((0,0,0),(9,11,3),1),(2,0,0))
        self.assertEqual(transform_pos((8,0,2),(9,11,3),1),(0,0,8))

    def test_directional_state_rotation(self):
        s='minecraft:chiseled_bookshelf[facing=north,slot_0_occupied=false]'
        self.assertIn('facing=east',transform_state(s,1,'none'))
        vine='minecraft:vine[north=true,east=false,south=false,west=false,up=false]'
        out=transform_state(vine,1,'none')
        self.assertIn('east=true',out)

    def test_microblock_grid_rotation_preserves_count(self):
        words=[0]*64;words[0]=1 # cell 0,0,0
        out=transform_grid_words(words,1,'none')
        self.assertEqual(sum(x.bit_count() for x in out),1)
        # x=0,z=0 rotates to x=15,z=0 -> index 15
        self.assertTrue(out[0] & (1<<15))

class PaletteTests(unittest.TestCase):
    def test_shape_preserving_masonry_remap(self):
        p=PalettePlan(json.loads((ROOT/'composition/palettes/massive_gothic_manor.json').read_text()))
        out=p.remap('minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]')
        self.assertTrue(out.startswith('minecraft:tuff_brick_stairs['))
        self.assertIn('facing=north',out)

    def test_wood_family_remap(self):
        p=PalettePlan(json.loads((ROOT/'composition/palettes/massive_gothic_manor.json').read_text()))
        self.assertEqual(p.remap('minecraft:oak_log[axis=y]'),'minecraft:dark_oak_log[axis=y]')

class PlannerTests(unittest.TestCase):
    def test_examples_have_no_required_failures(self):
        for brief in sorted((ROOT/'examples/composition').glob('*.json')):
            plan=plan_brief(ROOT,brief)
            self.assertFalse([w for w in plan.warnings if w.startswith('REQUIRED:')],brief.name)

    def test_same_seed_same_plan(self):
        b=ROOT/'examples/composition/gothic_library_demo.json'
        a=plan_brief(ROOT,b).to_dict();c=plan_brief(ROOT,b).to_dict()
        self.assertEqual(a,c)

    def test_connector_keepout_not_occupied(self):
        brief=json.loads((ROOT/'examples/composition/gothic_grand_hall_demo.json').read_text())
        plan=plan_brief(ROOT,brief)
        for k in plan.keepouts:
            self.assertFalse(any(p.box.intersects(k) for p in plan.placements))

class CompileTests(unittest.TestCase):
    def test_generated_text_outputs_use_lf_bytes(self):
        import tempfile
        from composition.compiler import compile_brief
        brief=ROOT/'examples/composition/gothic_library_demo.json'
        with tempfile.TemporaryDirectory() as td:
            out=compile_brief(ROOT,brief,Path(td))
            for key in ('source','manifest','preview'):
                data=Path(out[key]).read_bytes()
                self.assertNotIn(b'\r\n',data,key)
                self.assertNotIn(b'\r',data,key)

    def test_compile_readback_and_connector_carve(self):
        brief_path=ROOT/'examples/composition/gothic_library_demo.json'
        brief=json.loads(brief_path.read_text())
        with tempfile.TemporaryDirectory() as td:
            r=compile_brief(ROOT,brief_path,Path(td))
            source=json.loads(r['source'].read_text());blocks={tuple(b['pos']) for b in source['blocks']}
            plan=r['plan']
            self.assertEqual(r['readback']['nonair'],len(blocks))
            for conn in plan.connectors:
                opening=box_for_connector(conn,plan.room_size,keepout=False)
                self.assertFalse(any(p in blocks for p in opening.cells()))

    def test_hybrid_compiles_real_astra_hosts(self):
        with tempfile.TemporaryDirectory() as td:
            r=compile_brief(ROOT,ROOT/'examples/composition/hybrid_gothic_detail_demo.json',Path(td))
            manifest=json.loads(r['manifest'].read_text())
            self.assertEqual(manifest['microblock_hosts'],4)
            nbt=read(r['litematic']);region=next(iter(nbt['Regions'].values()));tiles=region['TileEntities']
            self.assertEqual(len(tiles),4)
            for be in tiles:
                self.assertEqual(be['id'],'astra_microblocks:test_host')
                self.assertIn('grid_0',be);self.assertIn('grid_63',be)
                self.assertEqual(be['astra_orientation'],0)

    def test_committed_examples_pending_live_game(self):
        for p in (ROOT/'composition/compiled_examples').glob('*.manifest.json'):
            d=json.loads(p.read_text());self.assertEqual(d['maturity'],'OFFLINE_COMPILED');self.assertEqual(d['live_game_status'],'PENDING')

    def test_compiled_outputs_exist_for_every_brief(self):
        for b in (ROOT/'examples/composition').glob('*.json'):
            id=json.loads(b.read_text())['id']
            for suffix in ('litematic','source.json','manifest.json','plan.svg'):
                self.assertTrue((ROOT/'composition/compiled_examples'/f'{id}.{suffix}').is_file())

if __name__=='__main__':unittest.main()
