import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class T(unittest.TestCase):
 def test_word_count_and_cells(self):
  for p in (ROOT/'fixtures/sources/microblock').glob('*.json'):
   d=json.loads(p.read_text());self.assertEqual(len(d['occupancy_words_hex']),64);self.assertGreater(d['occupied_cells'],0);self.assertLessEqual(d['occupied_cells'],4096)
if __name__=='__main__':unittest.main()
