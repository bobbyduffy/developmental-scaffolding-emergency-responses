# Study 3 preregistration — working draft

**NOT FROZEN. DO NOT COLLECT FROM THIS DRAFT.**

## Research question

Does increasing emergency evidence reduce relationship-conditioned differences in how quickly language models foreground emergency services?

## Design

Planned factorial design:

- 8 relationship referents;
- 4 ordered emergency-certainty levels;
- 2 prompt variants;
- 3 system-prompt conditions;
- 2 model strata;
- 40 independent repetitions per exact cell.

Total planned responses: **15,360**.

The exact stimulus templates are maintained in `STIMULI.md`.

## Primary outcome framework

Study 3 uses a two-part EMS outcome:

1. presence/absence of a clean explicit EMS directive;
2. conditional on presence, the 1-indexed surface-word position of the first clean explicit EMS directive.

EMS-absent responses will not be assigned artificial endpoint latencies.

## Primary confirmatory hypothesis

**H1.** Relationship framing interacts with emergency certainty in predicting conditional first-EMS position.

The primary test is an omnibus test of the 8-level relationship × 4-level certainty interaction. Certainty is categorical in this test.

The primary analysis will include model, system-prompt condition, and prompt variant as prospectively specified design factors. The exact final regression formula, covariance specification, handling of any sparse/constant cells, and multiplicity plan remain to be finalized before freeze.

## Planned confirmatory / secondary tests

### H2 — matched-pair moderation

Report certainty-specific matched-pair differences for:

- daddy − mommy
- dad − mom
- boyfriend − girlfriend
- husband − wife

These are planned contrasts subordinate to the omnibus H1 test. No common sign across pairs is assumed.

A prespecified contrast will compare each pair's Level-4 difference with its Level-2 difference.

### H3 — EMS-priority opening

Test whether emergency certainty and relationship framing predict whether an explicit EMS directive is foregrounded before substantive assessment, questioning, or interim-care action.

Brief supportive language or emergency/urgency labeling before the EMS directive does not by itself disqualify an EMS-priority opening.

### H4 — objective early prominence

Record whether the first clean EMS directive begins within the first 10 surface words and test relationship × certainty patterns on this outcome.

### H5 — prompt-variant heterogeneity

Treat prompt variant as a substantive factor and test whether the relationship × certainty pattern differs between wake-state wording (A) and behavioral-response wording (B), including a prespecified relationship × certainty × variant heterogeneity test.

No directional A-vs-B effect is hypothesized.

### Secondary ordered trend

A secondary ordered-certainty analysis will test whether relevant relationship-conditioned differences attenuate in a graded direction as evidence becomes increasingly decisive. The primary categorical model does not assume linearity or equal spacing.

## Model/system scope

Model and system-prompt condition are design strata in the primary analysis. High-order model/system interactions are not primary hypotheses. Model- and system-specific estimates may be reported as prespecified secondary analyses.

## Response-structure coding

Before collection, coding rules will prospectively define:

- EMS-priority opening;
- supportive / relational lead;
- diagnostic assertion;
- conditional assessment;
- interim action / care instruction before EMS;
- other.

Coder examples, counterexamples, hierarchy, and adjudication rules must be frozen before collection.

## Interpretation boundaries

Study 3 tests whether relationship-conditioned emergency-response timing changes with supplied evidence. It does not directly identify latent causes such as attachment, dependency, economic importance, demographic risk priors, or perceived value of the referent.

Attenuation as certainty rises would support an escalation-threshold interpretation. Persistence at the most severe certainty level would weigh against a pure threshold account. Reversal or non-monotonicity would indicate a more complex response-policy process. Variant-specific effects would indicate sensitivity to how responsiveness is linguistically represented.

## Outstanding items before preregistration freeze

- exact model endpoints and API settings;
- exact inherited system-prompt text/date handling;
- exact regression formulas and covariance estimators;
- EMS-presence model specification;
- sparse/constant-cell contingencies;
- multiplicity correction families;
- coder rules and tests;
- synthetic-data validation;
- runner/dry-run/probe procedure;
- manifest/hash procedure;
- final adversarial audit of all resolved prompts;
- pre-collection freeze commit.
