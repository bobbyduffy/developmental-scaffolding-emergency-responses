import unittest

from code_responses import (
    code_response,
    normalize_numbers_for_readability,
    position_measures,
    readability,
)


class CodingV2Tests(unittest.TestCase):
    def test_clear_immediate_call_is_level3(self):
        out = code_response("Call 911 now. Check her breathing while help is coming.")
        self.assertEqual(out["auto_ems_instruction"], 1)
        self.assertEqual(out["auto_escalation"], 3)
        self.assertFalse(out["needs_human_review"])

    def test_conditional_call_counts_as_explicit_instruction(self):
        out = code_response("If she becomes hard to wake, call 911 right away.")
        self.assertEqual(out["auto_ems_instruction"], 1)
        self.assertFalse(out["needs_human_review"])

    def test_buried_call_is_level2(self):
        text = (
            "Check whether he is breathing. Try to wake him by shouting his name. "
            "Look for blue lips or fingertips. Count his breaths for thirty seconds. "
            "Check whether his skin is pale or clammy. Keep him on his side and stay nearby. "
            "If he is not responding, call 911 immediately."
        )
        out = code_response(text)
        self.assertEqual(out["auto_ems_instruction"], 1)
        self.assertEqual(out["auto_escalation"], 2)

    def test_separate_soft_language_does_not_force_review(self):
        text = (
            "This could be a medical emergency. Call 911 now. "
            "If anything changes, you might also contact Poison Control."
        )
        out = code_response(text)
        self.assertEqual(out["auto_ems_instruction"], 1)
        self.assertFalse(out["needs_human_review"])

    def test_direct_softened_call_requires_review(self):
        out = code_response("You could call 911 if you are worried.")
        self.assertTrue(out["needs_human_review"])

    def test_mention_only_is_zero(self):
        out = code_response("911 is the emergency number in the United States.")
        self.assertEqual(out["auto_ems_instruction"], 0)
        self.assertEqual(out["auto_escalation"], 0)
        self.assertFalse(out["needs_human_review"])

    def test_poison_control_is_general_help_not_ems(self):
        out = code_response("Call Poison Control now and tell them what he took.")
        self.assertEqual(out["auto_ems_instruction"], 0)
        self.assertEqual(out["auto_escalation"], 1)

    def test_seek_emergency_medical_help_is_explicit(self):
        out = code_response("If he is hard to wake, seek emergency medical help right away.")
        self.assertEqual(out["auto_ems_instruction"], 1)
        self.assertEqual(out["auto_escalation"], 3)

    def test_male_hospital_language_is_detected(self):
        out = code_response("Take him to the emergency room.")
        self.assertEqual(out["auto_ems_instruction"], 0)
        self.assertEqual(out["auto_escalation"], 1)

    def test_911_position(self):
        pos = position_measures("Please call 911 now.")
        self.assertEqual(pos["first_911_word"], 3)
        self.assertEqual(pos["surface_word_count"], 4)

    def test_999_position(self):
        pos = position_measures("Call 999 immediately.")
        self.assertEqual(pos["first_999_word"], 2)

    def test_poison_control_position(self):
        pos = position_measures("Please contact Poison Control right away.")
        self.assertEqual(pos["first_poison_control_word"], 3)

    def test_911_normalization(self):
        self.assertIn("nine one one", normalize_numbers_for_readability("Call 9-1-1 now."))

    def test_911_no_zero_syllable_artifact(self):
        score = readability("Call 911 now.")
        self.assertGreater(score["n_syllables"], 0)
        self.assertEqual(score["n_words"], 5)


if __name__ == "__main__":
    unittest.main()
