# Developmental Scaffolding of Challenging or Emergency Responses

Research repository for a three-study experimental program on how relationship/developmental cues shape language-model emergency guidance, EMS foregrounding, and response policy under varying levels of emergency evidence.

## Project status

**Experimental phase complete. Manuscript construction in progress.**

Data collection, coding, planned confirmatory analysis, prespecified secondary/sensitivity analysis, and the Study 3 validation work are complete. The empirical analysis state is frozen for manuscript drafting.

The manuscript currently in construction is:

> **Relationship Framing and Emergency Evidence in Language-Model Responses: Three Studies of EMS Foregrounding**

The main-text figure architecture has been frozen, rendered, and verified. Tables are the current construction phase, after which manuscript prose will be drafted from the frozen reporting architecture.

This README describes the current repository state. It does not alter the frozen preregistrations, collection code, coding rules, analysis plans, analysis code, validation specifications, or historical checkpoints preserved in Git history.

## Studies

### Study 1 — discovery

`study1/` contains the original four-referent experiment:

- mommy
- mom
- girlfriend
- wife

Design: 2 models × 3 system-prompt conditions × 4 referents × 2 emergency-cue conditions × 60 repetitions = **2,880 responses**.

Study 1 established the initial experimental setting. EMS inclusion was the preregistered primary outcome. Exploratory post-confirmatory analysis identified differences in EMS foregrounding latency under explicit unresponsiveness, motivating the prospectively specified Study 2 latency endpoint.

The Study 1 directory preserves the frozen preregistration, collection/coding/analysis code, raw and coded data, blinded adjudication artifacts, synthetic validation data, software tests, and historical provenance.

### Study 2 — prospective replication and decomposition

`study2/` contains the contemporaneous eight-referent extension:

- mommy / daddy
- mom / dad
- girlfriend / boyfriend
- wife / husband

Design: 2 models × 3 system-prompt conditions × 8 referents × 2 emergency-cue conditions × 60 repetitions = **5,760 responses**.

Study 2 prospectively tested EMS foregrounding latency and decomposed the original relationship manipulation using matched female-coded and male-coded relational roles. Collection, coding, confirmatory analysis, and prespecified diagnostics are complete and preserved in the repository.

The key provenance sequence remains visible in Git history:

- freeze Study 2 before collection;
- checkpoint raw Study 2 collection before analysis;
- checkpoint coded Study 2 data before analysis;
- run frozen Study 2 confirmatory analysis before interpretation;
- add the prespecified daddy-polysemy diagnostic.

Exploratory post-confirmatory mechanism probes discussed during interpretation were not committed as part of the frozen Study 2 analysis record.

### Study 3 — boundary-condition test

`study3/` contains the preregistered emergency-evidence study.

Design: 2 models × 3 system-prompt conditions × 8 relationship referents × 4 emergency-evidence/certainty levels × 2 prompt variants × 40 repetitions = **15,360 canonical responses** across 384 cells.

Study 3 tests whether relationship-conditioned emergency-response differences contract as supplied medical evidence becomes increasingly decisive. Its primary manuscript-facing endpoints are mechanically defined measures of:

1. EMS presence;
2. first EMS-directive word position, conditional on EMS presence;
3. EMS appearance within the first 10 words, conditional on EMS presence.

Collection and planned analysis are complete and frozen. The directory preserves preregistration and analysis-plan materials, collection/coding/analysis code, raw and coded data, confirmatory outputs, prespecified secondary and sensitivity analyses, mechanical-endpoint synthesis, validation records, deviations, and the final manuscript-facing results map.

Two automated discourse-level measures failed prospective human validation. Their frozen outputs remain preserved for provenance, but they are not used for substantive manuscript interpretation.

The authoritative manuscript-facing Study 3 interpretation is recorded in:

- `study3/STUDY3_RESULTS_MAP.md`
- `checkpoints/2026-08-29_Study3_Analysis_Freeze_PreDraft.md`

## Manuscript construction

`manuscript/` contains the reporting architecture for the empirical paper.

Current main-text figure status:

- Figure 1 — three-study design progression: **rendered and verified**
- Figure 2 — Study 2 matched-role latency contrasts: **rendered and verified**
- Figure 3 — Study 3 relationship × emergency-evidence latency surfaces: **rendered and verified**
- Figure 4 — Study 3 mechanical-endpoint relationship-spread bars: **rendered and verified**

Planned main-text tables:

- Table 1 — three-study design and sample overview
- Table 2 — main inferential results
- Table 3 — human validation audit and disposition

The manuscript is being constructed from frozen study records rather than by reopening exploratory analysis during drafting.

## Cross-study records and provenance

`checkpoints/` contains timestamped records written at major research boundaries. These are narrative provenance documents and do not replace the frozen study-specific preregistrations, plans, code, or outputs.

The repository deliberately preserves distinctions among:

- preregistered confirmatory analysis;
- prespecified secondary/sensitivity analysis;
- post-confirmatory descriptive synthesis;
- prospective/post-confirmatory validation;
- historical deviations and recovery records.

No post-freeze analysis should be represented retrospectively as confirmatory.

## Repository layout

```text
.
├── README.md
├── LICENSE
├── checkpoints/
├── manuscript/
│   ├── FIGURE_TABLE_MANIFEST.md
│   └── figures/
├── study1/
├── study2/
└── study3/
```

See the README and frozen records inside each study directory for study-specific workflow, provenance, and analysis details.

official website https://bochesterton.com/
