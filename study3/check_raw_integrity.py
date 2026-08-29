#!/usr/bin/env python3
"""Metadata-only raw integrity check for completed Study 3 collection.

This script intentionally does not print or inspect substantive response text.
It verifies that every frozen trial has exactly one successful record, allows
retained earlier missing records from documented recovery, checks factor balance
on canonical successful records, and writes a hash-bearing integrity report.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import run_experiment as r

EXPECTED_FREEZE_SHA = "e82fc872ebaf2e52d35f37974d3ef5a7b5b0e92f"
EXPECTED_N = 15360
EXPECTED_RECOVERY_MISSING = 315


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    outdir = Path("./data")
    manifest_path = outdir / "manifest.json"
    raw_path = outdir / "full.jsonl"
    if not manifest_path.exists() or not raw_path.exists():
        raise SystemExit("Expected data/manifest.json and data/full.jsonl")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    trials = r.build_trials(manifest["frozen_current_date"], manifest["seed"])
    design = {t.trial_id: t for t in trials}
    if len(design) != EXPECTED_N:
        raise SystemExit(f"Frozen design rebuilt {len(design)} trials; expected {EXPECTED_N}")

    by_id: dict[str, list[dict]] = defaultdict(list)
    n_lines = 0
    status_counts = Counter()
    with open(raw_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            n_lines += 1
            rec = json.loads(line)
            tid = rec.get("trial_id")
            if tid is None:
                raise SystemExit(f"Line {n_lines} lacks trial_id")
            by_id[tid].append(rec)
            status_counts[rec.get("status")] += 1

    unknown_ids = sorted(set(by_id) - set(design))
    absent_ids = sorted(set(design) - set(by_id))

    canonical: dict[str, dict] = {}
    duplicate_ok_ids = []
    no_ok_ids = []
    recovery_ids = []
    unexpected_histories = []

    for tid in sorted(design):
        recs = by_id.get(tid, [])
        oks = [x for x in recs if x.get("status") == "ok"]
        misses = [x for x in recs if x.get("status") == "missing"]
        if len(oks) == 0:
            no_ok_ids.append(tid)
            continue
        if len(oks) > 1:
            duplicate_ok_ids.append(tid)
            continue
        canonical[tid] = oks[0]
        history = tuple(x.get("status") for x in recs)
        if misses:
            recovery_ids.append(tid)
            if len(misses) != 1 or len(recs) != 2 or history != ("missing", "ok"):
                unexpected_histories.append({"trial_id": tid, "history": history})
        elif len(recs) != 1 or history != ("ok",):
            unexpected_histories.append({"trial_id": tid, "history": history})

    # Metadata consistency: canonical raw fields must agree with the frozen design.
    mismatches = []
    for tid, rec in canonical.items():
        t = design[tid]
        expected = {
            "order_index": t.order_index,
            "model_key": t.model_key,
            "api_model": t.api_model,
            "sysprompt_condition": t.sysprompt_condition,
            "prompt_id": t.prompt_id,
            "relationship": t.relationship,
            "referent_sex": t.referent_sex,
            "pair_key": t.pair_key,
            "prompt_variant": t.prompt_variant,
            "certainty": t.certainty,
            "certainty_label": t.certainty_label,
            "rep": t.rep,
            "user_prompt": t.user_prompt,
            "system_prompt": t.system_prompt,
        }
        bad = {k: {"expected": v, "observed": rec.get(k)} for k, v in expected.items() if rec.get(k) != v}
        if bad:
            mismatches.append({"trial_id": tid, "fields": bad})

    # Canonical quality flags without printing response text.
    empty_ok = [tid for tid, rec in canonical.items() if rec.get("empty_response") is True or not str(rec.get("response") or "").strip()]
    truncated_ok = [tid for tid, rec in canonical.items() if rec.get("truncated") is True]

    cell_counts = Counter()
    for tid, rec in canonical.items():
        cell_counts[(
            rec.get("model_key"),
            rec.get("sysprompt_condition"),
            rec.get("relationship"),
            rec.get("prompt_variant"),
            rec.get("certainty"),
        )] += 1
    expected_cells = 2 * 3 * 8 * 2 * 4
    bad_cell_counts = {str(k): v for k, v in cell_counts.items() if v != 40}

    checks = {
        "manifest_intended_n_trials": manifest.get("intended_n_trials") == EXPECTED_N,
        "design_n_trials": len(design) == EXPECTED_N,
        "unique_recorded_ids": len(by_id) == EXPECTED_N,
        "unique_successful_ids": len(canonical) == EXPECTED_N,
        "no_unknown_ids": len(unknown_ids) == 0,
        "no_absent_ids": len(absent_ids) == 0,
        "no_duplicate_ok_ids": len(duplicate_ok_ids) == 0,
        "no_ids_without_ok": len(no_ok_ids) == 0,
        "recovery_count_expected": len(recovery_ids) == EXPECTED_RECOVERY_MISSING,
        "recovery_histories_clean": len(unexpected_histories) == 0,
        "canonical_metadata_matches_frozen_design": len(mismatches) == 0,
        "no_empty_successes": len(empty_ok) == 0,
        "no_truncated_successes": len(truncated_ok) == 0,
        "canonical_cell_count": len(cell_counts) == expected_cells,
        "canonical_cells_balanced_40_each": len(bad_cell_counts) == 0,
    }

    report = {
        "pre_collection_freeze_sha": EXPECTED_FREEZE_SHA,
        "raw_sha256": sha256_file(raw_path),
        "manifest_sha256": sha256_file(manifest_path),
        "raw_jsonl_lines": n_lines,
        "status_counts": dict(status_counts),
        "unique_recorded_trial_ids": len(by_id),
        "unique_successful_trial_ids": len(canonical),
        "recovered_trial_ids": len(recovery_ids),
        "canonical_cells": len(cell_counts),
        "canonical_cell_min_n": min(cell_counts.values()) if cell_counts else None,
        "canonical_cell_max_n": max(cell_counts.values()) if cell_counts else None,
        "empty_successes": len(empty_ok),
        "truncated_successes": len(truncated_ok),
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "failure_counts": {
            "unknown_ids": len(unknown_ids),
            "absent_ids": len(absent_ids),
            "duplicate_ok_ids": len(duplicate_ok_ids),
            "ids_without_ok": len(no_ok_ids),
            "unexpected_histories": len(unexpected_histories),
            "metadata_mismatches": len(mismatches),
            "bad_cell_counts": len(bad_cell_counts),
        },
    }

    report_path = outdir / "raw_integrity.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Raw JSONL lines: {n_lines}")
    print(f"Statuses: {dict(status_counts)}")
    print(f"Unique recorded IDs: {len(by_id)}")
    print(f"Unique successful IDs: {len(canonical)}")
    print(f"Recovered IDs: {len(recovery_ids)}")
    print(f"Canonical cells: {len(cell_counts)}; min/max n = {min(cell_counts.values())}/{max(cell_counts.values())}")
    print(f"Empty successful responses: {len(empty_ok)}")
    print(f"Truncated successful responses: {len(truncated_ok)}")
    print(f"Raw SHA256: {report['raw_sha256']}")
    print(f"Wrote {report_path}")
    print("ALL CHECKS PASS" if report["all_checks_pass"] else "INTEGRITY CHECK FAILED")

    if not report["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
