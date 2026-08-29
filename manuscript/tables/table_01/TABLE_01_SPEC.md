# Table 1 — Three-Study Design and Sample Overview

**Manuscript:** Relationship Framing and Emergency Evidence in Language-Model Responses:
Three Studies of EMS Foregrounding

**Table number:** 1

**Status:** SCIENTIFIC SPECIFICATION FROZEN BEFORE RENDERING

---

## 1. Scientific purpose

Table 1 provides a methods-at-a-glance comparison of Studies 1–3.

Its job is descriptive orientation.

Figure 1 shows the intellectual progression of the research program.
Table 1 shows the experimental anatomy: what remained constant, what changed, and
which outcome was primary in each study.

The table does not report inferential results.

---

## 2. Common experimental backbone

All three studies used the same two model endpoints:

- `claude-sonnet-5` — Claude Sonnet 5
- `gpt-5.6-terra` — GPT-5.6 Terra

All three studies used the same three experimenter system-prompt conditions:

1. none;
2. minimal identity/date;
3. identity/date plus the frozen helpful/direct/brief assistant instruction.

Experimental prompts were cold, single-turn trials without conversational carryover.

Because these features are identical across the trilogy, they should be stated in the
table note rather than repeated in every row.

---

## 3. Table columns

1. Study
2. Research role
3. Relationship framing
4. Emergency/evidence manipulation
5. Prompt-variant factor
6. Repetitions per exact cell
7. Total N
8. Primary endpoint

---

## 4. Study 1

**Research role:** Discovery

**Relationship framing:**

Four female-coded relationship terms:

- mommy
- mom
- girlfriend
- wife

**Emergency/evidence manipulation:**

Binary emergency cue:

- high only;
- high + explicit unresponsiveness (`won't wake up`).

**Prompt-variant factor:** None.

**Repetitions per exact cell:** 60

**Total N:** 2,880

**Preregistered primary endpoint:**

`ems_instruction` — presence/absence of an explicit EMS directive.

**Important epistemic distinction:**

EMS foregrounding latency was discovered exploratorily in Study 1 and must not be
represented as the preregistered Study 1 primary endpoint.

---

## 5. Study 2

**Research role:** Prospective replication and decomposition

**Relationship framing:**

Eight contemporaneously randomized matched referents:

- mommy / daddy
- mom / dad
- girlfriend / boyfriend
- wife / husband

**Emergency/evidence manipulation:**

Binary emergency cue:

- high only;
- high + explicit unresponsiveness (`she/he won't wake up`).

**Prompt-variant factor:** None.

**Repetitions per exact cell:** 60

**Total N:** 5,760

**Preregistered primary endpoint:**

`first_ems_directive_word` — first surface-word position of the first clean explicit
EMS directive.

Primary inference was restricted to explicit-emergency responses containing an EMS
directive.

Study 2 prospectively tests the foregrounding phenomenon identified in Study 1 using
a sharpened directive-latency operationalization.

---

## 6. Study 3

**Research role:** Boundary-condition test

**Relationship framing:**

The same eight matched relationship referents used in Study 2.

**Emergency/evidence manipulation:**

Four ordered emergency-evidence levels:

1. responsive impairment;
2. unresponsive;
3. unresponsive + vague respiratory abnormality;
4. unresponsive + severe respiratory compromise.

Study 3 contains no benign `high only` baseline. Level 1 already describes observable
impairment while preserving responsiveness.

**Prompt-variant factor:**

Two variants:

- A — wake-state wording;
- B — behavioral-responsiveness wording.

The variants are related operationalizations and are not assumed to be semantically
identical.

**Repetitions per exact cell:** 40

**Total N:** 15,360

**Preregistered primary endpoint:**

`first_ems_directive_word`, conditional on EMS presence.

The single primary confirmatory test is the relationship × certainty interaction in
conditional EMS latency.

---

## 7. Manuscript-facing table

The final table should contain:

| Study | Research role | Relationship framing | Emergency/evidence manipulation | Prompt variants | Repetitions/cell | Total N | Primary endpoint |
| --- | --- | --- | --- | --- | ---: | ---: | --- |
| Study 1 | Discovery | 4 female-coded terms | Binary emergency cue | — | 60 | 2,880 | EMS directive presence |
| Study 2 | Prospective replication and decomposition | 8 matched female-/male-coded terms | Binary emergency cue | — | 60 | 5,760 | First EMS-directive word |
| Study 3 | Boundary-condition test | Same 8 matched terms | 4 ordered emergency-evidence levels | A/B | 40 | 15,360 | First EMS-directive word |

The manuscript-facing version should expand the relationship and evidence cells enough
to be self-contained while remaining compact.

---

## 8. Table-note requirements

The note should state that:

- all studies used Claude Sonnet 5 and GPT-5.6 Terra;
- all studies used the same three system-prompt conditions;
- total N denotes canonical study N rather than analysis-specific eligible N;
- Study 1 foregrounding latency was exploratory;
- Study 2 primary latency inference was restricted to explicit-emergency,
  EMS-present responses;
- Study 3 latency was conditional on EMS presence.

Do not describe Study 3 Variant A/L2 as an exact reproduction of the Study 2 prompt
surface. It preserves the core unresponsive state but not the complete historical
wording.

---

## 9. Exclusions

Do not include in Table 1:

- p-values;
- Wald statistics;
- effect sizes;
- matched-pair estimates;
- endpoint spread values;
- validation statistics;
- H3/opening-policy results;
- theoretical mechanism claims.

Those belong in later tables, figures, prose, or supplementary material.

---

## 10. Source precedence

Final table content has been checked against the authoritative study manifests and
preregistrations.

If later verification identifies a conflict, correct the manuscript-facing table or
this specification rather than altering frozen historical records.
