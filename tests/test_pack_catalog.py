import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TestCatalog(unittest.TestCase):
 def test_counts(self):
  r=json.loads((ROOT/'packs/registry.json').read_text())
  self.assertEqual(r['totals']['assets'], 567)
  self.assertEqual(r['totals']['pack_files'], 68)
 def test_unique_assets(self):
  idx=json.loads((ROOT/'packs/index.json').read_text())
  ids=[x['id'] for x in idx['assets']]
  self.assertEqual(len(ids),len(set(ids)))
 def test_style_profiles_exist(self):
  r=json.loads((ROOT/'packs/registry.json').read_text())
  for x in r['style_profiles']: self.assertTrue((ROOT/x['path']).is_file())
if __name__=='__main__': unittest.main()
