# Study 3 Analysis Freeze — Pre-Draft Checkpoint

**Date:** 2026-08-29  
**Status:** analysis complete; manuscript drafting may begin.

## Purpose

This checkpoint marks the end of the planned Study 3 analysis phase before drafting
the empirical manuscript:

**Relationship Framing and Emergency Evidence in Language-Model Responses:
Three Studies of EMS Foregrounding**

The authoritative manuscript-facing interpretation is summarized in:

- `study3/STUDY3_RESULTS_MAP.md`

Historical checkpoints remain unchanged and should be read as records of the analysis
state at the time they were created.

## Final data state

Study 3 contains:

- 15,360 planned trial IDs
- 15,360 canonical successful responses
- 384 design cells
- 40 canonical successful responses per cell
- 0 empty successful responses
- 0 truncated successful responses

An initial collection interruption left 315 missing Claude trials because API credits
were exhausted. These were recovered append-only. Earlier failed/missing records were
retained as provenance.

Raw-file SHA differences between Windows working-tree and Git blob representations were
fully explained by CRLF/LF normalization and not by data differences.

## Final inferential state

### Supported manuscript outcomes

The empirical manuscript may substantively interpret:

1. EMS presence;
2. first EMS-directive word position conditional on EMS presence;
3. EMS appearance within the first 10 words conditional on EMS presence;
4. preregistered matched-pair and heterogeneity analyses associated with these outcomes;
5. prespecified secondary/sensitivity analyses;
6. post-confirmatory mechanical-endpoint synthesis when clearly labeled descriptive.

### H3 validation failure

The automated `ems_priority_opening` measure failed prospectively specified human
validation criteria.

The frozen confirmatory result remains preserved but will not receive substantive
inferential interpretation.

### Opening-policy validation failure

The automated `opening_policy` classifier also failed validation and will not be used
for substantive descriptive claims.

No frozen labels or confirmatory outputs were altered after validation.

## Central Study 3 result

The preregistered relationship × certainty interaction for conditional EMS latency is
strong and full-rank.

Increasingly decisive emergency evidence sharply compresses relationship-conditioned
differences in EMS foregrounding.

The manifestation differs by model endpoint.

### GPT-5.6 Terra

- EMS inclusion is 100% at every certainty level.
- Relationship-conditioned prominence/latency differences occur at L1 and L2.
- At L3, all 1,920 GPT responses begin the first clean EMS directive at surface-word 1.
- At L4, all 1,920 GPT responses likewise begin the directive at word 1.

### Claude Sonnet 5

- Under L1 ambiguity, relationship framing affects EMS inclusion as well as latency.
- EMS inclusion is essentially saturated by L2 and fully saturated at L3/L4.
- Large relationship-conditioned prominence and latency differences remain at L2.
- These differences contract sharply at L3 and are small by L4.

The post-confirmatory mechanical synthesis therefore suggests that relationship-conditioned
variation need not shrink uniformly across every endpoint. In Claude, the locus of
variation shifts from EMS inclusion under low certainty toward EMS prominence once
inclusion saturates, before largely disappearing under stronger respiratory evidence.

## Cross-study interpretation to carry into the manuscript

Study 1 identified relationship-conditioned emergency-response differences.

Study 2 replicated the latency phenomenon while showing that matched male/female
contrasts differ in direction and magnitude across relational roles; the effect is not
well characterized as a simple monotonic sex bias.

Study 3 establishes emergency evidence as a major boundary condition: relationship
framing matters most when the supplied medical evidence permits greater response-policy
discretion, and the differences largely collapse as emergency evidence becomes decisive.

The empirical manuscript should establish this result without claiming to have resolved
the underlying cognitive or representational mechanism.

## Final authoritative Study 3 files

### Frozen design and coding

- `study3/preregistration.md`
- `study3/ANALYSIS_PLAN.md`
- `study3/CODING_RULES.md`
- `study3/STIMULI.md`
- `study3/POST_FREEZE_DEVIATIONS.md`

### Core data

- `study3/data/full.jsonl`
- `study3/data/results.jsonl`
- `study3/data/raw_integrity.json`

### Confirmatory analysis

- `study3/analyze_results.py`
- `study3/data/confirmatory_analysis.json`

### Secondary / sensitivity

- `study3/secondary_reporting.py`
- `study3/data/secondary_reporting.json`
- `study3/presence_sensitivity.py`
- `study3/data/presence_sensitivity.json`
- `study3/latency_surface_diagnostics.py`
- `study3/data/latency_surface_diagnostics.json`
- `study3/h4_prominence_analysis.py`
- `study3/data/h4_prominence_analysis.json`

### Mechanical synthesis

- `study3/mechanical_endpoint_synthesis.py`
- `study3/data/mechanical_endpoint_surface.csv`
- `study3/data/mechanical_endpoint_relationship_spreads.csv`
- `study3/data/mechanical_endpoint_synthesis.json`

### Validation

- `study3/H3_OPENING_VALIDATION_SPEC.md`
- `study3/H3_OPENING_VALIDATION_ADDENDUM.md`
- `study3/H3_VALIDATION_DISPOSITION.md`
- `study3/data/h3_opening_validation_human.csv`
- `study3/data/h3_opening_validation_results.json`

### Manuscript source-of-truth

- `study3/STUDY3_RESULTS_MAP.md`

## Known manuscript caveats

- Study 3 uses two model endpoints.
- Responses are single-shot completions rather than multi-turn emergency interactions.
- Relationship referents bundle social-role, age-associated, linguistic, and other learned
  associations that are not independently identified by this design.
- Conditional latency and within-10 outcomes necessarily exclude EMS-absent responses.
- This selection issue is especially important for Claude at L1, where omission is
  strongly relationship-conditioned.
- Prompt wording and system condition can materially alter some response patterns.
- Binary outcomes were analyzed using the preregistered HC3 linear-probability approach;
  adjusted predictions can therefore slightly exceed natural probability bounds.
- Automated discourse-level H3/opening-policy measures failed human validation and are
  excluded from substantive interpretation.
- No benign true non-emergency baseline was included.

## Analysis-freeze rule

From this checkpoint forward, new analyses should not be undertaken merely because
additional slicing is possible.

A new analysis is appropriate only to:

- construct a preregistered/prespecified manuscript result;
- produce a figure or table from already established results;
- resolve a concrete reporting ambiguity;
- verify reproducibility;
- answer a reviewer/editor request; or
- investigate a clearly labeled new exploratory question.

No post-freeze analysis may be retrospectively represented as confirmatory.

## Next phase

The next phase is manuscript construction:

1. finalize figure/table specifications;
2. draft Study 1 and Study 2 as the empirical build-up;
3. draft Study 3 as the central boundary-condition study;
4. report the H3 validation failure transparently;
5. synthesize the three studies;
6. keep broader theoretical interpretation constrained for the separate theoretical paper.
