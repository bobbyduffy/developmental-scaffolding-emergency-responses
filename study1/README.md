# Study 1 — four-referent experiment

**Status: COMPLETED.**

This directory contains the original 2,880-response experiment on emergency guidance and linguistic complexity.

## Design

The experiment crossed:

- 2 models
- 3 system-prompt conditions
- 4 relationship/developmental cues: `mommy`, `mom`, `girlfriend`, `wife`
- 2 emergency-cue conditions
- 60 repetitions per cell

Total: **2,880 responses**.

The scientific specification is in `preregistration.md`.

## Files

- `preregistration.md` — frozen Study 1 plan
- `run_experiment.py` — collection runner
- `code_responses.py` — conservative primary coding, blinded adjudication export, and readability scoring
- `generate_synthetic.py` — fake schema-compatible outcomes used to test analysis before collection
- `analyze_results.py` — preregistered confirmatory analysis
- `output-budget-6000-v1.0.1.patch` — preserved prelaunch provenance artifact
- `data/` — raw data, manifest, coding outputs, blinded adjudication artifacts, and completed human codes
- `synthetic/` — synthetic validation outputs
- `tests/` — Study 1 software tests
- `requirements.txt` — frozen Study 1 dependencies

## Reproducing the Study 1 workflow

Run commands from this directory (`study1/`).

Create an environment and install dependencies:

```text
python -m venv .venv
.venv/Scripts/activate        # Windows
pip install -r requirements.txt
```

Run tests:

```text
python -m unittest discover -s tests
```

Generate fake data and run the confirmatory analysis:

```text
python generate_synthetic.py
python analyze_results.py --input synthetic/results.jsonl --outdir synthetic/analysis
```

The real Study 1 collection is already complete. Its raw data and manifest are preserved in `data/`.

To reproduce coding from the completed data:

```text
python code_responses.py --indir ./data --human-codes ./data/human_codes.csv
```

To reproduce the frozen confirmatory analysis:

```text
python analyze_results.py --input data/results.jsonl --outdir analysis
```

## Provenance note

Study 1 originally occupied the repository root. After Study 1 collection, blinded human coding, and the first analysis checkpoint were completed, the repository was reorganized into `study1/` and `study2/` directories. The frozen Study 1 file contents were moved without modification, so their content hashes remain unchanged. Git history preserves their original pre-collection locations and commits.

No API keys should ever be committed.
