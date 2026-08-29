# Figure 3 — Study 3 Relationship × Emergency-Evidence Latency Surfaces

**Manuscript:** Relationship Framing and Emergency Evidence in Language-Model Responses:
Three Studies of EMS Foregrounding

**Figure number:** 3

**Status:** SCIENTIFIC SPECIFICATION FROZEN BEFORE RENDERING

---

## 1. Scientific purpose

Figure 3 visualizes the primary Study 3 relationship × certainty interaction in
conditional EMS-directive latency separately for the two tested model endpoints.

Its scientific purpose is to show:

1. substantial relationship-conditioned variation under lower-certainty evidence;
2. contraction of that variation as emergency evidence strengthens;
3. materially different convergence trajectories for Claude and GPT.

The figure is the primary visual representation of Study 3 H1.

---

## 2. Population and outcome

Population:

Study 3 canonical responses containing an explicit EMS directive.

N = 14,991.

Outcome:

`first_ems_directive_word`

defined as the 1-indexed surface-word position at which the first clean explicit
emergency-services directive begins.

Lower values indicate earlier EMS foregrounding.

The plotted quantities are adjusted relationship × certainty estimates averaged equally
over prompt variant and system-prompt condition within each model.

---

## 3. Emergency-evidence axis

Four ordered evidence/certainty levels:

### L1 — retained responsiveness

Variant A:
the referent keeps falling asleep but can be awakened.

Variant B:
the referent keeps falling asleep but responds when called by name.

### L2 — unresponsiveness

Variant A:
the referent will not wake up.

Variant B:
the referent does not respond when called by name.

### L3 — unresponsiveness + abnormal breathing

L2 structure plus respiratory abnormality (`breathing weird`).

### L4 — unresponsiveness + severely compromised breathing

L2 structure plus `barely breathing`.

The x-axis represents increasing supplied emergency evidence from L1 through L4.

---

## 4. Claude adjusted latency estimates

| Relationship | L1 | L2 | L3 | L4 |
|---|---:|---:|---:|---:|
| boyfriend | 110.53 | 55.73 | 8.70 | 4.30 |
| dad | 65.27 | 14.83 | 5.13 | 4.40 |
| daddy | 42.47 | 8.77 | 4.41 | 4.01 |
| girlfriend | 113.86 | 50.60 | 7.10 | 3.81 |
| husband | 87.31 | 29.04 | 4.34 | 3.33 |
| mom | 61.84 | 19.55 | 2.85 | 3.32 |
| mommy | 33.91 | 12.47 | 4.85 | 4.28 |
| wife | 99.58 | 41.50 | 5.39 | 3.01 |

Across-relationship adjusted range:

- L1: 79.96 words
- L2: 46.97 words
- L3: 5.85 words
- L4: 1.39 words

---

## 5. GPT adjusted latency estimates

| Relationship | L1 | L2 | L3 | L4 |
|---|---:|---:|---:|---:|
| boyfriend | 35.95 | 7.89 | 1.00 | 1.00 |
| dad | 15.65 | 1.06 | 1.00 | 1.00 |
| daddy | 20.62 | 1.46 | 1.00 | 1.00 |
| girlfriend | 40.41 | 6.05 | 1.00 | 1.00 |
| husband | 20.91 | 1.31 | 1.00 | 1.00 |
| mom | 13.40 | 1.00 | 1.00 | 1.00 |
| mommy | 10.62 | 1.05 | 1.00 | 1.00 |
| wife | 19.64 | 1.10 | 1.00 | 1.00 |

Across-relationship adjusted range:

- L1: 29.79 words
- L2: 6.89 words
- L3: 0
- L4: 0

Raw-response verification:

- GPT L3: 1,920 / 1,920 responses begin the first clean EMS directive at surface-word 1.
- GPT L4: 1,920 / 1,920 responses begin the first clean EMS directive at surface-word 1.

This is literal raw saturation, not merely convergence of adjusted model estimates.

---

## 6. Primary inferential result

Study 3 H1:

relationship × certainty interaction in conditional EMS latency.

- N = 14,991
- Wald = 1334.965
- df = 21
- p = 7.95e-270

Rank diagnostics subsequently verified:

- nominal restrictions = 21
- covariance rank = 21
- design matrix full rank
- no rank deficiency.

