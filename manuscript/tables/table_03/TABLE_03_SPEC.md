# Table 3 — Human Validation Audit and Disposition

**Manuscript:** Relationship Framing and Emergency Evidence in Language-Model Responses: Three Studies of EMS Foregrounding

**Table number:** 3

**Status:** SCIENTIFIC SPECIFICATION DRAFT — VERIFIED AGAINST FROZEN VALIDATION RECORDS

---

## 1. Scientific purpose

Table 3 reports the prospective human-validation audit of the two automated Study 3
discourse-level measures:

1. `ems_priority_opening` (the preregistered H3 outcome); and
2. `opening_policy`.

Its purpose is to make the measurement failure visible in the main manuscript and to
document the resulting interpretive disposition.

The table does not attempt to rehabilitate either automated measure.

No frozen Study 3 machine labels or confirmatory outputs were changed after validation.

---

## 2. Validation design

Validation frame:

- canonical Study 3 responses with `ems_instruction = 1`;
- EMS-present population N = 14,991.

Audit sample:

- 2 models × 8 relationships × 4 certainty levels = 64 strata;
- 4 responses sampled deterministically from each stratum;
- audit N = 256.

Sampling used fixed SHA-256 ranking with frozen seed:

`study3-h3-opening-validation-v1-20260829`

Human audit characteristics:

- label-blinded author audit;
- not fully independent;
- not hypothesis-naive;
- automated labels were hidden during coding;
- explicit model/certainty/variant/system metadata were hidden during coding;
- complete response text necessarily remained visible.

All 256 completed human codes were checkpointed before machine agreement was revealed.

A pre-coding text-field repair, a mid-audit rule-application clarification/restart, and
a post-coding scorer type-coercion fix are documented in
`H3_OPENING_VALIDATION_ADDENDUM.md`. None changed the selected 256 source IDs, their
coding order, the frozen coding definitions, the validation thresholds, or any machine
label. The restarted audit was completed before machine-label comparison.

---

## 3. H3 — EMS-priority opening

Measure:

`ems_priority_opening`

Audit results:

- audit N = 256;
- non-uncertain human codes = 256;
- uncertain = 0;
- equal-cell exact agreement = 87.89%;
- Cohen's kappa = .694;
- 95% Wilson CI for exact agreement = [83.32%, 91.34%];
- sampling-weighted automated priority prevalence = 68.94%;
- sampling-weighted human priority prevalence = 81.19%;
- human minus automated prevalence = +12.25 percentage points.

Prespecified strong-support requirements:

- >=95% non-uncertain human coding;
- exact agreement >=90%;
- kappa >=.80;
- absolute weighted prevalence discrepancy <=5 percentage points.

Disposition:

**FAILED VALIDATION — no substantive inferential interpretation.**

The frozen automated H3 omnibus result remains part of the historical confirmatory
record but is not used as supported manuscript inference.

Important diagnostic pattern:

All 31 H3 disagreements were directional:

- machine non-priority / human priority = 31;
- machine priority / human non-priority = 0.

Disagreement rate by certainty:

- L1 = 25.0%;
- L2 = 15.6%;
- L3 = 4.7%;
- L4 = 3.1%.

Because the measurement error is certainty-dependent, it can directly distort or
exaggerate the relationship × certainty interaction that H3 was intended to test.
This is the scientific reason the failed audit limits interpretation.

The full confusion matrix belongs in supplementary material.

---

## 4. Opening-policy classifier

Measure:

`opening_policy`

Audit results:

- audit N = 256;
- non-uncertain human codes = 256;
- uncertain = 0;
- equal-cell exact agreement = 66.80%;
- Cohen's kappa = .463.

Prespecified descriptive-use requirements:

- >=95% non-uncertain human coding;
- exact agreement >=80%;
- kappa >=.70.

Disposition:

**FAILED VALIDATION — not used for substantive descriptive claims.**

Descriptive diagnostic:

- Claude disagreement = 55.47%;
- GPT disagreement = 10.94%.

A prominent confusion involved 30 responses automatically labeled `ems_priority`
whose first meaningful move was classified by the human auditor as `urgency_label`.

The full multiclass confusion matrix belongs in supplementary material.

---

## 5. Manuscript-facing columns

Use:

1. Measure
2. Audit N
3. Non-uncertain human codes
4. Exact agreement
5. Cohen's kappa
6. Weighted prevalence discrepancy
7. Prespecified criterion met?
8. Final disposition

For `opening_policy`, weighted prevalence discrepancy is not applicable because the
prespecified prevalence comparison was specific to H3.

---

## 6. Manuscript-facing table

| Measure | Audit N | Non-uncertain | Exact agreement | Cohen's kappa | Weighted prevalence discrepancy | Criterion met? | Final disposition |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| H3 EMS-priority opening | 256 | 256 (100%) | 87.89% | .694 | Human − automated = +12.25 pp | No | Frozen automated result retained; no substantive inferential interpretation |
| Opening policy | 256 | 256 (100%) | 66.80% | .463 | — | No | Not used for substantive descriptive claims |

---

## 7. Table-note requirements

The note should state that:

- the audit was a prospectively specified, label-blinded author validation of 256
  stratified EMS-present responses;
- H3 strong-support thresholds were >=90% agreement, kappa >=.80, <=5 pp absolute
  weighted prevalence discrepancy, and >=95% non-uncertain coding;
- opening-policy descriptive-use thresholds were >=80% agreement, kappa >=.70, and
  >=95% non-uncertain coding;
- H3 95% Wilson agreement CI was [83.32%, 91.34%];
- all 31 H3 disagreements were machine non-priority → human priority;
- H3 disagreement fell from 25.0% at L1 to 3.1% at L4, making the measurement error
  certainty-dependent;
- no frozen machine labels or confirmatory results were altered after validation.

Do not imply that failure of the validation audit invalidates the mechanically defined
Study 3 endpoints. Presence, directive latency, and within-10-word prominence are
separate outcomes and remain the manuscript's primary interpretive basis.

---

## 8. Exclusions

Do not place in the main Table 3 body:

- full H3 confusion matrix;
- full opening-policy multiclass confusion matrix;
- model-specific opening-policy confusion tables;
- prompt-variant/system disagreement diagnostics;
- interface implementation history;
- pre-coding text-field repair details;
- the preserved partial misapplied human-coding file;
- post hoc classifier repair or replacement analyses.

These belong in provenance records and/or supplementary material.

---

## 9. Source precedence

Authoritative validation records:

- `study3/H3_OPENING_VALIDATION_SPEC.md`
- `study3/H3_OPENING_VALIDATION_ADDENDUM.md`
- `study3/H3_VALIDATION_DISPOSITION.md`
- `study3/data/h3_opening_validation_results.json`
- `study3/data/h3_priority_validation_confusion.csv`
- `study3/data/opening_policy_validation_confusion.csv`
- `study3/data/h3_opening_validation_error_summary.csv`
- `study3/STUDY3_RESULTS_MAP.md`
- `checkpoints/2026-08-29_Study3_Analysis_Freeze_PreDraft.md`

If a manuscript-facing summary conflicts with these records, correct the manuscript
artifact rather than altering frozen validation history.
