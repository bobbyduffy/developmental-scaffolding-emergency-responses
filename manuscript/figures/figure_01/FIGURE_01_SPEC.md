# Figure 1 — Three-Study Design Progression

**Manuscript:** Relationship Framing and Emergency Evidence in Language-Model Responses:
Three Studies of EMS Foregrounding

**Figure number:** 1

**Status:** SCIENTIFIC SPECIFICATION FROZEN BEFORE RENDERING

---

## 1. Scientific purpose

Figure 1 orients the reader to the sequential empirical logic of the three-study
research program.

The progression is:

**discovery → prospective replication/decomposition → boundary-condition test**

The figure should show how each study answers a question left open by the preceding
study rather than presenting three independent experiments of equal conceptual role.

Study 1 identifies the phenomenon.
Study 2 prospectively tests and decomposes it.
Study 3 manipulates supplied emergency evidence to test when the phenomenon contracts.

---

## 2. Narrative position

Figure 1 should appear near the end of the Introduction, immediately before or near
the manuscript's overview of the three studies.

Its primary job is orientation, not statistical reporting.

The figure should allow a reader to understand within approximately 20 seconds:

1. what changed from Study 1 to Study 2;
2. what changed from Study 2 to Study 3;
3. why Study 3 is the logical destination of the sequence.

---

# 3. Study 1 — Discovery

## Scientific question

Does relationship/developmental wording change language-model emergency guidance and
linguistic response behavior when the same underlying situation is described using
different relationship terms?

## Design

- Models:
  - `gpt-5.6-terra`
  - `claude-sonnet-5`
- 3 system-prompt conditions
- 4 female-coded relationship/developmental cues:
  - mommy
  - mom
  - girlfriend
  - wife
- Emergency cue:
  - absent
  - present (`won't wake up`)
- 60 repetitions per exact cell
- Total N = 2,880
- 2,880 / 2,880 successful responses

## Preregistered primary outcome

Binary explicit EMS instruction (`ems_instruction`).

## Confirmatory result relevant to the trilogy

Explicit unresponsiveness produced a complete EMS-inclusion ceiling:

- emergency cue present: 1,440 / 1,440 = 100% EMS instruction;
- emergency cue absent: 694 / 1,440 = 48.19%.

Relationship wording strongly affected precautionary EMS inclusion before the explicit
emergency cue.

## Discovery that motivated Study 2

Within the explicit-emergency ceiling, exploratory post-coding analyses showed that
relationship wording altered how prominently and quickly emergency guidance was
communicated.

In emergency responses, first-911 position varied substantially by relationship term.
For example, the adjusted girlfriend-versus-mommy difference was approximately
+12.84 words.

These latency analyses were exploratory in Study 1.

## Figure-level result statement

**Relationship framing affected emergency-response policy even when eventual EMS
inclusion was at ceiling; exploratory analyses identified EMS foregrounding latency
as a candidate measurable phenomenon.**

## Interpretive limitation

Study 1 contained only female-coded referents.

It therefore could not determine whether the pattern represented:

- a general relationship-role effect;
- a uniform sex-coded effect;
- or role-specific differences.

Latency was discovered post hoc and was not the preregistered Study 1 primary outcome.

---

# 4. Study 2 — Prospective replication and decomposition

## Scientific question

Does referent framing prospectively alter how quickly an explicit emergency-action
directive is communicated when the described person is high and unresponsive?

And:

Can the relationship effect be reduced to a common female-coded versus male-coded
difference?

## Design

- Models:
  - `gpt-5.6-terra`
  - `claude-sonnet-5`
- 3 system-prompt conditions
- 8 contemporaneously randomized referents:
  - mommy / daddy
  - mom / dad
  - girlfriend / boyfriend
  - wife / husband
- Emergency cue:
  - absent
  - present
- 60 repetitions per exact cell
- Total N = 5,760
- 5,760 / 5,760 successful responses

Female- and male-coded matched referents were collected contemporaneously in the same
randomized run, avoiding confounding of matched comparisons with run date.

## Preregistered primary outcome

`first_ems_directive_word`:

the 1-indexed surface-word position at which the first clean explicit EMS directive
begins.

Primary inference was restricted to explicit-emergency responses containing an EMS
directive.

## Primary result

Relationship/referent framing strongly affected EMS-directive latency:

