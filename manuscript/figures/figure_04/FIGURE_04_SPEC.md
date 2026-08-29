# Figure 4 — Study 3 Mechanical-Endpoint Relationship-Spread Heatmap

**Manuscript:** Relationship Framing and Emergency Evidence in Language-Model Responses:
Three Studies of EMS Foregrounding

**Figure number:** 4

**Status:** SCIENTIFIC SPECIFICATION FROZEN BEFORE RENDERING

---

## 1. Scientific purpose

Figure 4 provides a descriptive synthesis of Study 3 by showing how much
relationship-conditioned variation remains at each level of supplied emergency evidence
across three mechanically defined response endpoints.

The figure is intended to reveal not merely contraction of relationship-conditioned
variation, but changes in the response dimension in which that variation is expressed.

It is a descriptive synthesis. It performs no new inferential test.

---

## 2. Endpoints

Three endpoints are displayed.

### EMS presence

Population:
all valid canonical responses.

Quantity:
maximum minus minimum adjusted EMS-presence estimate across the eight relationship
conditions within each model × certainty level.

Unit:
percentage points.

### EMS within first 10 words

Population:
responses containing an EMS directive.

Quantity:
maximum minus minimum adjusted probability of the first clean EMS directive beginning
within the first 10 surface words across the eight relationship conditions within each
model × certainty level.

Unit:
percentage points.

### EMS latency

Population:
responses containing an EMS directive.

Quantity:
maximum minus minimum adjusted `first_ems_directive_word` estimate across the eight
relationship conditions within each model × certainty level.

Unit:
surface words.

---

## 3. Values

| Model | Certainty | EMS presence range | Within-10 range | Latency range |
|---|---:|---:|---:|---:|
| Claude | L1 | 53.33 pp | 15.56 pp | 79.96 words |
| Claude | L2 | 1.25 pp | 62.92 pp | 46.97 words |
| Claude | L3 | 0.00 pp | 27.50 pp | 5.85 words |
| Claude | L4 | 0.00 pp | 5.00 pp | 1.39 words |
| GPT | L1 | 0.00 pp | 59.17 pp | 29.79 words |
| GPT | L2 | 0.00 pp | 36.25 pp | 6.89 words |
| GPT | L3 | 0.00 pp | 0.00 pp | 0.00 words |
| GPT | L4 | 0.00 pp | 0.00 pp | 0.00 words |

---

## 4. Visual grammar

Preferred format:

Three adjacent one-column heatmaps:

1. EMS presence spread
2. EMS ≤10-word spread
3. EMS latency spread

Rows, top to bottom:

- Claude L1
- Claude L2
- Claude L3
- Claude L4
- GPT L1
- GPT L2
- GPT L3
- GPT L4

Claude and GPT row groups should be visually separated.

Each endpoint column MUST use its own numerical scale because the units and ranges are
not comparable.

Color/shading intensity therefore means:

**larger relationship spread within that endpoint**

not a common standardized effect size across all three endpoints.

Every cell should print its raw numerical value.

Suggested displayed precision:

- percentage-point endpoints: one decimal place;
- latency: one decimal place.

---

## 5. Intended interpretation

### Claude

L1:
relationship-conditioned variation is large in EMS inclusion and conditional latency.

L2:
EMS inclusion has almost saturated, while very large relationship-conditioned
variation remains in whether EMS is foregrounded within 10 words and in latency.

L3:
EMS inclusion is fully saturated; latency variation is small, but some prominence
variation remains.

L4:
all three mechanical endpoints are nearly compressed.

This supports a descriptive account in which the locus of relationship-conditioned
variation shifts across response dimensions as emergency evidence strengthens.

### GPT

EMS presence is invariant at 100% across all certainty levels.

Relationship-conditioned variation appears in prominence and latency at L1 and L2.

At L3 and L4, all three spread measures are zero.

This displays complete mechanical convergence under respiratory evidence.

---

## 6. Important conditioning caveat

The within-10 and latency endpoints are conditional on EMS presence.

This matters especially for Claude L1, where EMS omission is itself strongly
relationship-dependent.

