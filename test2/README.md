# Test 2 — contemporaneous eight-referent extension

**STATUS: BUILDING / NOT YET FROZEN / DO NOT START REAL COLLECTION YET**

This folder is the Study 2 extension of the completed Study 1 experiment.

## Planned design

Eight relationship/developmental referents are randomized contemporaneously:

- mommy / daddy
- mom / dad
- girlfriend / boyfriend
- wife / husband

Each is crossed with:

- emergency cue absent/present;
- 3 experimenter system-prompt conditions;
- 2 models;
- 60 repetitions.

Total: **5,760 trials** (2 models × 3 system prompts × 16 user prompts × 60 reps).

The female and male referents are collected in the same randomized run so that matched comparisons are not confounded with collection date/model drift.

## Prompt constancy

The inherited system-prompt date is intentionally retained as **August 25, 2026**, matching Study 1. The actual Study 2 collection timestamp is separately recorded in `manifest.json` / each raw trial.

Apart from the added matched referents and necessary pronoun substitution (`she`/`he`), the user-prompt structure and generation settings inherit Study 1.

## Current contents

- `run_experiment.py` — 5,760-trial eight-referent collector; dry-run tested.
- `code_responses.py` — tightened coder v2.0.0.
- `CODING_RULES.md` — explicit prospective coding definitions.
- `CODER_CALIBRATION.md` — retrospective Study 1 calibration results.
- `tests/` — coder and runner tests.
- `requirements.txt` — inherited dependencies.
- `data/` — intentionally empty before collection.

## Before real collection

Still required before `run`:

1. finalize `preregistration.md`;
2. finalize the Study 2 confirmatory/exploratory analysis plan;
3. create/adapt `analyze_results.py` and synthetic-data checks;
4. run the full test suite;
5. run `dry-run` and inspect all resolved prompts;
6. run API `probe` only with unrelated text;
7. create the real Study 2 manifest and verify hashes;
8. commit the frozen Study 2 files before inspecting any Study 2 response.

Do not use the temporary dry-run manifest created during development as the real Study 2 manifest.
