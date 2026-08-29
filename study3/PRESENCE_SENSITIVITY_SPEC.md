# Study 3 EMS-presence sensitivity specification

**Status:** post-confirmatory implementation note for analyses already specified before collection.

This document was added after the frozen confirmatory output had been generated and after descriptive inspection showed that EMS omissions were concentrated in one model endpoint and at low certainty. It does **not** create a new preregistered hypothesis and does not alter the frozen confirmatory analysis.

Its purpose is to make the implementation boundary explicit before the corresponding formal sensitivity models are executed.

## Frozen basis

The pre-collection `ANALYSIS_PLAN.md` specified a two-part EMS framework. Part A analyzes `ems_instruction` on all valid rows using an HC3 linear probability model, and Section 11 states that relationship × certainty × model and relationship × certainty × system-prompt interactions are secondary/sensitivity analyses. The frozen preregistration repeats the same model/system sensitivity commitment and requires model-, system-, and variant-stratified estimates so concentration in a design stratum is visible.

The frozen plan also specifies that binary outcomes remain HC3 linear probability models; constant subsets are reported descriptively without fabricated p-values; planned Wald restrictions must be estimable; and sparse/constant cells are not repaired by post hoc category merging or silent substitution of logistic/Firth regression.

## Formal inferential sensitivity tests

Only the two higher-order interactions explicitly named in the frozen plan are tested inferentially here.

### 1. Relationship × certainty × model

Fit on all valid rows:

`ems_instruction ~ C(relationship) * C(certainty) * C(model_key) + C(relationship) * C(prompt_variant) + C(certainty) * C(prompt_variant) + C(model_key) * C(prompt_variant) + C(sysprompt_condition)`

Jointly test the 21 relationship × certainty × model coefficients using HC3 covariance.

This is a secondary/sensitivity test, not a primary hypothesis and not part of the core binary multiplicity family.

### 2. Relationship × certainty × system prompt

Fit on all valid rows:

`ems_instruction ~ C(relationship) * C(certainty) * C(sysprompt_condition) + C(relationship) * C(prompt_variant) + C(certainty) * C(prompt_variant) + C(sysprompt_condition) * C(prompt_variant) + C(model_key)`

Jointly test the 42 relationship × certainty × system coefficients using HC3 covariance.

This is a secondary/sensitivity test, not a primary hypothesis and not part of the core binary multiplicity family.

These formula extensions mirror the already implemented prespecified latency sensitivity models while substituting the Part-A EMS-presence outcome.

## Stratified reporting

Report raw EMS-presence/omission counts and probabilities by:

- model × relationship × certainty;
- system prompt × relationship × certainty;
- prompt variant × relationship × certainty;
- model × relationship × certainty × prompt variant × system prompt where useful for locating concentration.

If a model/system/variant subset is constant, report the observed probability only. Stratified tables are descriptive unless a formal interaction above directly tests the corresponding concentration.

## Explicitly not promoted to prespecified inference

The frozen prompt-variant heterogeneity hypothesis (H5) and its three-way relationship × certainty × variant test were specified for **latency conditional on EMS presence**, not for EMS presence itself. Therefore, despite descriptive wording differences observed in the EMS-presence data, this implementation does **not** add a formal relationship × certainty × variant EMS-presence test to the prespecified family.

Likewise, no new within-Claude relationship × certainty × variant or relationship × certainty × system inferential test is introduced after inspecting the omission pattern. Such analyses, if ever performed, must be labeled exploratory/post hoc.

## Estimability and rank

For each planned Wald restriction:

- report coefficient count;
- compute the rank of the robust restriction covariance matrix;
- report any rank deficiency explicitly;
- do not alter categories, reference levels, estimand, or estimator to recover significance or estimability.

The descriptive fact that one endpoint may be constant is not itself grounds to change the frozen HC3-LPM framework.