The figure visualizes estimates; the Wald statistic provides the formal omnibus test.

---

## 7. Visual grammar

Preferred format:

Two side-by-side panels:

### Panel A — Claude Sonnet 5
### Panel B — GPT-5.6 Terra

Both panels must use the SAME y-axis.

X-axis:

L1 → L2 → L3 → L4

Suggested tick labels:

- `L1` / `responsive`
- `L2` / `unresponsive`
- `L3` / `+ abnormal breathing`
- `L4` / `+ barely breathing`

Y-axis:

**Adjusted first EMS-directive word**

Eight relationship traces appear in each panel.

Use the same relationship marker/line identity in both panels.

Because eight traces may overlap at higher certainty, distinguish relationships using
a combination of line/marker identity rather than relying only on color.

Legend should be shared across panels.

Preferred y-axis range:

approximately 0–120 words.

This common scale is intentional and should not be replaced by separate model-specific
scales merely to enlarge the GPT differences.

---

## 8. GPT saturation annotation

Panel B should contain a small unobtrusive annotation near L3/L4:

**L3/L4: every raw response begins EMS directive at word 1**

or equivalently:

**L3/L4 raw saturation: 1,920 / 1,920 at word 1**

The annotation should make clear that complete convergence is observed directly in the
raw responses.

---

## 9. Intended interpretation

The figure should make visible that:

### Claude

Relationship-conditioned latency differences are extremely large at L1 and remain
substantial at L2.

They collapse sharply once respiratory abnormality is supplied and become very small
at L4.

### GPT

Relationship-conditioned latency differences are present at L1, substantially reduced
at L2, and disappear completely at L3.

At both L3 and L4 every response begins the first clean EMS directive at word 1.

### Cross-model

Both models show increasing constraint from stronger emergency evidence, but they reach
convergence through materially different trajectories.

---

## 10. Interpretive boundary

Figure 3 does not establish:

- that relationship terms operate through one latent mechanism;
- that certainty is a psychological state inside the model;
- that the two endpoints represent all language-model families;
- that the relationship effect decreases monotonically in every measured response
  dimension.

The figure concerns conditional EMS-directive latency only.

Claude L1 conditional latency must be interpreted alongside the EMS-presence result:
EMS omission at L1 is relationship-dependent, so the latency population is selectively
conditioned on responses in which EMS is present.

---

## 11. Source files

Authoritative Study 3 sources:

- `study3/ANALYSIS_PLAN.md`
- `study3/data/confirmatory_analysis.json`
- Study 3 model-specific latency diagnostic output
- `study3/STUDY3_RESULTS_MAP.md`
- `checkpoints/2026-08-29_Study3_Analysis_Freeze_PreDraft.md`

---

## 12. Draft caption

**Figure 3. Model-specific relationship × emergency-evidence surfaces for Study 3
EMS-directive latency.** Lines show adjusted first EMS-directive word position for the
eight relationship referents across four increasingly diagnostic levels of supplied
emergency evidence, averaged equally over prompt variant and system-prompt condition
within each model. Lower values indicate earlier EMS foregrounding. Both models showed
substantial relationship-conditioned variation under lower-certainty evidence and
marked convergence as the emergency evidence strengthened, but their trajectories
differed. GPT maintained universal EMS inclusion and reached complete raw-response
word-1 convergence at L3: all 1,920 L3 responses, and all 1,920 L4 responses, began the
first clean EMS directive at word 1. Claude converged more gradually and retained a
small latency range through L4. The preregistered relationship × certainty latency
interaction was significant, Wald(21) = 1334.96, p = 7.95e-270.

---

## 13. Verification checklist

- [ ] Conditional EMS N = 14,991
- [ ] All 32 Claude adjusted values verified
- [ ] All 32 GPT adjusted values verified
- [ ] Common y-axis used
- [ ] H1 Wald = 1334.965 verified
- [ ] H1 df = 21 verified
- [ ] H1 p = 7.95e-270 verified
- [ ] GPT L3 raw word-1 saturation verified
- [ ] GPT L4 raw word-1 saturation verified
- [ ] Claude L1 selection caveat preserved
- [ ] No H3/opening-policy results enter the figure
- [ ] No latent-mechanism claim made
