#!/usr/bin/env python3
"""Reproduce the Study-2 coder calibration against the completed Study-1 corpus.

Run from test2/ after Study 1 data/human_codes.csv exists one directory above.
This script is audit-only and does not alter Study 1 files.
"""

from __future__ import annotations

import csv
import json
import tempfile
from pathlib import Path

import code_responses as v2

HERE = Path(__file__).resolve().parent
STUDY1 = HERE.parent


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    raw = load_jsonl(STUDY1 / "data" / "full.jsonl")
    old_results = load_jsonl(STUDY1 / "data" / "results.jsonl")
    with open(STUDY1 / "data" / "human_codes.csv", newline="", encoding="utf-8") as fh:
        human = {r["adjudication_id"]: r for r in csv.DictReader(fh)}

    final_old = {}
    human_ids = set(human)
    for row in old_results:
        aid = row.get("adjudication_id")
        if aid and aid in human:
            final_old[row["trial_id"]] = (
                int(human[aid]["ems_instruction"]),
                int(human[aid]["escalation"]),
                "human",
            )
        else:
            final_old[row["trial_id"]] = (
                int(row["ems_instruction"]),
                int(row["escalation"]),
                "auto",
            )

    primary_match = 0
    escalation_match = 0
    human_primary_match = 0
    human_escalation_match = 0
    human_n = 0
    human_23_n = 0
    human_23_match = 0
    human_23_v2positive_n = 0
    human_23_v2positive_match = 0
    review_n = 0

    for rec in raw:
        text = rec.get("response") or ""
        coded = v2.code_response(text)
        if coded["needs_human_review"]:
            review_n += 1

        old_ems, old_esc, source = final_old[rec["trial_id"]]
        new_ems = coded["auto_ems_instruction"]
        new_esc = coded["auto_escalation"]
        primary_match += int(new_ems == old_ems)
        escalation_match += int(new_esc == old_esc)

        if source == "human":
            human_n += 1
            human_primary_match += int(new_ems == old_ems)
            human_escalation_match += int(new_esc == old_esc)
            if old_esc in (2, 3):
                human_23_n += 1
                human_23_match += int(new_esc == old_esc)
                if new_ems == 1:
                    human_23_v2positive_n += 1
                    human_23_v2positive_match += int(new_esc == old_esc)

    n = len(raw)
    print(f"Study 1 rows: {n}")
    print(f"v2 human-review rows: {review_n}")
    print(f"Primary concordance: {primary_match}/{n} = {primary_match/n:.4%}")
    print(f"Escalation concordance: {escalation_match}/{n} = {escalation_match/n:.4%}")
    print(
        f"Human-subset primary concordance: {human_primary_match}/{human_n} "
        f"= {human_primary_match/human_n:.4%}"
    )
    print(
        f"Human 2/3 concordance: {human_23_match}/{human_23_n} "
        f"= {human_23_match/human_23_n:.4%}"
    )
    print(
        f"Human 2/3 concordance where v2 detects EMS: "
        f"{human_23_v2positive_match}/{human_23_v2positive_n} "
        f"= {human_23_v2positive_match/human_23_v2positive_n:.4%}"
    )


if __name__ == "__main__":
    main()
