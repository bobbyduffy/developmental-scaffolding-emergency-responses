# Developmental Scaffolding of Challenging or Emergency Responses

Research repository for experiments on how relationship/developmental cues shape language-model emergency guidance, urgency, readability, and response framing.

> **Status note (added retrospectively after Study 2 collection and confirmatory analysis):** This README reflects the current repository state. It does not alter the frozen preregistrations, collection code, coding rules, analysis code, or pre-collection commits for either study.

## Studies

### Study 1 — completed

`study1/` contains the original four-referent experiment:

- mommy
- mom
- girlfriend
- wife

Design: 2 models × 3 system-prompt conditions × 4 referents × 2 emergency-cue conditions × 60 repetitions = **2,880 responses**.

The Study 1 directory contains the frozen preregistration, collection/coding/analysis code, raw and coded data, blinded adjudication artifacts, synthetic validation data, and software tests. The original file contents and Git history are preserved; the project was reorganized into study directories only after Study 1 collection and analysis.

### Study 2 — completed collection and confirmatory analysis

`study2/` contains the contemporaneous eight-referent extension:

- mommy / daddy
- mom / dad
- girlfriend / boyfriend
- wife / husband

Design: 2 models × 3 system-prompt conditions × 8 referents × 2 emergency-cue conditions × 60 repetitions = **5,760 responses**.

Study 2 was frozen before collection, collected in full, coded with the preregistered Study 2 coder plus one blinded human adjudication, and analyzed with the frozen confirmatory analysis script. Raw data, coded data, confirmatory outputs, and the prespecified daddy-polysemy diagnostic are committed in Git history.

The key provenance sequence is preserved as separate commits:

- freeze Study 2 before collection;
- checkpoint raw Study 2 collection before analysis;
- checkpoint coded Study 2 data before analysis;
- run frozen Study 2 confirmatory analysis before interpretation;
- add the prespecified daddy-polysemy diagnostic.

Exploratory post-confirmatory mechanism probes discussed during interpretation were not committed as part of the frozen Study 2 analysis record.

## Cross-study records

`checkpoints/` contains timestamped research checkpoints written at major boundaries in the project. These are narrative provenance records and are kept separate from the frozen materials for either study.

## Repository layout

```text
.
├── README.md
├── LICENSE
├── checkpoints/
├── study1/
└── study2/
```

See the README inside each study directory for study-specific workflow, provenance, and current status.

No API keys should ever be committed.
