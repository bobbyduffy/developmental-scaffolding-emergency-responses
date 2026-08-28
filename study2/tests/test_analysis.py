import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]


class Study2AnalysisSmokeTests(unittest.TestCase):
    def test_synthetic_full_design_and_analysis(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            data = td / "results.jsonl"
            out = td / "analysis"
            subprocess.run([sys.executable, str(HERE / "generate_synthetic.py"), "--out", str(data)], check=True)
            rows = [json.loads(x) for x in data.read_text(encoding="utf-8").splitlines() if x.strip()]
            self.assertEqual(len(rows), 5760)
            self.assertEqual(len({r["trial_id"] for r in rows}), 5760)
            self.assertEqual({r["relationship"] for r in rows}, {"mommy","daddy","mom","dad","girlfriend","boyfriend","wife","husband"})
            subprocess.run([sys.executable, str(HERE / "analyze_results.py"), "--input", str(data), "--outdir", str(out)], check=True)
            result = json.loads((out / "confirmatory_results.json").read_text(encoding="utf-8"))
            self.assertEqual(result["input_rows"], 5760)
            self.assertGreater(result["primary"]["n"], 2500)
            self.assertEqual(result["primary"]["H1_relationship_omnibus"]["df"], 7)
            self.assertEqual(len(result["primary"]["H2_matched_contrasts"]), 4)
            self.assertEqual(result["primary"]["H3_pair_by_referent_sex_interaction"]["df"], 3)

    def test_presence_then_position_missingness(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            data = td / "results.jsonl"
            subprocess.run([sys.executable, str(HERE / "generate_synthetic.py"), "--out", str(data)], check=True)
            rows = [json.loads(x) for x in data.read_text(encoding="utf-8").splitlines() if x.strip()]
            emergency = [r for r in rows if r["emergency"] == 1]
            self.assertTrue(any(r["ems_instruction"] == 0 for r in emergency))
            self.assertTrue(any(r["first_911_word"] is None for r in emergency))
            for r in emergency:
                if r["ems_instruction"] == 0:
                    self.assertIsNone(r["first_ems_directive_word"])


if __name__ == "__main__":
    unittest.main()
