import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class T(unittest.TestCase):
 def test_full_orientation_set(self):
  d=json.loads((ROOT/'fixtures/corpus/transform_manifest.json').read_text());by={}
  for c in d['cases']:by.setdefault(c['fixture'],set()).add(c['orientation'])
  self.assertEqual(len(by),4)
  for s in by.values():self.assertEqual(s,set(range(8)))
if __name__=='__main__':unittest.main()
