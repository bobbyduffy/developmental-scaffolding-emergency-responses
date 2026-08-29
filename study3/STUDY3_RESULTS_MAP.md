# Study 3 Results Map

**Purpose:** manuscript-facing source-of-truth map for Study 3.

This file distinguishes frozen confirmatory results, prespecified secondary/sensitivity
analyses, post-confirmatory descriptive synthesis, and outcomes that failed validation.

No result listed here supersedes the preregistration or frozen analysis plan. This file
records the final interpretive disposition reached before manuscript drafting.

---

## 1. Canonical dataset

- Planned design: 15,360 trials
- Canonical successful responses: 15,360
- Cells: 384
- Canonical successful responses per cell: 40
- Empty successful responses: 0
- Truncated successful responses: 0

Collection included 315 initially missing Claude trials caused by exhausted API credits.
These were recovered append-only. Canonicalization selected exactly one successful
response per trial ID.

Authoritative integrity files:

- `data/raw_integrity.json`
- `check_raw_integrity.py`
- `POST_FREEZE_DEVIATIONS.md`

Primary raw-response source:

- `data/full.jsonl`

Canonical coded analysis table:

- `data/results.jsonl`

---

## 2. Confirmatory outcomes

Authoritative frozen confirmatory output:

- `data/confirmatory_analysis.json`
- analysis script: `analyze_results.py`

### EMS presence

Population: all 15,360 valid canonical responses.

- EMS present: 14,991 / 15,360
- Overall presence: 97.60%
- relationship × certainty omnibus:
  - Wald = 487.904
  - df = 21
  - p = 4.96e-90

Interpretive status:

**Usable.**

Presence is treated as the first part of the prespecified two-part EMS framework.

---

### H1 — first EMS-directive word

Population: EMS-present responses only.

Primary model:

`first_ems_directive_word ~ relationship × certainty + relationship × prompt_variant + certainty × prompt_variant + model + system`

- N = 14,991
- relationship × certainty:
  - Wald = 1334.965
  - df = 21
  - p = 7.95e-270

Post-confirmatory rank verification:

- nominal restrictions = 21
- covariance rank = 21
- design rank = 46 / 46
- rank deficient = false
- rank-aware statistic exactly reproduces frozen H1

Authoritative diagnostic files:

- `latency_surface_diagnostics.py`
- `data/latency_surface_diagnostics.json`
- `data/model_relationship_certainty_latency_surfaces.csv`
- `data/model_relationship_certainty_spread.csv`

Interpretive status:

**Primary result; usable.**

---

### H2 — matched-pair attenuation

Prespecified contrast:

`(male-coded − female-coded at L4) − (male-coded − female-coded at L2)`

Holm-adjusted matched-pair results:

- daddy − mommy:
  - DID = +1.514 words
  - Holm p = .151

- dad − mom:
  - DID = +2.871 words
  - Holm p = .042

- boyfriend − girlfriend:
  - DID = −3.242 words
  - Holm p = .151

- husband − wife:
  - DID = +6.182 words
  - Holm p = .000528

At L4, all four adjusted matched-pair gaps are small in absolute magnitude
(|gap| <= approximately 0.54 words).

Interpretive status:

**Usable, but pair-specific. Do not describe as a common-sign sex effect.**

---

### H3 — EMS-priority opening

Frozen confirmatory automated result:

- overall automated priority rate ≈ 70.3%
- relationship × certainty omnibus statistically strong
- p numerically underflowed below floating-point reporting precision

However, the automated H3 measure subsequently failed a prospectively specified
label-blinded human validation audit.

Validation N = 256.

- exact agreement = 87.89%
- Cohen's kappa = .694
- sampling-weighted automated priority prevalence = 68.94%
- sampling-weighted human priority prevalence = 81.19%
- human minus machine = +12.25 percentage points

All 31 disagreements were:

- machine non-priority
- human priority

No disagreements occurred in the opposite direction.

Disagreement by certainty:

- L1: 25.0%
- L2: 15.6%
- L3: 4.7%
- L4: 3.1%

Because measurement error is certainty-dependent, it could directly distort the
relationship × certainty interaction.

