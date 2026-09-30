import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class T(unittest.TestCase):
 def setUp(self):self.r=json.loads((ROOT/'fixtures/registry.json').read_text())
 def test_counts(self):self.assertEqual(self.r['counts'],{'vanilla':40,'microblock':24,'transform_cases':32})
 def test_unique(self):ids=[x['id'] for x in self.r['fixtures']];self.assertEqual(len(ids),len(set(ids)))
 def test_files(self):
  for x in self.r['fixtures']:self.assertTrue((ROOT/x['file']).is_file(),x['id'])
if __name__=='__main__':unittest.main()
