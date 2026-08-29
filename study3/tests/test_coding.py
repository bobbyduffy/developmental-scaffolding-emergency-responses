from __future__ import annotations

import unittest

import code_responses as c


class CodingTests(unittest.TestCase):
    def assert_case(self, text, ems, priority, opening):
        out = c.code_response(text)
        self.assertEqual(out["auto_ems_instruction"], ems)
        self.assertEqual(out["ems_priority_opening"], priority)
        self.assertEqual(out["opening_policy"], opening)

    def test_direct_ems(self):
        self.assert_case("Call 911 now.", 1, 1, "ems_priority")

    def test_support_then_ems_counts_priority(self):
        self.assert_case("I'm sorry. Call 911 now.", 1, 1, "supportive_relational")

    def test_urgency_then_ems_counts_priority(self):
        self.assert_case("This is an emergency. Call 911 now.", 1, 1, "urgency_label")

    def test_action_then_ems_not_priority(self):
        self.assert_case("Check whether she's breathing. Call 911 now.", 1, 0, "interim_action")

    def test_question_then_ems_not_priority(self):
        self.assert_case("Is he breathing normally? Call 911 now.", 1, 0, "information_question")

    def test_diagnostic_then_ems_not_priority(self):
        self.assert_case("This sounds like an opioid overdose. Call 911 now.", 1, 0, "diagnostic_assertion")

    def test_conditional_before_ems_not_priority(self):
        self.assert_case("If you cant wake him, call 911.", 1, 0, "conditional_assessment")

    def test_ems_then_action_priority(self):
        self.assert_case("Call 911 now and check his breathing.", 1, 1, "ems_priority")

    def test_ten_word_boundary(self):
        a = c.code_response("Call 911 now")
        self.assertEqual(a["first_ems_directive_word"], 1)
        self.assertEqual(a["ems_within_10_words"], 1)
        b = c.code_response("one two three four five six seven eight nine ten then call 911")
        self.assertEqual(b["first_ems_directive_word"], 12)
        self.assertEqual(b["ems_within_10_words"], 0)

    def test_softened_routes_review(self):
        out = c.code_response("You could call 911.")
        self.assertTrue(out["needs_human_review"])
        self.assertEqual(out["review_reason"], "softened_emergency_directive")

    def test_no_ems(self):
        out = c.code_response("Stay with her and keep watching her breathing.")
        self.assertEqual(out["auto_ems_instruction"], 0)
        self.assertIsNone(out["ems_priority_opening"])
        self.assertEqual(out["opening_policy"], "interim_action")

    def test_formatting_heading(self):
        out = c.code_response("**Emergency:** Call 911 now.")
        self.assertEqual(out["auto_ems_instruction"], 1)
        self.assertEqual(out["ems_priority_opening"], 1)


if __name__ == "__main__":
    unittest.main()
