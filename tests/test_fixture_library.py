import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from composition.fixture_library import FixtureLibrary

class T(unittest.TestCase):
 def setUp(self):self.r=json.loads((ROOT/'fixtures/registry.json').read_text())
 def test_counts(self):self.assertEqual(self.r['counts'],{'vanilla':85,'microblock':24,'transform_cases':32,'detail_vanilla':45})
 def test_unique(self):
  ids=[x['id'] for x in self.r['fixtures']];self.assertEqual(len(ids),len(set(ids)))
 def test_files(self):
  for x in self.r['fixtures']:self.assertTrue((ROOT/x['file']).is_file(),x['id'])
 def test_primary_library_excludes_detail_fixtures_by_default(self):
  lib=FixtureLibrary(ROOT)
  default_ids={x.id for x in lib.search(stage='vanilla')}
  detail_ids={x['id'] for x in self.r['fixtures'] if x.get('detail_fixture')}
  self.assertTrue(detail_ids)
  self.assertTrue(default_ids.isdisjoint(detail_ids))
  optin_ids={x.id for x in lib.search(stage='vanilla',include_detail_fixtures=True)}
  self.assertTrue(detail_ids.issubset(optin_ids))

if __name__=='__main__':unittest.main()
