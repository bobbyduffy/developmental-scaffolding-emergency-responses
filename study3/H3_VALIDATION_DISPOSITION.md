# Study 3 H3 / Opening-Policy Validation Disposition

## Status

The preregistered automated H3 outcome (`ems_priority_opening`) and the automated
`opening_policy` classifier were subjected to a prospective label-blinded author
validation audit of 256 stratified EMS-present responses.

The audit was completed and human labels were checkpointed before machine agreement
was revealed.

## H3 validation result

`ems_priority_opening` did not satisfy the prespecified validation guardrails.

- Audit N: 256
- Non-uncertain human codes: 256
- Exact agreement: 87.89%
- Cohen's kappa: 0.694
- 95% Wilson CI for agreement: [83.32%, 91.34%]
- Sampling-weighted automated priority prevalence: 68.94%
- Sampling-weighted human priority prevalence: 81.19%
- Human minus automated prevalence: +12.25 percentage points

Prespecified strong-support requirements were:

- >=95% non-uncertain human coding
- >=90% exact agreement
- kappa >=0.80
- <=5 percentage-point weighted prevalence discrepancy

H3 therefore failed prospective validation.

All 31 H3 disagreements were directional:

- machine non-priority / human priority: 31
- machine priority / human non-priority: 0

Disagreement was also certainty-dependent:

- L1: 25.0%
- L2: 15.6%
- L3: 4.7%
- L4: 3.1%

Because measurement error is systematically concentrated at lower certainty levels,
it can directly contaminate or exaggerate a relationship-by-certainty interaction.
The confirmatory automated H3 omnibus result therefore remains part of the frozen
record but will not receive substantive inferential interpretation.

## Opening-policy validation result

The more granular automated `opening_policy` classifier also failed its prespecified
validation guardrails.

- Exact agreement: 66.80%
- Cohen's kappa: 0.463

Prespecified descriptive-use requirements were:

- >=95% non-uncertain human coding
- >=80% exact agreement
- kappa >=0.70

Opening-policy classifications therefore will not be used for substantive descriptive
claims without additional independent validation or human recoding.

The classifier was particularly unreliable for Claude responses:

- Claude disagreement: 55.47%
- GPT disagreement: 10.94%

Notable confusion included automated `ems_priority` openings classified by the human
auditor as `urgency_label` in 30 sampled responses.

## Consequence for Study 3

No frozen machine labels or confirmatory results are altered.

Primary interpretation will instead rely on the more mechanically defined outcomes:

1. whether an explicit EMS directive occurs;
2. surface-word position of the first clean EMS directive, conditional on presence;
3. whether that directive begins within the first 10 surface words, conditional on presence.

The failed validation is reported transparently and limits interpretation rather than
triggering post hoc recoding or replacement of the preregistered H3 outcome.

The 256 human-coded validation responses may later be examined descriptively as an
explicitly exploratory validation-sample analysis, but such analysis cannot rehabilitate
the failed confirmatory H3 measure.
