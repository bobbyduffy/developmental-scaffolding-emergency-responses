#!/usr/bin/env python3
"""Prespecified Study 3 EMS-presence sensitivity analysis.

This implementation follows PRESENCE_SENSITIVITY_SPEC.md, which was committed
before these formal sensitivity models were executed.  It does not modify the
frozen confirmatory analysis or promote any post hoc variant/within-Claude
pattern to prespecified inference.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2

import analyze_results as frozen

MODEL_FORMULA = (
    "ems_instruction ~ C(relationship) * C(certainty) * C(model_key) "
    "+ C(relationship) * C(prompt_variant) "
    "+ C(certainty) * C(prompt_variant) "
    "+ C(model_key) * C(prompt_variant) "
    "+ C(sysprompt_condition)"
)

SYSTEM_FORMULA = (
    "ems_instruction ~ C(relationship) * C(certainty) * C(sysprompt_condition) "
    "+ C(relationship) * C(prompt_variant) "
    "+ C(certainty) * C(prompt_variant) "
    "+ C(sysprompt_condition) * C(prompt_variant) "
    "+ C(model_key)"
)


def matching_names(model, required: tuple[str, ...], forbidden: tuple[str, ...] = ()) -> list[str]:
    return [
        name
        for name in model.params.index
        if all(token in name for token in required)
        and not any(token in name for token in forbidden)
    ]


def rank_aware_wald(model, names: list[str]) -> dict:
    """Joint HC3 Wald test with explicit robust-covariance rank reporting.

    The nominal restriction count is kept separate from the effective rank of
    R Cov(beta) R'.  If the robust restriction covariance is rank deficient,
    the generalized-inverse statistic and chi-square p-value use that effective
    rank and the deficiency is reported explicitly rather than hidden.
    """
    if not names:
        return {
            "estimable": False,
            "reason": "no matching coefficients",
            "nominal_constraints": 0,
        }

    pnames = list(model.params.index)
    R = np.zeros((len(names), len(pnames)), dtype=float)
    for i, name in enumerate(names):
        R[i, pnames.index(name)] = 1.0

    beta = np.asarray(model.params, dtype=float)
    cov = np.asarray(model.cov_params(), dtype=float)
    q = R @ beta
    cov_r = R @ cov @ R.T

    rank = int(np.linalg.matrix_rank(cov_r))
    nominal = int(len(names))
    design_rank = int(np.linalg.matrix_rank(np.asarray(model.model.exog, dtype=float)))
    n_params = int(len(beta))

    out = {
        "estimable": rank > 0,
        "nominal_constraints": nominal,
        "covariance_rank": rank,
        "rank_deficient": bool(rank < nominal),
        "design_matrix_rank": design_rank,
        "n_parameters": n_params,
        "coefficient_names": names,
    }

    if rank == 0:
        out["reason"] = "robust restriction covariance has rank 0"
        return out

    stat = float(q @ np.linalg.pinv(cov_r) @ q)
    out.update({
        "statistic": stat,
        "effective_df": rank,
        "p": float(chi2.sf(stat, rank)),
        "max_abs_restriction_estimate": float(np.max(np.abs(q))),
    })
    return out


def presence_summary(df: pd.DataFrame, keys: list[str]) -> list[dict]:
    rows = []
    for vals, grp in df.groupby(keys, sort=True, dropna=False):
        if not isinstance(vals, tuple):
            vals = (vals,)
        n = int(len(grp))
        present = int(grp["ems_instruction"].sum())
        row = {k: v for k, v in zip(keys, vals)}
        row.update({
            "n": n,
            "ems_present": present,
            "ems_absent": n - present,
            "presence_rate": float(present / n) if n else None,
        })
        rows.append(row)
    return rows


def analyze(df: pd.DataFrame) -> dict:
    v = frozen.valid_rows(df)
    v = v.dropna(subset=["ems_instruction"]).copy()
    if not len(v):
        raise RuntimeError("No valid rows with EMS-presence coding")

    v["ems_instruction"] = pd.to_numeric(v["ems_instruction"], errors="raise").astype(float)

    model_fit = frozen.fit_hc3(v, MODEL_FORMULA)
    model_names = matching_names(
        model_fit,
        ("C(relationship)", "C(certainty)", "C(model_key)"),
        ("C(prompt_variant)",),
    )

    system_fit = frozen.fit_hc3(v, SYSTEM_FORMULA)
    system_names = matching_names(
        system_fit,
        ("C(relationship)", "C(certainty)", "C(sysprompt_condition)"),
        ("C(prompt_variant)",),
    )

    return {
        "status": "post-confirmatory prespecified EMS-presence sensitivity analysis",
        "confirmatory_checkpoint": "a321cbee8fd7a4166152892ef38d6ad4ff38b89c",
        "presence_sensitivity_spec_checkpoint": "ccef3450279e98fa944ad312a20e92372441eb15",
        "n_valid": int(len(v)),
        "overall_presence_rate": float(v["ems_instruction"].mean()),
        "formal_tests": {
            "relationship_x_certainty_x_model": rank_aware_wald(model_fit, model_names),
            "relationship_x_certainty_x_system": rank_aware_wald(system_fit, system_names),
        },
        "descriptives": {
            "by_model": presence_summary(v, ["model_key"]),
            "by_certainty": presence_summary(v, ["certainty"]),
            "model_x_relationship_x_certainty": presence_summary(
                v, ["model_key", "relationship", "certainty"]
            ),
            "system_x_relationship_x_certainty": presence_summary(
                v, ["sysprompt_condition", "relationship", "certainty"]
            ),
            "variant_x_relationship_x_certainty": presence_summary(
                v, ["prompt_variant", "relationship", "certainty"]
            ),
            "full_design_cells": presence_summary(
                v,
                [
                    "model_key",
                    "sysprompt_condition",
                    "prompt_variant",
                    "relationship",
                    "certainty",
                ],
            ),
        },
        "interpretive_scope": {
            "formal_variant_presence_test": False,
            "within_claude_formal_interactions": False,
            "note": (
                "Variant-stratified and full-cell presence summaries are descriptive. "
                "No post hoc relationship-by-certainty-by-variant EMS-presence test and "
                "no special within-Claude interaction test are promoted to prespecified inference."
            ),
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--indir", type=Path, default=Path("./data"))
    args = ap.parse_args()

    df = frozen.load_jsonl(args.indir / "results.jsonl")
    results = analyze(df)
    out = args.indir / "presence_sensitivity.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(f"Wrote {out}")
    print("Model sensitivity:")
    print(json.dumps(results["formal_tests"]["relationship_x_certainty_x_model"], indent=2))
    print("System sensitivity:")
    print(json.dumps(results["formal_tests"]["relationship_x_certainty_x_system"], indent=2))
    print("By model:")
    print(json.dumps(results["descriptives"]["by_model"], indent=2))
    print("By certainty:")
    print(json.dumps(results["descriptives"]["by_certainty"], indent=2))


if __name__ == "__main__":
    main()
