# Table 2 — Main Inferential Results

**Manuscript:** Relationship Framing and Emergency Evidence in Language-Model Responses: Three Studies of EMS Foregrounding

**Table number:** 2

**Status:** SCIENTIFIC SPECIFICATION DRAFT — VERIFIED AGAINST FROZEN STUDY RECORDS

---

## 1. Scientific purpose

Table 2 provides the numerical inferential backbone of the empirical manuscript without reproducing full regression output.

It must preserve the distinction among:

- confirmatory primary analyses;
- preregistered or prespecified secondary analyses;
- prespecified sensitivity analyses.

It must not promote exploratory or failed-validation analyses into the supported inferential record.

The table is divided into three panels:

- Panel A — Studies 1–2;
- Panel B — Study 3 confirmatory results;
- Panel C — Study 3 prespecified secondary/sensitivity results.

---

## 2. Panel A — Studies 1–2

### Study 1

Include:

1. Overall emergency-cue effect on EMS directive presence.
   - Status: confirmatory primary-family result.
   - Emergency: 1,440/1,440 = 100%.
   - Non-emergency: 694/1,440 = 48.19%.
   - Difference = +51.81 percentage points.
   - 95% CI = [49.21, 54.38] pp.
   - z = 31.73.
   - p = 6.02e-221.

2. Emergency × relationship interaction on EMS directive presence.
   - Status: confirmatory.
   - Use the preregistered separation fallback.
   - HC3 linear-probability-model Wald = 85.90.
   - df = 3.
   - p = 1.66e-18.

3. Emergency × relationship interaction on Flesch–Kincaid Grade Level.
   - Status: preregistered secondary.
   - HC3 OLS Wald = 32.76.
   - df = 3.
   - p = 3.61e-7.

Do not include the four within-relationship emergency contrasts in the main table. They are confirmatory but are not necessary to understand the main relationship × emergency result on first reading; retain them for prose/supplement.

The table note must disclose that the frozen Study 1 logistic interaction fit returned numerically despite practical complete separation. The preregistration had specified an HC3 linear-probability fallback for non-estimable separation; the fallback was applied after the separation problem was diagnosed. Do not report the frozen script's approximately p=1 logistic interaction as substantive evidence.

### Study 2

Include:

1. H1 relationship omnibus on first EMS-directive word.
   - Status: primary confirmatory.
   - Wald = 406.196.
   - df = 7.
   - p = 1.1186e-83.

2. H2 matched male-coded minus female-coded contrasts.
   - Status: confirmatory.
   - daddy − mommy = +4.2528 words; 95% CI [3.0678, 5.4377]; Holm p = 8.00048e-12.
   - dad − mom = +1.9111 words; 95% CI [0.2725, 3.5498]; Holm p = .0445206.
   - boyfriend − girlfriend = −0.6778 words; 95% CI [−3.6178, 2.2622]; Holm p = .651379.
   - husband − wife = −3.2500 words; 95% CI [−5.2917, −1.2083]; Holm p = .005426.

3. H3 role × gendered-referent interaction.
   - Status: confirmatory.
   - Wald = 42.4846.
   - df = 3.
   - p = 3.16612e-9.

Do not place the large Study 2 H4 accessibility/register families in the main inferential table. They remain real prespecified secondary evidence, but they are better suited to the supplement and/or later theoretical treatment unless manuscript prose requires a specific main-text claim from them.

---

## 3. Panel B — Study 3 confirmatory results

Include:

1. EMS presence relationship × certainty omnibus.
   - Population: all 15,360 canonical responses.
   - EMS present = 14,991/15,360.
   - Wald = 487.904.
   - df = 21.
   - Raw p = 4.96e-90.
   - Holm p across the prespecified core binary-guidance family = 4.96e-90.
   - Status: confirmatory binary-guidance result.

2. H1 relationship × certainty on conditional EMS latency.
   - Population: 14,991 EMS-present responses.
   - Wald = 1334.965.
   - df = 21.
   - p = 7.95e-270.
   - Status: single primary confirmatory test.