Authoritative validation files:

- `H3_OPENING_VALIDATION_SPEC.md`
- `H3_OPENING_VALIDATION_ADDENDUM.md`
- `H3_VALIDATION_DISPOSITION.md`
- `data/h3_opening_validation_results.json`
- `data/h3_priority_validation_confusion.csv`
- `data/h3_opening_validation_human.csv`

Interpretive status:

**Failed validation. Frozen result remains in the record but receives no substantive
inferential interpretation in the manuscript.**

---

### H4 — EMS within first 10 words

Population: EMS-present responses only.

Frozen relationship × certainty result:

- Wald = 1054.425
- df = 21
- p = 7.03e-210
- covariance rank = 21 / 21
- design rank = 46 / 46

Authoritative post-confirmatory reporting:

- `h4_prominence_analysis.py`
- `data/h4_prominence_analysis.json`
- `data/h4_model_relationship_certainty_surfaces.csv`
- `data/h4_relationship_spread_by_model.csv`

Interpretive status:

**Usable.**

This is a mechanically defined prominence outcome and provides an independent
operationalization of EMS foregrounding.

---

### H5 — relationship × certainty × prompt-variant latency heterogeneity

Frozen result:

- Wald = 153.538
- df = 21
- p = 3.73e-22

Interpretive status:

**Usable as prespecified heterogeneity evidence.**

Do not promote local variant-specific cells to new confirmatory hypotheses.

---

## 3. Prespecified secondary and sensitivity analyses

Authoritative output:

- `secondary_reporting.py`
- `data/secondary_reporting.json`

### Ordered certainty trend

- Wald = 781.641
- df = 7
- p = 1.70e-164

Interpretation:

Strong overall certainty-related change, but categorical/nonmonotonic structure remains
important. Do not let the ordered trend replace the categorical analysis.

### Role / sex decomposition

- pair_key × referent_sex × certainty:
  - Wald = 34.802
  - df = 9
  - p = 6.46e-5

- referent_sex × certainty:
  - Wald = 49.340
  - df = 3
  - p = 1.10e-10

Interpretation:

There is a sex-coded component, but it is materially pair-dependent and is not well
summarized as a uniform male/female effect.

### Latency heterogeneity by model

- relationship × certainty × model:
  - Wald = 1201.074
  - df = 21
  - p = 3.46e-241

### Latency heterogeneity by system prompt

- relationship × certainty × system:
  - Wald = 176.741
  - df = 42
  - p = 1.87e-18

Relationship × certainty latency remains strong when stratified by:

- Claude
- GPT
- assistant system condition
- minimal system condition
- no system prompt
- prompt variant A
- prompt variant B

Interpretive status:

**Usable secondary/sensitivity evidence.**

Do not equate larger Wald statistics with larger raw effect magnitude.

---

## 4. EMS-presence sensitivity

Authoritative files:

- `PRESENCE_SENSITIVITY_SPEC.md`
- `presence_sensitivity.py`
- `data/presence_sensitivity.json`

### relationship × certainty × model

- Wald = 662.994
- df = 21
- p = 8.62e-127
- covariance rank = 21 / 21

### relationship × certainty × system

- Wald = 47.803
- df = 42
- p = .249
- covariance rank = 42 / 42

Descriptive structure:

- GPT EMS presence = 7,680 / 7,680
- Claude EMS presence = 7,311 / 7,680
- all 369 EMS omissions are Claude responses
- 365 / 369 omissions occur at L1
- Claude omissions:
  - L1: 365
  - L2: 4
  - L3: 0
  - L4: 0

Interpretation:

Presence is strongly model-dependent. GPT is at a hard EMS-inclusion ceiling. Claude
shows relationship-conditioned EMS omission primarily under L1 ambiguity.

No detectable pooled relationship × certainty × system heterogeneity was found for
presence. This is not an equivalence claim.

---

## 5. Model-specific latency surfaces

Authoritative files:

- `latency_surface_diagnostics.py`
- `data/model_relationship_certainty_latency_surfaces.csv`
- `data/model_relationship_certainty_spread.csv`

Across-relationship adjusted latency ranges:

