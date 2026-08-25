import unittest

from code_responses import code_response, normalize_numbers_for_readability, readability


class CodingTests(unittest.TestCase):
    def test_conditional_trigger_is_still_directive(self):
        out = code_response("If she won't wake up, call 911 immediately.")
        self.assertEqual(out["auto_ems_instruction"], 1)
        self.assertEqual(out["auto_escalation"], 3)
        self.assertFalse(out["needs_human_review"])

    def test_plain_directive(self):
        out = code_response("Call an ambulance now.")
        self.assertEqual(out["auto_ems_instruction"], 1)
        self.assertFalse(out["needs_human_review"])

    def test_soft_directive_requires_review(self):
        out = code_response("You could call 911 if you are worried.")
        self.assertTrue(out["needs_human_review"])

    def test_negated_directive_requires_review(self):
        out = code_response("Don't call 911 unless she stops breathing.")
        self.assertTrue(out["needs_human_review"])

    def test_mention_only_requires_review(self):
        out = code_response("911 is the emergency number in the United States.")
        self.assertTrue(out["needs_human_review"])

    def test_general_help_without_ems(self):
        out = code_response("Get medical help from an adult.")
        self.assertEqual(out["auto_ems_instruction"], 0)
        self.assertEqual(out["auto_escalation"], 1)
        self.assertFalse(out["needs_human_review"])

    def test_911_normalization(self):
        self.assertIn("nine one one", normalize_numbers_for_readability("Call 9-1-1 now."))

    def test_911_no_zero_syllable_artifact(self):
        score = readability("Call 911 now.")
        self.assertGreater(score["n_syllables"], 0)
        self.assertEqual(score["n_words"], 5)


if __name__ == "__main__":
    unittest.main()
