# Study 2 — contemporaneous eight-referent extension

**STATUS: COLLECTION COMPLETE / CODING COMPLETE / FROZEN CONFIRMATORY ANALYSIS COMPLETE**

> **Retrospective documentation note:** This README was updated after Study 2 collection and confirmatory analysis to reflect the completed state of the study. The preregistration, collection code, coding rules, analysis code, manifest, and pre-collection freeze commit remain preserved in Git history and are not modified by this status update.

This directory contains the Study 2 extension of the completed Study 1 experiment.

## Design

Eight relationship/developmental referents were randomized contemporaneously:

- mommy / daddy
- mom / dad
- girlfriend / boyfriend
- wife / husband

Each was crossed with:

- emergency cue absent/present;
- 3 experimenter system-prompt conditions;
- 2 models;
- 60 repetitions.

Total: **5,760 trials** (2 models × 3 system prompts × 16 user prompts × 60 reps).

The female- and male-coded referents were collected in the same randomized run so that matched comparisons were not confounded with collection date/model drift.

## Prompt constancy

The inherited system-prompt date was intentionally retained as **August 25, 2026**, matching Study 1. The actual Study 2 collection timestamps are separately recorded in `data/manifest.json` and the raw trial records.

Apart from the added matched referents and necessary pronoun substitution (`she`/`he`), the user-prompt structure and generation settings inherit Study 1.

## Collection and coding status

The real Study 2 collection completed with **5,760/5,760 successful responses**.

The frozen Study 2 coder produced coded results for all 5,760 trials. One genuinely ambiguous response was sent to blinded human adjudication and then incorporated into the final coded dataset according to the preregistered workflow.

Permanent data artifacts are in `data/`, including:

- `manifest.json` — realized design, collection metadata, and frozen-file hashes;
- `full.jsonl` — raw response-level collection;
- `results.jsonl` — final coded response-level dataset;
- `adjudicate_blind.csv` — blinded review packet;
- `adjudication_key.jsonl` — mapping retained separately from blind review;
- `../human_codes.csv` — completed human adjudication record.

## Confirmatory analysis status

The frozen confirmatory analysis was run only after the raw and coded checkpoints had been committed.

Committed confirmatory outputs are in `analysis/`:

- `confirmatory_results.json`
- `confirmatory_results.md`
- `cell_summary.csv`

The prespecified descriptive daddy-polysemy diagnostic is also committed as:

- `analysis/daddy_polysemy.csv`

Exploratory post-confirmatory mechanism probes performed during interpretation were intentionally kept out of the frozen Study 2 analysis record.

## Provenance checkpoints

The key Study 2 commit sequence is:

1. `881fb92` — **Freeze Study 2 before collection**
2. `be9c4c7` — **Checkpoint raw Study 2 collection before analysis**
3. `9a36e2c` — **Checkpoint Study 2 coded data before analysis**
4. `f4db0b0` — **Run frozen Study 2 confirmatory analysis before interpretation**
5. `64a6cf6` — **Add prespecified daddy polysemy diagnostic**

These commits preserve the distinction between prospective specification, raw collection, coding, confirmatory analysis, and later interpretation.

## Study 2 materials

- `preregistration.md` — frozen preregistration and confirmatory/exploratory analysis plan.
- `run_experiment.py` — 5,760-trial eight-referent collector.
- `code_responses.py` — Study 2 coder v2.0.0.
- `CODING_RULES.md` — prospective coding definitions.
- `CODER_CALIBRATION.md` — retrospective Study 1 calibration results used before Study 2 collection.
- `DESIGN_NOTES.md` — pre-freeze design decisions and analysis notes.
- `calibrate_coder_against_study1.py` — reproduces coder calibration using `../study1/data/`.
- `analyze_results.py` — frozen confirmatory analysis script.
- `generate_synthetic.py` — synthetic-data validation.
- `daddy_polysemy_check.py` — prespecified descriptive construct-validity diagnostic.
- `tests/` — coder, runner, and analysis tests.
- `requirements.txt` — Python dependencies.

Study 2 should now be treated as a completed study record. Any new mechanism tests or extensions should be implemented prospectively as a new study rather than by modifying the frozen Study 2 analysis pipeline.
