# Figure 2 — Study 2 Matched-Role EMS-Latency Contrasts

**Manuscript:** Relationship Framing and Emergency Evidence in Language-Model Responses:
Three Studies of EMS Foregrounding

**Figure number:** 2

**Status:** SCIENTIFIC SPECIFICATION FROZEN BEFORE RENDERING

---

## 1. Scientific purpose

Figure 2 visualizes the four prespecified Study 2 matched female-coded versus male-coded
relationship contrasts in emergency-action latency.

Its principal scientific purpose is to show that the female/male difference does not
share a common direction across relational roles.

The figure supports the claim that the Study 2 relationship effect is not well summarized
as a single monotonic sex-coded bias.

---

## 2. Population and outcome

Study 2 primary analysis subset:

- explicit-emergency responses;
- explicit EMS directive present;
- nonmissing `first_ems_directive_word`.

N = 2,880.

Outcome:

`first_ems_directive_word`

defined as the 1-indexed surface-word position at which the first clean explicit
emergency-services directive begins.

Lower values indicate earlier EMS foregrounding.

---

## 3. Contrast definition

All plotted estimates are:

**male-coded referent minus matched female-coded referent**

Therefore:

- positive values = EMS directive appears later for the male-coded referent;
- negative values = EMS directive appears earlier for the male-coded referent;
- zero = no adjusted matched difference.

Contrasts are derived from the preregistered Study 2 primary HC3 OLS model adjusted for:

- model;
- system-prompt condition.

---

## 4. Values to plot

| Matched role | Contrast | Estimate | 95% CI | Raw p | Holm p |
|---|---|---:|---:|---:|---:|
| Diminutive parent | daddy - mommy | +4.2528 | [3.0678, 5.4377] | 2.00e-12 | 8.00e-12 |
| Parent | dad - mom | +1.9111 | [0.2725, 3.5498] | .02226 | .04452 |
| Dating partner | boyfriend - girlfriend | -0.6778 | [-3.6178, 2.2622] | .65138 | .65138 |
| Spouse | husband - wife | -3.2500 | [-5.2917, -1.2083] | .00181 | .00543 |

Role × gendered-referent interaction:

- Wald = 42.4846
- df = 3
- p = 3.16612e-09

---

## 5. Visual grammar

Preferred format:

Horizontal coefficient / forest plot.

Y-axis categories, top to bottom:

1. daddy - mommy
2. dad - mom
3. boyfriend - girlfriend
4. husband - wife

X-axis:

**Male-coded - female-coded difference in first EMS-directive word**

Include:

- point estimate;
- 95% CI;
- vertical reference line at zero.

Do not use significance stars as the primary visual encoding.

Optional small right-side text may provide Holm-adjusted p-values if this remains visually
clean, but the estimates and intervals should dominate.

Use a symmetric x-axis around zero if practical so sign differences are visually honest.

---

## 6. Intended interpretation

The figure should make immediately visible that:

- daddy - mommy is positive;
- dad - mom is positive;
- boyfriend - girlfriend is near zero and slightly negative;
- husband - wife is negative.

The matched contrasts therefore differ in both magnitude and direction.

This visual pattern, together with the prespecified role × gendered-referent interaction,
argues against summarizing Study 2 as a single uniform male-versus-female latency effect.

---

## 7. Interpretive boundary

Figure 2 does not establish:

- biological sex effects;
- gender effects independent of relationship wording;
- a universal property of all language models;
- a simple male-favoring or female-favoring bias.

The manipulated variables are gendered lexical referents embedded in distinct relationship
roles.

Do not describe a positive coefficient as inherently "more biased" than a negative one.

Do not infer relative effect magnitude merely from p-values.

---

## 8. Source files

Authoritative Study 2 sources:

- `study2/preregistration.md`
- `study2/analysis/confirmatory_results.json`
- `study2/analysis/confirmatory_results.md`

---

## 9. Draft caption

**Figure 2. Matched female-coded versus male-coded relationship contrasts in Study 2
EMS-directive latency.** Points show adjusted male-coded minus female-coded differences
in the first surface-word position at which an explicit EMS directive begins; horizontal
lines show 95% confidence intervals. Positive values indicate later EMS foregrounding
for the male-coded referent and negative values indicate earlier foregrounding. The
direction of the matched contrast varied across relational roles: daddy-mommy and
dad-mom contrasts were positive, boyfriend-girlfriend was near zero, and husband-wife
was negative. The prespecified role × gendered-referent interaction was significant,
Wald(3) = 42.48, p = 3.17e-9.

---

## 10. Verification checklist

- [ ] N = 2,880 primary eligible responses
- [ ] Contrast orientation is male-coded minus female-coded
- [ ] All four point estimates verified
- [ ] All four 95% CIs verified
- [ ] Holm-adjusted p-values verified
- [ ] Role × gendered-referent Wald/df/p verified
- [ ] Zero reference line shown
- [ ] Axis meaning makes positive/negative direction unambiguous
- [ ] No claim of a generic sex effect