- N = 2,880 primary eligible emergency responses
- Wald = 406.196
- df = 7
- p = 1.12e-83

## Matched-role decomposition

Male-coded minus female-coded adjusted latency contrasts:

- daddy − mommy: +4.253 words
- dad − mom: +1.911 words
- boyfriend − girlfriend: −0.678 words
- husband − wife: −3.250 words

Three of four contrasts survived Holm correction except boyfriend − girlfriend.

The role × gendered-referent interaction was also strong:

- Wald = 42.485
- df = 3
- p = 3.17e-9

## Figure-level result statement

**EMS-foregrounding latency prospectively replicated across eight referents, but
matched female/male contrasts differed in direction and magnitude across relational
roles.**

## Interpretive limitation

Study 2 establishes that the phenomenon is not well summarized as one uniform
male-versus-female scalar bias.

However, all explicit-emergency prompts used the same decisive unresponsiveness cue.

The study therefore did not establish how relationship-conditioned differences behave
as the strength of supplied emergency evidence changes.

---

# 5. Study 3 — Emergency evidence as a boundary condition

## Scientific question

Does increasing supplied emergency evidence reduce relationship-conditioned
differences in how quickly a model foregrounds emergency services?

## Design

- Models:
  - `gpt-5.6-terra`
  - `claude-sonnet-5`
- 3 system-prompt conditions
- 8 matched relationship referents:
  - mommy / daddy
  - mom / dad
  - girlfriend / boyfriend
  - wife / husband
- 4 emergency-evidence / certainty levels
- 2 prompt variants
- 40 repetitions per exact cell
- 384 cells
- Planned N = 15,360
- Canonical successful N = 15,360

The four evidence levels progressively move from retained responsiveness or ambiguous
responsiveness toward nonresponsiveness plus increasingly explicit respiratory danger.

## Primary framework

Study 3 uses a two-part EMS framework:

1. whether an explicit EMS instruction appears;
2. conditional on EMS appearance, how quickly it is foregrounded.

Primary latency outcome:

`first_ems_directive_word`.

Mechanical prominence outcome:

EMS directive beginning within the first 10 surface words.

## Primary result

Conditional EMS latency showed a strong relationship × certainty interaction:

- N = 14,991 EMS-present responses
- Wald = 1334.965
- df = 21
- p = 7.95e-270

The full 21-df restriction set was subsequently verified as full rank.

## Model-specific convergence

GPT:

- EMS presence = 100% throughout;
- relationship-conditioned foregrounding differences occur primarily at L1/L2;
- at L3, all 1,920 responses begin the first clean EMS directive at word 1;
- the same complete word-1 convergence remains at L4.

Claude:

- relationship-conditioned EMS omission occurs primarily under L1 ambiguity;
- inclusion is essentially saturated by L2 and fully saturated at L3/L4;
- substantial relationship-conditioned prominence/latency variation remains at L2;
- differences contract sharply under respiratory evidence.

## Mechanical synthesis

Relationship-conditioned variation changes not only in magnitude but, for Claude,
in which response dimension carries it.

At low certainty, Claude shows substantial relationship variation in EMS inclusion.
Once inclusion saturates, the variation is expressed primarily through prominence
and latency before largely disappearing under stronger respiratory evidence.

## Figure-level result statement

**Relationship-conditioned emergency-response differences are largest when supplied
medical evidence leaves greater room for response-policy discretion and contract as
the evidence becomes increasingly decisive; models differ in which response dimension
carries that variation.**

## Interpretive limitation

Study 3 establishes a boundary condition on the observed output phenomenon.

It does not establish the latent cognitive, representational, developmental, or social
mechanism that produces the relationship-conditioned differences.

---

# 6. Cross-study logical progression

The visual should communicate the following sequence:

### STUDY 1
**DISCOVERY**

Relationship cue
+
emergency cue

→

Eventual EMS inclusion reaches ceiling under unresponsiveness,
but exploratory analyses reveal relationship-conditioned
differences in urgency / EMS foregrounding latency.

↓

### STUDY 2
**PROSPECTIVE REPLICATION & DECOMPOSITION**

Eight matched relationship referents
+
prospectively frozen EMS latency outcome

→

Latency effect replicates strongly.
Matched female/male contrasts vary by relational role
rather than following one common direction.

↓

### STUDY 3
**BOUNDARY CONDITION**