### Claude

- L1: 79.96 words
- L2: 46.97 words
- L3: 5.85 words
- L4: 1.39 words

### GPT

- L1: 29.79 words
- L2: 6.89 words
- L3: 0
- L4: 0

Raw verification established that for GPT:

- L3: 1,920 / 1,920 responses had first EMS-directive word = 1
- L4: 1,920 / 1,920 responses had first EMS-directive word = 1

Interpretation:

GPT reaches complete first-word EMS convergence at L3 and remains there at L4.
Claude converges more gradually into a narrow early-response band.

---

## 6. H4 model-specific prominence surfaces

Across-relationship adjusted range in probability of EMS appearing within 10 words:

### Claude

- L1: 15.56 percentage points
- L2: 62.92 percentage points
- L3: 27.50 percentage points
- L4: 5.00 percentage points

### GPT

- L1: 59.17 percentage points
- L2: 36.25 percentage points
- L3: 0
- L4: 0

Three Claude L1 adjusted linear-probability estimates fall slightly below zero.

Interpretation:

These are ordinary LPM boundary artifacts and must not be interpreted as literal
negative probabilities. Do not clip them for inference.

---

## 7. Mechanical-endpoint synthesis

Authoritative files:

- `mechanical_endpoint_synthesis.py`
- `data/mechanical_endpoint_surface.csv`
- `data/mechanical_endpoint_relationship_spreads.csv`
- `data/mechanical_endpoint_synthesis.json`

No new inference is performed in this synthesis.

Relationship-conditioned adjusted spread:

| Model | Certainty | EMS presence range | Within-10 range | Latency range |
|---|---:|---:|---:|---:|
| Claude | L1 | 53.33 pp | 15.56 pp | 79.96 words |
| Claude | L2 | 1.25 pp | 62.92 pp | 46.97 words |
| Claude | L3 | 0 | 27.50 pp | 5.85 words |
| Claude | L4 | 0 | 5.00 pp | 1.39 words |
| GPT | L1 | 0 | 59.17 pp | 29.79 words |
| GPT | L2 | 0 | 36.25 pp | 6.89 words |
| GPT | L3 | 0 | 0 | 0 |
| GPT | L4 | 0 | 0 | 0 |

Interpretive status:

**Primary descriptive synthesis for manuscript use.**

Empirical summary:

Relationship framing has its greatest observable influence when emergency evidence
leaves room for response-policy discretion, but the affected dimension differs by model.

GPT maintains universal EMS inclusion and varies primarily in foregrounding at L1/L2,
then reaches complete first-word convergence at L3/L4.

Claude additionally varies whether EMS appears under L1 ambiguity. Once inclusion
saturates, substantial relationship-conditioned variation remains in prominence and
latency before contracting sharply under respiratory evidence.

---

## 8. Opening-policy classifier

Prospective validation:

- exact agreement = 66.80%
- Cohen's kappa = .463
- Claude disagreement = 55.47%
- GPT disagreement = 10.94%

Interpretive status:

**Failed validation. Do not use automated opening-policy categories for substantive
descriptive claims.**

The partial first human-coding pass:

- `data/h3_opening_validation_human_partial_misapplied.csv`

is provenance only and must never be used analytically.

---

## 9. Manuscript-facing outcome hierarchy

### Main empirical outcomes

1. EMS presence
2. first EMS-directive word position
3. EMS within first 10 words

### Confirmatory result retained but not interpreted

4. H3 EMS-priority opening — failed validation

### Excluded from substantive interpretation

5. automated opening-policy categories — failed validation

---

## 10. Analysis boundary

Study 3 analysis is considered complete for manuscript drafting.

Further analyses should be undertaken only when required to resolve a concrete reporting,
reproducibility, reviewer, or manuscript-construction question.

Any such analysis is post-freeze and must not be represented as confirmatory unless it
was explicitly specified in the frozen preregistration/analysis plan.

The manuscript should preserve the distinction among:

- preregistered confirmatory analysis;
- prespecified secondary/sensitivity analysis;
- post-confirmatory descriptive synthesis;
- post-confirmatory validation.
