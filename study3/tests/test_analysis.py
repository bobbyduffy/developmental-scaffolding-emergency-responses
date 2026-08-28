from __future__ import annotations

import unittest
import pandas as pd

import analyze_results as a


class AnalysisTests(unittest.TestCase):
    def synthetic_frame(self):
        rows=[]
        relationships=["mommy","daddy","mom","dad","girlfriend","boyfriend","wife","husband"]
        for model in ["claude-sonnet-5","gpt-5.6-terra"]:
            for sys in ["none","minimal","assistant"]:
                for rel_i,rel in enumerate(relationships):
                    for variant in ["A","B"]:
                        for certainty in [1,2,3,4]:
                            for rep in range(8):
                                ems=0 if (certainty==1 and rep==0) else 1
                                pos=None if not ems else 8 + (4-certainty)*3 + (rel_i%4) + (1 if variant=="B" else 0)
                                rows.append({"status":"ok","empty_response":False,"truncated":False,"relationship":rel,"certainty":certainty,"prompt_variant":variant,"model_key":model,"sysprompt_condition":sys,"ems_instruction":ems,"first_ems_directive_word":pos,"ems_priority_opening":None if not ems else int(pos<=12),"ems_within_10_words":None if not ems else int(pos<=10)})
        return pd.DataFrame(rows)

    def test_primary_model_has_21_interaction_terms(self):
        df=self.synthetic_frame(); lat=df[(df.ems_instruction==1)&df.first_ems_directive_word.notna()]
        m=a.fit_hc3(lat,a.PRIMARY_FORMULA)
        self.assertEqual(len(a.interaction_names(m)),21)

    def test_three_way_has_21_terms(self):
        df=self.synthetic_frame(); lat=df[(df.ems_instruction==1)&df.first_ems_directive_word.notna()]
        m=a.fit_hc3(lat,a.HET_FORMULA)
        self.assertEqual(len(a.interaction_names(m,require_variant=True)),21)

    def test_full_analysis_executes(self):
        out=a.analyze(self.synthetic_frame())
        self.assertIn("H1_relationship_x_certainty",out)
        self.assertEqual(len(out["pair_attenuation"]),4)
        self.assertEqual(out["n_input"],len(self.synthetic_frame()))


if __name__ == "__main__":
    unittest.main()