3. H2 matched-pair L4-minus-L2 changes in the male-coded minus female-coded latency gap.
   Prespecified contrast:
   (male-coded − female-coded at L4) − (male-coded − female-coded at L2)

   - daddy − mommy: +1.514 words; 95% CI [−0.306, 3.334]; Holm p = .151.
   - dad − mom: +2.871 words; 95% CI [0.578, 5.164]; Holm p = .042.
   - boyfriend − girlfriend: −3.242 words; 95% CI [−6.818, 0.334]; Holm p = .151.
   - husband − wife: +6.182 words; 95% CI [3.012, 9.352]; Holm p = .000528.

   Do not imply that positive values are inherently more biased or that a common sign was predicted.

4. H4 EMS within first 10 words, relationship × certainty.
   - Population: EMS-present responses.
   - Wald = 1054.425.
   - df = 21.
   - Raw p = 7.03e-210.
   - Holm p across the prespecified core binary-guidance family = 1.41e-209.
   - Status: confirmatory objective prominence outcome.

5. H5 relationship × certainty × prompt-variant latency heterogeneity.
   - Wald = 153.538.
   - df = 21.
   - p = 3.73e-22.
   - Status: prespecified confirmatory heterogeneity result.

Do not include H3 EMS-priority opening as an ordinary supported inferential result. Its frozen automated result remains in the research record but failed prospective human validation and receives no substantive inferential interpretation. Table 3 documents that disposition.

---

## 4. Panel C — Study 3 prespecified secondary/sensitivity results

Include:

1. Role / referent-sex decomposition:
   - pair_key × referent_sex × certainty:
     Wald = 34.802; df = 9; p = 6.46e-5.
   - referent_sex × certainty:
     Wald = 49.340; df = 3; p = 1.10e-10.
   Status: prespecified secondary.

These rows support the bounded conclusion that a sex-coded component is detectable but materially pair-dependent.

2. Latency heterogeneity:
   - relationship × certainty × model:
     Wald = 1201.074; df = 21; p = 3.46e-241.
   - relationship × certainty × system:
     Wald = 176.741; df = 42; p = 1.87e-18.
   Status: prespecified sensitivity.

3. EMS-presence heterogeneity:
   - relationship × certainty × model:
     Wald = 662.994; df = 21; p = 8.62e-127.
   - relationship × certainty × system:
     Wald = 47.803; df = 42; p = .249.
   Status: prespecified post-confirmatory sensitivity.

The nonsignificant presence × system result is not an equivalence claim.

Do not include the ordered-certainty trend in the main table. It is usable prespecified secondary evidence, but the categorical/nonmonotonic structure is scientifically primary and the ordered trend is not required to verify a main-text claim on first reading.

Do not include full model/system/variant-stratified estimates in the main table; place them in the supplement.

---

## 5. Manuscript-facing columns

Use:

1. Study / hypothesis
2. Inferential status
3. Test or contrast
4. Estimate (95% CI), when applicable
5. Test statistic
6. df
7. p value

For multiplicity-adjusted families, report the adjusted p value in the p column and identify it as Holm-adjusted.

For omnibus tests without a single meaningful effect estimate, use an em dash in the estimate column rather than inventing one.

---

## 6. P-value presentation

Use compact scientific notation for very small p-values.

Do not print p = 0.

Suggested manuscript rendering:

- 6.02 × 10^-221
- 1.66 × 10^-18
- 3.61 × 10^-7
- etc.

Values such as .151, .042, .249 may be printed to three significant decimals.

---

## 7. Source precedence

Study 1:
- `study1/preregistration.md`
- frozen `study1/analyze_results.py`
- `checkpoints/2026-08-28-study1-analysis-checkpoint.md`

Study 2:
- `study2/preregistration.md`
- `study2/analysis/confirmatory_results.json`
- `study2/analysis/confirmatory_results.md`

Study 3:
- `study3/preregistration.md`
- `study3/ANALYSIS_PLAN.md`
- `study3/data/confirmatory_analysis.json`
- `study3/data/secondary_reporting.json`
- `study3/data/presence_sensitivity.json`
- `study3/STUDY3_RESULTS_MAP.md`
- validation disposition records for H3

If a manuscript-facing summary conflicts with these frozen records, correct the manuscript artifact rather than rewriting historical records.
