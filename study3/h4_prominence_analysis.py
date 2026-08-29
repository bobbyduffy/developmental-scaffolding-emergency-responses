#!/usr/bin/env python3
"""Study 3 H4 objective-prominence reporting and prespecified sensitivity analysis.

H4 = first clean EMS directive begins at surface-word position <= 10,
conditional on EMS being present.

This is post-confirmatory implementation of analyses already authorized by
the frozen Study 3 analysis plan. It does not modify the frozen H4 result.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from patsy import build_design_matrices
from scipy.stats import chi2

import analyze_results as frozen


DATA = Path("./data")
OUTCOME = "ems_within_10_words"

BASE = (
    f"{OUTCOME} ~ C(relationship) * C(certainty) "
    "+ C(relationship) * C(prompt_variant) "
    "+ C(certainty) * C(prompt_variant) "
    "+ C(model_key) + C(sysprompt_condition)"
)

MODEL_STRAT = (
    f"{OUTCOME} ~ C(relationship) * C(certainty) "
    "+ C(relationship) * C(prompt_variant) "
    "+ C(certainty) * C(prompt_variant) "
    "+ C(sysprompt_condition)"
)

SYSTEM_STRAT = (
    f"{OUTCOME} ~ C(relationship) * C(certainty) "
    "+ C(relationship) * C(prompt_variant) "
    "+ C(certainty) * C(prompt_variant) "
    "+ C(model_key)"
)

VARIANT_STRAT = (
    f"{OUTCOME} ~ C(relationship) * C(certainty) "
    "+ C(model_key) + C(sysprompt_condition)"
)

MODEL_HET = (
    f"{OUTCOME} ~ C(relationship) * C(certainty) * C(model_key) "
    "+ C(relationship) * C(prompt_variant) "
    "+ C(certainty) * C(prompt_variant) "
    "+ C(model_key) * C(prompt_variant) "
    "+ C(sysprompt_condition)"
)

SYSTEM_HET = (
    f"{OUTCOME} ~ C(relationship) * C(certainty) * C(sysprompt_condition) "
    "+ C(relationship) * C(prompt_variant) "
    "+ C(certainty) * C(prompt_variant) "
    "+ C(sysprompt_condition) * C(prompt_variant) "
    "+ C(model_key)"
)


def matching_names(model, required, forbidden=()):
    return [
        name for name in model.params.index
        if all(x in name for x in required)
        and not any(x in name for x in forbidden)
    ]


def rank_wald(model, names):
    if not names:
        return {"estimable": False, "reason": "no matching coefficients"}

    pnames = list(model.params.index)
    R = np.zeros((len(names), len(pnames)))

    for i, name in enumerate(names):
        R[i, pnames.index(name)] = 1.0

    beta = np.asarray(model.params, dtype=float)
    cov = np.asarray(model.cov_params(), dtype=float)

    q = R @ beta
    cov_r = R @ cov @ R.T

    nominal = len(names)
    rank = int(np.linalg.matrix_rank(cov_r))

    out = {
        "estimable": rank > 0,
        "nominal_constraints": nominal,
        "covariance_rank": rank,
        "rank_deficient": rank < nominal,
        "design_matrix_rank": int(
            np.linalg.matrix_rank(np.asarray(model.model.exog, dtype=float))
        ),
        "n_parameters": int(len(beta)),
    }

    if rank == 0:
        out["reason"] = "restriction covariance rank = 0"
        return out

    stat = float(q @ np.linalg.pinv(cov_r) @ q)

    out.update({
        "statistic": stat,
        "effective_df": rank,
        "p": float(chi2.sf(stat, rank)),
    })

    return out


def prediction_vector(model, relationship, certainty):
    frame = model.model.data.frame

    rows = []
    for variant in sorted(frame["prompt_variant"].dropna().unique()):
        for sys in sorted(frame["sysprompt_condition"].dropna().unique()):
            rows.append({
                "relationship": relationship,
                "certainty": certainty,
                "prompt_variant": variant,
                "sysprompt_condition": sys,
            })

    mat = np.asarray(
        build_design_matrices(
            [frozen._design_info(model)],
            pd.DataFrame(rows)
        )[0]
    )

    return mat.mean(axis=0)


def vector_estimate(model, v):
    beta = np.asarray(model.params, dtype=float)
    cov = np.asarray(model.cov_params(), dtype=float)

    estimate = float(v @ beta)
    se = float(np.sqrt(max(float(v @ cov @ v), 0.0)))

    return {
        "adjusted_probability": estimate,
        "se": se,
        "ci_low": estimate - 1.96 * se,
        "ci_high": estimate + 1.96 * se,
    }


def model_surfaces(h4):
    rows = []

    for model_key, sub in h4.groupby("model_key", sort=True):
        fit = frozen.fit_hc3(sub, MODEL_STRAT)

        for relationship in sorted(sub["relationship"].unique()):
            for certainty in (1, 2, 3, 4):

                cell = sub[
                    (sub["relationship"] == relationship)
                    & (sub["certainty"] == certainty)
                ]

                raw_n = len(cell)
                raw_yes = int(cell[OUTCOME].sum())
                raw_rate = float(cell[OUTCOME].mean())

                v = prediction_vector(fit, relationship, certainty)
                est = vector_estimate(fit, v)

                rows.append({
                    "model_key": model_key,
                    "relationship": relationship,
                    "certainty": certainty,
                    "n": int(raw_n),
                    "within_10_yes": raw_yes,
                    "raw_probability": raw_rate,
                    **est,
                })

    return pd.DataFrame(rows)


def spread_table(surfaces):
    rows = []

    for (model_key, certainty), g in surfaces.groupby(
        ["model_key", "certainty"], sort=True
    ):
        x = g["adjusted_probability"].astype(float)

        rows.append({
            "model_key": model_key,
            "certainty": int(certainty),
            "min_adjusted_probability": float(x.min()),
            "max_adjusted_probability": float(x.max()),
            "relationship_range_probability": float(x.max() - x.min()),
            "relationship_range_percentage_points":
                float(100 * (x.max() - x.min())),
            "sd_across_relationship_estimates": float(x.std(ddof=1)),
        })

    return pd.DataFrame(rows)


def stratified_tests(h4):
    out = {"by_model": {}, "by_system": {}, "by_variant": {}}

    for key, sub in h4.groupby("model_key", sort=True):
        fit = frozen.fit_hc3(sub, MODEL_STRAT)
        names = frozen.interaction_names(fit)

        out["by_model"][str(key)] = {
            "n": int(len(sub)),
            "rate": float(sub[OUTCOME].mean()),
            "relationship_x_certainty": rank_wald(fit, names),
        }

    for key, sub in h4.groupby("sysprompt_condition", sort=True):
        fit = frozen.fit_hc3(sub, SYSTEM_STRAT)
        names = frozen.interaction_names(fit)

        out["by_system"][str(key)] = {
            "n": int(len(sub)),
            "rate": float(sub[OUTCOME].mean()),
            "relationship_x_certainty": rank_wald(fit, names),
        }

    for key, sub in h4.groupby("prompt_variant", sort=True):
        fit = frozen.fit_hc3(sub, VARIANT_STRAT)
        names = frozen.interaction_names(fit)

        out["by_variant"][str(key)] = {
            "n": int(len(sub)),
            "rate": float(sub[OUTCOME].mean()),
            "relationship_x_certainty": rank_wald(fit, names),
        }

    return out


def main():
    df = frozen.load_jsonl(DATA / "results.jsonl")
    valid = frozen.valid_rows(df)

    h4 = valid[
        (valid["ems_instruction"] == 1)
        & valid[OUTCOME].notna()
    ].copy()

    h4[OUTCOME] = pd.to_numeric(
        h4[OUTCOME], errors="raise"
    ).astype(float)

    # Refit frozen H4 only for rank/estimability verification.
    pooled = frozen.fit_hc3(h4, BASE)
    pooled_names = frozen.interaction_names(pooled)

    # Prespecified higher-order sensitivity tests.
    mf = frozen.fit_hc3(h4, MODEL_HET)
    model_names = matching_names(
        mf,
        ("C(relationship)", "C(certainty)", "C(model_key)"),
        ("C(prompt_variant)",),
    )

    sf = frozen.fit_hc3(h4, SYSTEM_HET)
    system_names = matching_names(
        sf,
        ("C(relationship)", "C(certainty)", "C(sysprompt_condition)"),
        ("C(prompt_variant)",),
    )

    surfaces = model_surfaces(h4)
    spreads = spread_table(surfaces)
    stratified = stratified_tests(h4)

    surfaces.to_csv(
        DATA / "h4_model_relationship_certainty_surfaces.csv",
        index=False,
    )

    spreads.to_csv(
        DATA / "h4_relationship_spread_by_model.csv",
        index=False,
    )

    results = {
        "status":
            "post-confirmatory prespecified H4 reporting/sensitivity analysis",
        "confirmatory_checkpoint":
            "a321cbee8fd7a4166152892ef38d6ad4ff38b89c",
        "n_h4": int(len(h4)),
        "overall_rate": float(h4[OUTCOME].mean()),
        "frozen_H4_rank_diagnostic":
            rank_wald(pooled, pooled_names),
        "model_heterogeneity":
            rank_wald(mf, model_names),
        "system_heterogeneity":
            rank_wald(sf, system_names),
        "stratified_relationship_x_certainty":
            stratified,
        "adjusted_probability_note":
            "Model-stratified LPM estimates equally average prompt variants "
            "and system-prompt design strata.",
        "interpretive_scope":
            "Higher-order model/system interactions are secondary sensitivity "
            "analyses. Variant-stratified relationship-by-certainty estimates "
            "are reporting/sensitivity results, not a new confirmatory family.",
    }

    (DATA / "h4_prominence_analysis.json").write_text(
        json.dumps(results, indent=2),
        encoding="utf-8",
    )

    print("\n=== H4 FROZEN OMNIBUS RANK CHECK ===")
    print(json.dumps(results["frozen_H4_rank_diagnostic"], indent=2))

    print("\n=== H4 MODEL HETEROGENEITY ===")
    print(json.dumps(results["model_heterogeneity"], indent=2))

    print("\n=== H4 SYSTEM HETEROGENEITY ===")
    print(json.dumps(results["system_heterogeneity"], indent=2))

    print("\n=== H4 STRATIFIED TESTS ===")
    print(json.dumps(stratified, indent=2))

    print("\n=== H4 ADJUSTED PROBABILITY SURFACES ===")
    for model_key in sorted(surfaces["model_key"].unique()):
        print(f"\n{model_key}")

        p = surfaces[
            surfaces["model_key"] == model_key
        ].pivot(
            index="relationship",
            columns="certainty",
            values="adjusted_probability",
        )

        print((100 * p).round(1).to_string())

    print("\n(values above are adjusted percentages within 10 words)")

    print("\n=== H4 ACROSS-RELATIONSHIP SPREAD ===")
    print(
        spreads[
            [
                "model_key",
                "certainty",
                "relationship_range_percentage_points",
                "sd_across_relationship_estimates",
            ]
        ].round(3).to_string(index=False)
    )

    outside = surfaces[
        (surfaces["adjusted_probability"] < 0)
        | (surfaces["adjusted_probability"] > 1)
    ]

    print("\n=== LPM BOUND CHECK ===")
    print(
        f"Adjusted cells outside [0,1]: {len(outside)} / {len(surfaces)}"
    )

    print("\nWrote:")
    print("  data/h4_prominence_analysis.json")
    print("  data/h4_model_relationship_certainty_surfaces.csv")
    print("  data/h4_relationship_spread_by_model.csv")


if __name__ == "__main__":
    main()