Eight matched relationship referents
×
four levels of supplied emergency evidence

→

Relationship-conditioned differences contract as evidence becomes decisive.
The response dimension carrying the effect differs by model.

---

# 7. Visual grammar

Preferred layout:

Three horizontally arranged panels connected by rightward arrows.

Each panel should contain four visually distinct levels:

1. Study number and conceptual role
2. Experimental manipulation
3. Scientific question
4. Concise result

Suggested panel headings:

- **Study 1 — Discovery**
- **Study 2 — Replication & decomposition**
- **Study 3 — Boundary condition**

The three panels should visually increase in experimental constraint/structure from
left to right.

Suggested conceptual shorthand beneath each heading:

### Study 1

`4 relationship cues × emergency absent/present`

Question:

**Does relationship wording alter emergency guidance?**

Result:

**Foregrounding differences discovered beneath an EMS ceiling**

Small footer:

`2 models · 3 systems · 60 reps/cell · N = 2,880`

### Study 2

`8 matched referents × emergency absent/present`

Question:

**Does EMS latency replicate, and is it a uniform sex-coded effect?**

Result:

**Latency replicates; matched contrasts differ by relational role**

Small footer:

`2 models · 3 systems · 60 reps/cell · N = 5,760`

### Study 3

`8 matched referents × 4 evidence levels × 2 variants`

Question:

**Does stronger emergency evidence constrain the relationship effect?**

Result:

**Relationship-conditioned differences contract as evidence becomes decisive**

Small footer:

`2 models · 3 systems · 40 reps/cell · N = 15,360`

A very short secondary line may note:

**Model families converge through different response-policy trajectories.**

---

# 8. Interpretive boundary

Figure 1 is a conceptual/design schematic, not an effect-size figure.

It must not imply:

- that Study 1 latency was preregistered;
- that Study 2 supports a uniform sex effect;
- that Study 3 proves a latent psychological mechanism;
- that repeated model outputs represent independent human participants;
- that the tested models constitute a representative sample of all language models.

The intended progression is empirical:

**observation → prospective replication/decomposition → manipulated boundary test**

not:

**observation → proof of bias → proof of mechanism**.

---

# 9. Source files

## Study 1

- `study1/preregistration.md`
- `study1/README.md`
- `checkpoints/2026-08-28-study1-analysis-checkpoint.md`

## Study 2

- `study2/preregistration.md`
- `study2/analysis/confirmatory_results.md`
- `study2/README.md`

## Study 3

- `study3/preregistration.md`
- `study3/ANALYSIS_PLAN.md`
- `study3/STUDY3_RESULTS_MAP.md`
- `checkpoints/2026-08-29_Study3_Analysis_Freeze_PreDraft.md`

---

# 10. Draft caption

**Figure 1. Sequential design of the three-study research program.**
Study 1 tested whether relationship/developmental wording altered language-model
emergency guidance. Although explicit unresponsiveness produced universal EMS
instruction, exploratory analyses identified relationship-conditioned differences in
the latency and prominence of emergency guidance. Study 2 prospectively elevated EMS
directive latency to the primary outcome and tested eight contemporaneously randomized
matched referents; latency differences replicated, while female/male matched contrasts
varied across relational roles rather than following a common direction. Study 3 then
manipulated the strength of supplied emergency evidence across four levels. Relationship-
conditioned differences in EMS foregrounding were greatest when the evidence permitted
more response-policy variation and contracted sharply as respiratory evidence became
more decisive, with different model-specific trajectories. The studies used separately
collected response sets and progressively constrained the interpretation of the observed
relationship-framing effect.

---

# 11. Verification checklist before rendering

- [ ] Study 1 N = 2,880 verified
- [ ] Study 1 latency explicitly labeled exploratory
- [ ] Study 1 emergency EMS ceiling = 1,440 / 1,440 verified
- [ ] Study 2 N = 5,760 verified
- [ ] Study 2 primary eligible emergency N = 2,880 verified
- [ ] Study 2 H1 Wald/df/p verified
- [ ] Study 2 matched-pair directions verified
- [ ] Study 3 N = 15,360 verified
- [ ] Study 3 H1 Wald/df/p verified
- [ ] Study 3 GPT L3/L4 word-1 convergence verified
- [ ] No mechanistic claim exceeds the frozen analysis
- [ ] No failed H3/opening-policy result is used to support the figure
