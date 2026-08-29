#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import pandas as pd


DATA = Path("data")
FULL = DATA / "full.jsonl"
SAMPLE = DATA / "h3_opening_validation_sample_blinded.jsonl"
MANIFEST = DATA / "h3_opening_validation_manifest.json"
HUMAN = DATA / "h3_opening_validation_human.csv"

ID_COL = "trial_id"
TEXT_COL = "response"


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_jsonl(path):
    rows = []
    with path.open("r", encoding="utf-8-sig") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def id_order_hash(rows):
    text = "\n".join(str(r["source_id"]) for r in rows)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main():
    if HUMAN.exists():
        h = pd.read_csv(HUMAN, dtype=str)
        if len(h):
            raise RuntimeError(
                f"{HUMAN} already contains {len(h)} human codes. "
                "Refusing to alter the sample."
            )

    sample = read_jsonl(SAMPLE)

    if len(sample) != 256:
        raise RuntimeError(
            f"Expected frozen sample N=256; found {len(sample)}."
        )

    ids_before = [str(r["source_id"]) for r in sample]
    hash_before = id_order_hash(sample)
    wanted = set(ids_before)

    # Collect only nonempty response texts for frozen sampled IDs.
    found = {sid: [] for sid in wanted}

    with FULL.open("r", encoding="utf-8-sig") as f:
        for line in f:
            if not line.strip():
                continue

            row = json.loads(line)
            sid = str(row.get(ID_COL, ""))

            if sid not in wanted:
                continue

            text = row.get(TEXT_COL)

            if text is not None and str(text).strip():
                found[sid].append(str(text))

    lookup = {}

    for sid in ids_before:
        texts = found[sid]

        if not texts:
            raise RuntimeError(
                f"No nonempty response found in {FULL} for {sid}"
            )

        unique = list(dict.fromkeys(texts))

        if len(unique) != 1:
            raise RuntimeError(
                f"{sid} has {len(unique)} distinct nonempty responses "
                f"in {FULL}; refusing ambiguous repair."
            )

        lookup[sid] = unique[0]

    repaired = []

    for row in sample:
        r = dict(row)
        r["response_text"] = lookup[str(row["source_id"])]
        repaired.append(r)

    ids_after = [str(r["source_id"]) for r in repaired]
    hash_after = id_order_hash(repaired)

    if ids_before != ids_after:
        raise RuntimeError("Frozen source-ID order changed.")

    if hash_before != hash_after:
        raise RuntimeError("Frozen source-ID/order hash changed.")

    lengths = pd.Series(
        [len(r["response_text"]) for r in repaired]
    )

    print("\n=== EXPLICIT RESPONSE REPAIR CHECK ===")
    print(f"Source file: {FULL}")
    print(f"ID field: {ID_COL}")
    print(f"Response field: {TEXT_COL}")
    print(f"Frozen sample N: {len(repaired)}")
    print(f"ID/order SHA256: {hash_before}")
    print(f"Median response length: {lengths.median():.1f}")
    print(f"Min response length: {lengths.min()}")
    print(f"Max response length: {lengths.max()}")

    preview = (
        repaired[0]["response_text"]
        .replace("\r", " ")
        .replace("\n", " ")
    )

    print("\nFirst frozen response preview:")
    print("-" * 78)
    print(preview[:1000])
    print("-" * 78)

    print(
        "\nThis will change ONLY response_text in the existing 256-row "
        "blinded sample. Source IDs and coding order remain unchanged."
    )

    confirm = input(
        "\nIf this is genuine model-response prose, type REPAIR: "
    ).strip()

    if confirm != "REPAIR":
        print("\nNo files changed.")
        return

    tmp = SAMPLE.with_suffix(".jsonl.tmp")

    with tmp.open("w", encoding="utf-8", newline="\n") as f:
        for row in repaired:
            f.write(
                json.dumps(row, ensure_ascii=False) + "\n"
            )

    os.replace(tmp, SAMPLE)

    manifest = json.loads(
        MANIFEST.read_text(encoding="utf-8-sig")
    )

    manifest["source_text_column"] = TEXT_COL
    manifest["sample_id_order_sha256"] = hash_after

    manifest["text_field_repair"] = {
        "performed_before_human_coding": True,
        "human_codes_entered_before_repair": 0,
        "sample_size": 256,
        "selected_source_ids_changed": False,
        "coding_order_changed": False,
        "source_file": str(FULL).replace("\\", "/"),
        "source_file_sha256": sha256_file(FULL),
        "source_id_column": ID_COL,
        "response_text_column": TEXT_COL,
        "reason": (
            "Initial audit UI mistakenly displayed a SHA-256-like derived "
            "field. A second heuristic selected opening_feature_starts. "
            "Both attempts were stopped before any human label was entered. "
            "Repository inspection established that complete model prose is "
            "stored explicitly in data/full.jsonl under response."
        ),
    }

    MANIFEST.write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
        newline="\n",
    )

    print("\nRepair complete.")
    print(f"Updated: {SAMPLE}")
    print(f"Updated: {MANIFEST}")
    print(f"Frozen ID/order hash preserved: {hash_after}")


if __name__ == "__main__":
    main()
