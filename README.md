# Developmental Scaffolding of Challenging or Emergency Responses

Code and preregistration for a two-model experiment on emergency guidance and linguistic complexity.

The experiment crosses:

- 2 models
- 3 system prompt conditions
- 4 relationship/developmental cues
- 2 emergency-cue conditions
- 60 repetitions per cell

Total planned responses: 2,880.

The scientific specification is in [preregistration.md](preregistration.md).

## Files

- `preregistration.md` — frozen study plan
- `run_experiment.py` — collection runner
- `code_responses.py` — conservative primary coding, blinded adjudication export, and readability scoring
- `generate_synthetic.py` — creates fake schema-compatible outcomes for testing analysis before collection
- `analyze_results.py` — preregistered confirmatory analysis
- `tests/test_coding.py` — basic coder/readability checks
- `requirements.txt` — Python dependencies

## Intended workflow

Create an environment and install dependencies:

    python -m venv .venv
    .venv/Scripts/activate        # Windows
    pip install -r requirements.txt

Test the coder:

    python -m unittest discover -s tests

Generate fake data and run the confirmatory analysis before collecting real responses:

    python generate_synthetic.py
    python analyze_results.py --input synthetic/results.jsonl --outdir synthetic/analysis

Check the full planned design without making API calls:

    python run_experiment.py dry-run

Run the technical API probe. The probe uses unrelated text and never exposes an experimental prompt:

    python run_experiment.py probe

Set `OPENAI_API_KEY` and `ANTHROPIC_API_KEY`, then collect:

    python run_experiment.py run

Code responses:

    python code_responses.py --indir ./data

If `adjudicate_blind.csv` contains rows, give only that file and the coding definitions from the preregistration to the human adjudicator. Keep `adjudication_key.jsonl` separate. After the completed blind coding file is returned:

    python code_responses.py --indir ./data --human-codes ./data/human_codes.csv

Then run the frozen confirmatory analysis:

    python analyze_results.py --input data/results.jsonl --outdir analysis

## Before collection

The initial manifest records SHA-256 hashes of the preregistration, collector, coder, confirmatory analysis, synthetic-data generator, and requirements file. If any of those files change after the manifest is created, regenerate the manifest before collecting real data and preserve the change in version control.

No API keys should ever be committed.
