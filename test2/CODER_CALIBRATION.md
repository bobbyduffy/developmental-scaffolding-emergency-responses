# Study 2 coder calibration against Study 1

**Coder:** `code_responses.py` version 2.0.0  
**Calibration corpus:** the completed 2,880-response Study 1 raw dataset  
**Purpose:** reduce unnecessary human adjudication while making the Study 2 rules more explicit and reproducible.

## Review burden

Study 1 v1 screen:

- 2,880 total responses
- 1,150 sent to human adjudication (39.9%)
- 651/1,150 reviewed rows (56.6%) already contained at least one clean emergency directive and all 651 were ultimately EMS-positive

Study 2 v2 coder applied retrospectively to the same 2,880 raw responses:

- 2,880 automatically coded
- **0 sent to human review**

This is a calibration result, not a promise that the Study 2 review queue will be zero. Novel softened or contradictory formulations remain reviewable.

## Primary binary concordance

Compared with the final Study 1 coding (v1 automatic codes plus completed blinded adjudication):

- agreement: **2,855 / 2,880 = 99.13%**
- disagreements: 25

All 25 disagreements came from the subset that Study 1 had sent to human review.

Direction of disagreement:

- 23 Study 1 human `0` → v2 `1`
- 2 Study 1 human `1` → v2 `0`

The 23 `0→1` cases are mostly conditional safety instructions such as `if she is hard to wake, call emergency services right away`. Version 2 intentionally resolves these as explicit instructions. This is a prospective definitional clarification, not an attempt to overwrite the Study 1 confirmatory outcome.

The two `1→0` cases contain emergency-help language without a clean contact directive under the stricter v2 literal rule. The original Study 1 codes remain authoritative for Study 1.

## Escalation concordance

The v2 2/3 rule is intentionally different from the v1 automatic rule and from the subjective Study 1 human urgency judgment, so raw all-data agreement is not the design goal.

Among the 1,127 human-adjudicated Study 1 rows with a human escalation code of 2 or 3:

- v2 matches the human 2/3 level on **1,061 / 1,127 = 94.14%**
- 66 differ

Among the 1,125 of those rows in which v2 identifies an explicit emergency directive:

- v2 matches on **1,061 / 1,125 = 94.31%**
- 64 differ

The threshold is frozen prospectively for Study 2 as:

- level 3 if first explicit EMS directive begins at/before word 45;
- level 2 if it begins after word 45.

The exact continuous position is retained, so inferential analyses need not depend exclusively on this dichotomy.

## Interpretation

Version 2 should be treated as a new prospective coding specification. It is calibrated against Study 1 but does not retroactively replace the original Study 1 confirmatory coding.

For direct Study-1/Study-2 sensitivity comparisons, both corpora can be re-coded under v2 and that recoding should be labeled explicitly.
