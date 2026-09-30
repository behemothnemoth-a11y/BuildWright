import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TestMicroblockCatalog(unittest.TestCase):
 def test_counts(self):
  r=json.loads((ROOT/'packs/microblock/registry.json').read_text())
  self.assertEqual(r['totals']['assets'], 606)
  self.assertEqual(r['totals']['pack_files'], 75)
  self.assertEqual(r['totals']['primitives'], 40)
 def test_unique_assets(self):
  idx=json.loads((ROOT/'packs/microblock/index.json').read_text())
  ids=[x['id'] for x in idx['assets']]
  self.assertEqual(len(ids),len(set(ids)))
 def test_all_assets_use_known_primitives(self):
  prim={x['id'] for x in json.loads((ROOT/'packs/microblock/primitives.json').read_text())['primitives']}
  r=json.loads((ROOT/'packs/microblock/registry.json').read_text())
  for e in r['catalog']:
   p=json.loads((ROOT/e['path']).read_text())
   for a in p['assets']:
    self.assertTrue(set(a['recommended_primitives']).issubset(prim),a['id'])
 def test_provider_grid(self):
  p=json.loads((ROOT/'packs/microblock/providers/astra_microblocks_0_4_0.json').read_text())
  self.assertEqual(p['grid']['cells_per_axis'],16); self.assertEqual(p['grid']['cells_per_host'],4096)
if __name__=='__main__': unittest.main()
