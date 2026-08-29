#!/usr/bin/env python3
"""Post-freeze recovery helper for Study 3.

This script was added only after the original frozen collection run exhausted
provider credits near completion. It does not alter prompts, model endpoints,
system prompts, generation settings, concurrency, retry policy, or trial order.
It imports the frozen Study 3 runner and re-dispatches only trial IDs for which
`data/full.jsonl` contains no successful (`status == "ok"`) record.

Earlier `status == "missing"` records are deliberately retained. Recovery
successes are appended to the same raw JSONL under the same trial IDs, preserving
an auditable record of the failure and retry.

Commands:
    python recover_missing.py plan
    python recover_missing.py run
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import run_experiment as r

EXPECTED_FREEZE_SHA = "e82fc872ebaf2e52d35f37974d3ef5a7b5b0e92f"
EXPECTED_N = 15360


def read_record_state(path: Path) -> tuple[set[str], dict[str, list[str]], int]:
    ok_ids: set[str] = set()
    statuses: dict[str, list[str]] = defaultdict(list)
    n_lines = 0
    if not path.exists():
        return ok_ids, statuses, n_lines
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            n_lines += 1
            rec = json.loads(line)
            tid = rec["trial_id"]
            status = rec.get("status")
            statuses[tid].append(status)
            if status == "ok":
                ok_ids.add(tid)
    return ok_ids, statuses, n_lines


def load_frozen_design(outdir: Path):
    manifest_path = outdir / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"Missing frozen manifest: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("experiment") != "developmental-scaffolding-emergency-responses-study3":
        raise SystemExit("Manifest is not the Study 3 frozen manifest")
    if manifest.get("intended_n_trials") != EXPECTED_N:
        raise SystemExit(
            f"Unexpected intended_n_trials={manifest.get('intended_n_trials')}; expected {EXPECTED_N}"
        )
    frozen_date = manifest["frozen_current_date"]
    seed = manifest["seed"]
    trials = r.build_trials(frozen_date, seed)
    if len(trials) != EXPECTED_N:
        raise SystemExit(f"Frozen runner rebuilt {len(trials)} trials; expected {EXPECTED_N}")
    return manifest, trials


def recovery_plan(outdir: Path):
    manifest, trials = load_frozen_design(outdir)
    full = outdir / "full.jsonl"
    ok_ids, statuses, n_lines = read_record_state(full)
    design_ids = {t.trial_id for t in trials}
    observed_ids = set(statuses)
    unknown = observed_ids - design_ids
    if unknown:
        raise SystemExit(f"Raw file contains {len(unknown)} trial IDs not in frozen design")

    todo = [t for t in trials if t.trial_id not in ok_ids]
    by_model = Counter(t.model_key for t in todo)
    by_status_pattern = Counter(tuple(statuses.get(t.trial_id, [])) for t in todo)

    print(f"Frozen pre-collection commit: {EXPECTED_FREEZE_SHA}")
    print(f"Manifest trials: {len(trials)}")
    print(f"Raw JSONL lines currently: {n_lines}")
    print(f"Unique recorded trial IDs: {len(observed_ids)}")
    print(f"Unique successful trial IDs: {len(ok_ids)}")
    print(f"Recovery targets (no successful record): {len(todo)}")
    print("Recovery targets by model:")
    for key in sorted(by_model):
        print(f"  {key}: {by_model[key]}")
    if by_status_pattern:
        print("Existing status histories among recovery targets:")
        for pattern, n in by_status_pattern.most_common():
            print(f"  {pattern!r}: {n}")
    return manifest, trials, todo


async def execute_recovery(todo, outdir: Path, abort_after: int) -> None:
    if not todo:
        print("No recovery targets remain.")
        return

    clients = r.make_clients()
    sems = {m.key: asyncio.Semaphore(m.max_concurrency) for m in r.MODELS}
    writer = r.Writer(outdir / "full.jsonl")
    state = {"ok": 0, "missing": 0, "consecutive_permanent": 0}
    state_lock = asyncio.Lock()
    abort_event = asyncio.Event()
    started = time.time()

    async def guarded(trial) -> None:
        if abort_event.is_set():
            return
        await r.run_trial(
            trial,
            clients[trial.provider],
            writer,
            sems[trial.model_key],
            state,
            state_lock,
            abort_event,
            abort_after,
        )
        n = state["ok"] + state["missing"]
        if n and n % 25 == 0:
            rate = n / max(time.time() - started, 1e-9)
            print(
                f"  recovery {n}/{len(todo)} ok={state['ok']} "
                f"missing={state['missing']} ({rate:.2f}/s)",
                flush=True,
            )

    try:
        await asyncio.gather(*(guarded(t) for t in todo))
    finally:
        writer.close()

    if abort_event.is_set():
        print(
            f"ABORTED recovery after {abort_after} consecutive non-retryable errors.",
            file=sys.stderr,
        )
    print(f"Recovery done. ok={state['ok']} missing={state['missing']}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", choices=["plan", "run"])
    ap.add_argument("--outdir", type=Path, default=Path("./data"))
    ap.add_argument("--abort-after", type=int, default=10)
    args = ap.parse_args()

    _manifest, _trials, todo = recovery_plan(args.outdir)
    if args.command == "plan":
        return
    asyncio.run(execute_recovery(todo, args.outdir, args.abort_after))


if __name__ == "__main__":
    main()
