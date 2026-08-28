# Developmental Scaffolding of Challenging or Emergency Responses

Research repository for experiments on how relationship/developmental cues shape language-model emergency guidance, urgency, readability, and response framing.

## Studies

### Study 1 — completed

`study1/` contains the original four-referent experiment:

- mommy
- mom
- girlfriend
- wife

Design: 2 models × 3 system-prompt conditions × 4 referents × 2 emergency-cue conditions × 60 repetitions = **2,880 responses**.

The Study 1 directory contains the frozen preregistration, collection/coding/analysis code, raw and coded data, blinded adjudication artifacts, synthetic validation data, and software tests. The original file contents and Git history are preserved; the project was reorganized into study directories only after Study 1 collection and analysis.

### Study 2 — pre-collection

`study2/` contains the contemporaneous eight-referent extension:

- mommy / daddy
- mom / dad
- girlfriend / boyfriend
- wife / husband

Planned design: 2 models × 3 system-prompt conditions × 8 referents × 2 emergency-cue conditions × 60 repetitions = **5,760 responses**.

Study 2 is under construction and must not be collected until its preregistration, analysis code, synthetic checks, manifest, and freeze commit are complete.

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

See the README inside each study directory for study-specific workflow and status.

No API keys should ever be committed.
