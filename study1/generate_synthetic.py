#!/usr/bin/env python3
"""Generate schema-compatible fake results for testing the frozen analysis only."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

MODELS = ["claude-sonnet-5", "gpt-5.6-terra"]
SYSTEMS = ["none", "minimal", "assistant"]
RELATIONSHIPS = ["mommy", "mom", "girlfriend", "wife"]
N_REPS = 60


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=Path("./synthetic/results.jsonl"))
    ap.add_argument("--seed", type=int, default=91731)
    args = ap.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)

    rows = []
    for model in MODELS:
        for system in SYSTEMS:
            for relationship in RELATIONSHIPS:
                for emergency in (0, 1):
                    for rep in range(N_REPS):
                        # Deliberately neutral fake outcomes: no encoded experimental
                        # effect. These values exist only to exercise the analysis.
                        ems = int(rng.binomial(1, 0.5))
                        fk = float(rng.normal(8.0, 2.0))
                        escalation = int(rng.integers(0, 4))
                        trial_id = f"synthetic|{model}|{system}|{relationship}|e{emergency}|r{rep:02d}"
                        rows.append(
                            {
                                "trial_id": trial_id,
                                "model_key": model,
                                "sysprompt_condition": system,
                                "relationship": relationship,
                                "emergency": emergency,
                                "rep": rep,
                                "status": "ok",
                                "ems_instruction": ems,
                                "escalation": escalation,
                                "fk_grade": round(fk, 3),
                                "needs_human_review": False,
                                "code_source": "synthetic",
                            }
                        )

    with open(args.output, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row) + "\n")
    print(f"Wrote {args.output} ({len(rows)} synthetic rows)")


if __name__ == "__main__":
    main()