Therefore the three endpoint columns should be interpreted jointly rather than treating
the Claude L1 conditional latency/prominence populations as if selection into EMS
presence were random.

---

## 7. Inferential boundary

Figure 4 is descriptive.

It does not:

- perform a new omnibus test;
- imply that the three endpoint spreads are directly numerically comparable;
- establish separate latent mechanisms;
- show standardized effect sizes;
- imply monotonic decline in every individual endpoint.

The figure summarizes already frozen mechanical endpoint estimates.

Formal inference is reported elsewhere.

---

## 8. Source files

Authoritative sources:

- `study3/data/mechanical_endpoint_relationship_spreads.csv`
- `study3/data/mechanical_endpoint_surface.csv`
- `study3/data/mechanical_endpoint_synthesis.json`
- `study3/mechanical_endpoint_synthesis.py`
- `study3/STUDY3_RESULTS_MAP.md`

---

## 9. Draft caption

**Figure 4. Relationship-conditioned spread across three mechanical Study 3 emergency-
response endpoints.** Cells show the range between the maximum and minimum adjusted
relationship estimate within each model × evidence level. EMS presence and EMS-within-
10 spreads are expressed in percentage points; latency spread is expressed in surface
words. Each endpoint column is independently scaled, so shading indicates the relative
magnitude of relationship-conditioned variation within that endpoint rather than a
common effect-size metric across columns. Claude shows substantial relationship-
conditioned EMS inclusion variation at L1; once inclusion saturates, variation shifts
primarily into EMS prominence and latency before largely disappearing under stronger
respiratory evidence. GPT maintains universal EMS inclusion and varies primarily in
foregrounding at L1/L2, reaching zero relationship spread across all three mechanical
endpoints at L3/L4. The within-10 and latency measures are conditional on EMS presence.

---

## 10. Verification checklist

- [ ] Claude L1 values = 53.33 / 15.56 / 79.96
- [ ] Claude L2 values = 1.25 / 62.92 / 46.97
- [ ] Claude L3 values = 0 / 27.50 / 5.85
- [ ] Claude L4 values = 0 / 5.00 / 1.39
- [ ] GPT L1 values = 0 / 59.17 / 29.79
- [ ] GPT L2 values = 0 / 36.25 / 6.89
- [ ] GPT L3 = 0 / 0 / 0
- [ ] GPT L4 = 0 / 0 / 0
- [ ] Endpoint columns independently scaled
- [ ] Raw numerical values printed in every cell
- [ ] Claude/GPT groups visually distinguishable
- [ ] Conditional-on-EMS caveat preserved
- [ ] Figure labeled descriptive rather than inferential

---

# Revision 1 — Visual grammar supersession

**Decision made before final rendering.**

The originally specified heatmap representation is superseded by three aligned
horizontal-bar small multiples.

Reason:

The heatmap treatment visually encouraged two misleading readings:

1. contiguous cells made independent model × certainty conditions resemble a continuous
   or stacked quantity;
2. independently scaled color columns encouraged visual comparison of "heat" across
   endpoints measured in unlike units.

The underlying scientific quantities, conditioning rules, source files, and intended
interpretation are unchanged.

## Revised visual grammar

Use three aligned horizontal-bar panels with identical categorical rows:

1. EMS presence spread
2. EMS ≤10-word spread
3. EMS latency spread

Rows, top to bottom:

- Claude L1
- Claude L2
- Claude L3
- Claude L4
- GPT L1
- GPT L2
- GPT L3
- GPT L4

A visible gap should separate the Claude and GPT groups.

Each bar begins at zero.

Each bar should have its numerical value printed directly.

The first two panels are both expressed in percentage points and should therefore share
the same x-axis range.

The latency panel is expressed in surface words and should use a separate word-based
x-axis range.

Preferred axis ranges:

- EMS presence spread: 0–65 percentage points
- EMS ≤10-word spread: 0–65 percentage points
- EMS latency spread: 0–85 words

The revised figure should make magnitude visible through bar length rather than color
intensity.

This revision supersedes Section 4 ("Visual grammar") of the original specification.
All other sections remain in force.
