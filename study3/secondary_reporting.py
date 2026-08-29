#!/usr/bin/env python3
"""Prespecified Study 3 secondary/reporting analyses.

This file was added only after the frozen confirmatory output had been committed
at a321cbee8fd7a4166152892ef38d6ad4ff38b89c.  It does not modify or overwrite
`data/confirmatory_analysis.json` and is limited to reporting/sensitivity work
already described in the frozen ANALYSIS_PLAN.md.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from patsy import build_design_matrices
from scipy.stats import norm

import analyze_results as frozen


BASE_NO_MODEL = (
    "first_ems_directive_word ~ C(relationship) * C(certainty) "
    "+ C(relationship) * C(prompt_variant) "
    "+ C(certainty) * C(prompt_variant) "
    "+ C(sysprompt_condition)"
)
BASE_NO_SYSTEM = (
    "first_ems_directive_word ~ C(relationship) * C(certainty) "
    "+ C(relationship) * C(prompt_variant) "
    "+ C(certainty) * C(prompt_variant) "
    "+ C(model_key)"
)
BASE_NO_VARIANT = (
    "first_ems_directive_word ~ C(relationship) * C(certainty) "
    "+ C(model_key) + C(sysprompt_condition)"
)

ORDERED_FORMULA = (
    "first_ems_directive_word ~ C(relationship) * certainty_score "
    "+ C(relationship) * C(prompt_variant) "
    "+ certainty_score * C(prompt_variant) "
    "+ C(model_key) + C(sysprompt_condition)"
)

DECOMP_FORMULA = (
    "first_ems_directive_word ~ C(pair_key) * C(referent_sex) * C(certainty) "
    "+ C(pair_key) * C(referent_sex) * C(prompt_variant) "
    "+ C(certainty) * C(prompt_variant) "
    "+ C(model_key) + C(sysprompt_condition)"
)

MODEL_HET_FORMULA = (
    "first_ems_directive_word ~ C(relationship) * C(certainty) * C(model_key) "
    "+ C(relationship) * C(prompt_variant) "
    "+ C(certainty) * C(prompt_variant) "
    "+ C(model_key) * C(prompt_variant) "
    "+ C(sysprompt_condition)"
)

SYSTEM_HET_FORMULA = (
    "first_ems_directive_word ~ C(relationship) * C(certainty) * C(sysprompt_condition) "
    "+ C(relationship) * C(prompt_variant) "
    "+ C(certainty) * C(prompt_variant) "
    "+ C(sysprompt_condition) * C(prompt_variant) "
    "+ C(model_key)"
)


def joint_wald_matching(model, required: tuple[str, ...], forbidden: tuple[str, ...] = ()) -> dict:
    names = [
        n for n in model.params.index
        if all(x in n for x in required) and not any(x in n for x in forbidden)
    ]
    out = frozen.joint_wald(model, names)
    out["coefficient_count"] = len(names)
    return out


def descriptive_latency(lat: pd.DataFrame) -> list[dict]:
    keys = ["relationship", "certainty"]
    rows = []
    for vals, grp in lat.groupby(keys, sort=True):
        x = grp["first_ems_directive_word"].astype(float)
        q1 = float(x.quantile(0.25))
        q3 = float(x.quantile(0.75))
        rows.append({
            "relationship": vals[0],
            "certainty": int(vals[1]),
            "n": int(len(x)),
            "mean": float(x.mean()),
            "sd": float(x.std(ddof=1)),
            "median": float(x.median()),
            "q1": q1,
            "q3": q3,
            "iqr": q3 - q1,
        })
    return rows


def prediction_vector(model, relationship: str, certainty: int) -> np.ndarray:
    frame = model.model.data.frame
    rows = []
    for variant in sorted(frame["prompt_variant"].dropna().unique()):
        for model_key in sorted(frame["model_key"].dropna().unique()):
            for sys in sorted(frame["sysprompt_condition"].dropna().unique()):
                rows.append({
                    "relationship": relationship,
                    "certainty": certainty,
                    "prompt_variant": variant,
                    "model_key": model_key,
                    "sysprompt_condition": sys,
                })
    mat = np.asarray(build_design_matrices([frozen._design_info(model)], pd.DataFrame(rows))[0])
    return mat.mean(axis=0)


def vector_estimate(model, v: np.ndarray) -> dict:
    beta = model.params.values
    cov = np.asarray(model.cov_params())
    est = float(v @ beta)
    se = float(np.sqrt(max(float(v @ cov @ v), 0.0)))
    z = est / se if se > 0 else np.nan
    p = float(2 * norm.sf(abs(z))) if np.isfinite(z) else None
    return {
        "estimate": est,
        "se": se,
        "ci_low": est - 1.96 * se,
        "ci_high": est + 1.96 * se,
        "p_raw": p,
    }


def all_level_pair_differences(primary) -> list[dict]:
    out = []
    for female, male in frozen.PAIRS:
        for certainty in (1, 2, 3, 4):
            vf = prediction_vector(primary, female, certainty)
            vm = prediction_vector(primary, male, certainty)
            stats = vector_estimate(primary, vm - vf)
            stats.update({
                "pair": f"{male}-{female}",
                "certainty": certainty,
                "contrast": "male-coded minus female-coded latency",
            })
            out.append(stats)
    return out


def stratified_tests(lat: pd.DataFrame) -> dict:
    out: dict[str, dict] = {"by_model": {}, "by_system": {}, "by_variant": {}}

    for model_key, sub in lat.groupby("model_key", sort=True):
        m = frozen.fit_hc3(sub, BASE_NO_MODEL)
        out["by_model"][str(model_key)] = {
            "n": int(len(sub)),
            "relationship_x_certainty": frozen.joint_wald(m, frozen.interaction_names(m)),
        }

    for sys, sub in lat.groupby("sysprompt_condition", sort=True):
        m = frozen.fit_hc3(sub, BASE_NO_SYSTEM)
        out["by_system"][str(sys)] = {
            "n": int(len(sub)),
            "relationship_x_certainty": frozen.joint_wald(m, frozen.interaction_names(m)),
        }

    for variant, sub in lat.groupby("prompt_variant", sort=True):
        m = frozen.fit_hc3(sub, BASE_NO_VARIANT)
        out["by_variant"][str(variant)] = {
            "n": int(len(sub)),
            "relationship_x_certainty": frozen.joint_wald(m, frozen.interaction_names(m)),
        }

    return out


def adjusted_relationship_certainty(primary) -> list[dict]:
    out = []
    for relationship in sorted(primary.model.data.frame["relationship"].dropna().unique()):
        for certainty in (1, 2, 3, 4):
            v = prediction_vector(primary, relationship, certainty)
            stats = vector_estimate(primary, v)
            stats.update({"relationship": relationship, "certainty": certainty})
            out.append(stats)
    return out


def opening_policy_description(v: pd.DataFrame) -> list[dict]:
    keys = ["relationship", "certainty", "opening_policy"]
    counts = (
        v.groupby(keys, dropna=False).size().rename("n").reset_index()
    )
    totals = (
        v.groupby(["relationship", "certainty"], dropna=False).size().rename("total").reset_index()
    )
    merged = counts.merge(totals, on=["relationship", "certainty"], how="left")
    merged["proportion"] = merged["n"] / merged["total"]
    return merged.to_dict(orient="records")


def analyze(df: pd.DataFrame) -> dict:
    v = frozen.valid_rows(df)
    lat = v[(v["ems_instruction"] == 1) & v["first_ems_directive_word"].notna()].copy()
    if len(lat) == 0:
        raise RuntimeError("No EMS-present latency rows")

    primary = frozen.fit_hc3(lat, frozen.PRIMARY_FORMULA)
    results: dict = {
        "status": "post-confirmatory prespecified secondary/reporting analyses",
        "confirmatory_checkpoint": "a321cbee8fd7a4166152892ef38d6ad4ff38b89c",
        "n_valid": int(len(v)),
        "n_latency": int(len(lat)),
        "latency_relationship_certainty_descriptives": descriptive_latency(lat),
        "adjusted_relationship_certainty_estimates": adjusted_relationship_certainty(primary),
        "matched_pair_differences_all_certainty_levels": all_level_pair_differences(primary),
        "opening_policy_relationship_certainty": opening_policy_description(v),
    }

    ordered = lat.copy()
    ordered["certainty_score"] = ordered["certainty"].astype(float) - 1.0
    om = frozen.fit_hc3(ordered, ORDERED_FORMULA)
    results["ordered_certainty_trend"] = {
        "relationship_x_ordered_certainty": joint_wald_matching(
            om, ("C(relationship)", "certainty_score"), ("C(prompt_variant)",)
        )
    }

    decomp = frozen.fit_hc3(lat, DECOMP_FORMULA)
    results["role_sex_decomposition"] = {
        "pair_key_x_referent_sex_x_certainty": joint_wald_matching(
            decomp, ("C(pair_key)", "C(referent_sex)", "C(certainty)"), ("C(prompt_variant)",)
        ),
        "referent_sex_x_certainty": joint_wald_matching(
            decomp, ("C(referent_sex)", "C(certainty)"), ("C(pair_key)", "C(prompt_variant)")
        ),
    }

    results["stratified_relationship_x_certainty"] = stratified_tests(lat)

    mm = frozen.fit_hc3(lat, MODEL_HET_FORMULA)
    results["model_heterogeneity"] = {
        "relationship_x_certainty_x_model": joint_wald_matching(
            mm, ("C(relationship)", "C(certainty)", "C(model_key)"), ("C(prompt_variant)",)
        )
    }

    sm = frozen.fit_hc3(lat, SYSTEM_HET_FORMULA)
    results["system_heterogeneity"] = {
        "relationship_x_certainty_x_system": joint_wald_matching(
            sm, ("C(relationship)", "C(certainty)", "C(sysprompt_condition)"), ("C(prompt_variant)",)
        )
    }

    return results


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--indir", type=Path, default=Path("./data"))
    args = ap.parse_args()

    df = frozen.load_jsonl(args.indir / "results.jsonl")
    results = analyze(df)
    out = args.indir / "secondary_reporting.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote {out}")
    print("Ordered trend:", results["ordered_certainty_trend"])
    print("Model heterogeneity:", results["model_heterogeneity"])
    print("System heterogeneity:", results["system_heterogeneity"])
    print("Stratified tests:", json.dumps(results["stratified_relationship_x_certainty"], indent=2))


if __name__ == "__main__":
    main()
