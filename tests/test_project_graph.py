from __future__ import annotations
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from project_graph.compiler import compile_project
from project_graph.model import load_project, port_for
from project_graph.solver import solve_project, world_port

class GraphSolveTests(unittest.TestCase):
    def test_wayne_attach_and_corridor_solve(self):
        brief = ROOT / "examples/projects/wayne_manor_phase_a.json"
        plan = load_project(ROOT, brief)
        placed = solve_project(plan)
        self.assertEqual(set(placed), {"grand_hall", "library", "suite", "garden"})
        hall = placed["grand_hall"]
        library = placed["library"]
        self.assertEqual(hall.box[3], library.box[0])
        garden = placed["garden"]
        self.assertEqual(hall.box[2] - garden.box[5] - 1, 7)

    def test_vertical_port_alignment(self):
        plan = load_project(ROOT, ROOT / "examples/projects/two_floor_manor.json")
        placed = solve_project(plan)
        hall = plan.modules["hall"]
        suite = plan.modules["upper_suite"]
        a = world_port(placed["hall"].origin, port_for(hall, "upper"))
        b = world_port(placed["upper_suite"].origin, port_for(suite, "down"))
        self.assertEqual(a.pos, b.pos)

class CompileTests(unittest.TestCase):
    def test_industrial_corridor_compiles(self):
        brief = ROOT / "examples/projects/industrial_campus.json"
        with tempfile.TemporaryDirectory() as td:
            result = compile_project(ROOT, brief, Path(td))
            manifest = json.loads(Path(result["manifest"]).read_text(encoding="utf-8"))
            self.assertEqual(manifest["modules"], 2)
            self.assertEqual(manifest["connections"], 1)
            self.assertGreater(manifest["blocks"], 1000)
            self.assertGreater(manifest["site"]["ground_blocks"], 0)

    def test_wayne_facade_and_roof_are_active(self):
        with tempfile.TemporaryDirectory() as td:
            result = compile_project(ROOT, ROOT / "examples/projects/wayne_manor_phase_a.json", Path(td))
            manifest = json.loads(Path(result["manifest"]).read_text(encoding="utf-8"))
            self.assertGreater(manifest["facade"]["piers"], 0)
            self.assertGreater(manifest["facade"]["windows"], 0)
            self.assertGreater(manifest["roof"]["modules"], 0)
            self.assertEqual(manifest["live_game_status"], "PENDING")

    def test_generated_text_is_lf_and_deterministic(self):
        brief = ROOT / "examples/projects/two_floor_manor.json"
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            first = compile_project(ROOT, brief, Path(a))
            second = compile_project(ROOT, brief, Path(b))
            for key in ("source", "manifest", "preview"):
                p1 = Path(first[key])
                p2 = Path(second[key])
                data = p1.read_bytes()
                self.assertNotIn(b"\r\n", data)
                self.assertEqual(data, p2.read_bytes(), key)
            self.assertEqual(Path(first["litematic"]).read_bytes(), Path(second["litematic"]).read_bytes())

    def test_readback_matches_final_block_count(self):
        with tempfile.TemporaryDirectory() as td:
            result = compile_project(ROOT, ROOT / "examples/projects/two_floor_manor.json", Path(td))
            manifest = json.loads(Path(result["manifest"]).read_text(encoding="utf-8"))
            self.assertEqual(result["readback"]["nonair"], manifest["blocks"])

class CommittedExampleTests(unittest.TestCase):
    def test_compiled_examples_exist_and_pending_live_game(self):
        compiled = ROOT / "project_graph" / "compiled_examples"
        for brief_path in (ROOT / "examples" / "projects").glob("*.json"):
            project_id = json.loads(brief_path.read_text(encoding="utf-8"))["id"]
            manifest_path = compiled / f"{project_id}.manifest.json"
            self.assertTrue(manifest_path.is_file(), project_id)
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["maturity"], "OFFLINE_COMPILED")
            self.assertEqual(manifest["live_game_status"], "PENDING")
            for suffix in ("litematic", "project.json", "plan.svg"):
                self.assertTrue((compiled / f"{project_id}.{suffix}").is_file())

if __name__ == "__main__":
    unittest.main()
