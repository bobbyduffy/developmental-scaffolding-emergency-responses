#!/usr/bin/env python3
"""Post-confirmatory diagnostics/reporting already authorized by the frozen Study 3 plan.

Outputs:
- explicit HC3 restriction-covariance rank diagnostic for real H1
- model-stratified adjusted relationship x certainty latency surfaces
- model-stratified matched-pair differences at all certainty levels
- descriptive across-relationship spread by model and certainty

No new inferential hypotheses are introduced.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2

import analyze_results as frozen
import secondary_reporting as sec


DATA = Path("./data")


def h1_rank_diagnostic(primary):
    names = frozen.interaction_names(primary)
    pnames = list(primary.params.index)

    R = np.zeros((len(names), len(pnames)), dtype=float)
    for i, name in enumerate(names):
        R[i, pnames.index(name)] = 1.0

    beta = np.asarray(primary.params, dtype=float)
    cov = np.asarray(primary.cov_params(), dtype=float)
    q = R @ beta
    cov_r = R @ cov @ R.T

    rank = int(np.linalg.matrix_rank(cov_r))
    nominal = len(names)

    stat_rank = float(q @ np.linalg.pinv(cov_r) @ q)
    p_rank = float(chi2.sf(stat_rank, rank)) if rank > 0 else None

    return {
        "nominal_constraints": nominal,
        "covariance_rank": rank,
        "rank_deficient": rank < nominal,
        "design_matrix_rank": int(
            np.linalg.matrix_rank(np.asarray(primary.model.exog, dtype=float))
        ),
        "n_parameters": int(len(beta)),
        "rank_aware_statistic": stat_rank,
        "rank_aware_df": rank,
        "rank_aware_p": p_rank,
        "frozen_joint_wald": frozen.joint_wald(primary, names),
        "coefficient_names": names,
    }


def model_surfaces(lat):
    surface_rows = []
    pair_rows = []

    for model_key, sub in lat.groupby("model_key", sort=True):
        # Frozen-plan model-stratified latency model:
        # relationship*certainty + relationship*variant +
        # certainty*variant + system
        fit = frozen.fit_hc3(sub, sec.BASE_NO_MODEL)

        relationships = sorted(sub["relationship"].dropna().unique())

        for relationship in relationships:
            for certainty in (1, 2, 3, 4):
                v = sec.prediction_vector(fit, relationship, certainty)
                est = sec.vector_estimate(fit, v)

                raw = sub[
                    (sub["relationship"] == relationship)
                    & (sub["certainty"] == certainty)
                ]["first_ems_directive_word"].astype(float)

                surface_rows.append({
                    "model_key": model_key,
                    "relationship": relationship,
                    "certainty": certainty,
                    "n_latency": int(len(raw)),
                    "raw_mean": float(raw.mean()),
                    "raw_median": float(raw.median()),
                    "adjusted_estimate": est["estimate"],
                    "se": est["se"],
                    "ci_low": est["ci_low"],
                    "ci_high": est["ci_high"],
                })

        for row in sec.all_level_pair_differences(fit):
            row = dict(row)
            row["model_key"] = model_key
            pair_rows.append(row)

    return pd.DataFrame(surface_rows), pd.DataFrame(pair_rows)


def spread_summary(surfaces):
    rows = []
    for (model_key, certainty), g in surfaces.groupby(
        ["model_key", "certainty"], sort=True
    ):
        x = g["adjusted_estimate"].astype(float)
        rows.append({
            "model_key": model_key,
            "certainty": int(certainty),
            "min_adjusted_latency": float(x.min()),
            "max_adjusted_latency": float(x.max()),
            "relationship_range_words": float(x.max() - x.min()),
            "sd_across_relationship_estimates": float(x.std(ddof=1)),
        })
    return pd.DataFrame(rows)


def main():
    df = frozen.load_jsonl(DATA / "results.jsonl")
    valid = frozen.valid_rows(df)

    lat = valid[
        (valid["ems_instruction"] == 1)
        & valid["first_ems_directive_word"].notna()
    ].copy()

    primary = frozen.fit_hc3(lat, frozen.PRIMARY_FORMULA)
    rank_diag = h1_rank_diagnostic(primary)

    surfaces, pairs = model_surfaces(lat)
    spreads = spread_summary(surfaces)

    surfaces.to_csv(
        DATA / "model_relationship_certainty_latency_surfaces.csv",
        index=False,
    )
    pairs.to_csv(
        DATA / "model_matched_pair_latency_differences.csv",
        index=False,
    )
    spreads.to_csv(
        DATA / "model_relationship_certainty_spread.csv",
        index=False,
    )

    diagnostic = {
        "status": "post-confirmatory prespecified reporting/diagnostic",
        "confirmatory_checkpoint":
            "a321cbee8fd7a4166152892ef38d6ad4ff38b89c",
        "n_latency": int(len(lat)),
        "H1_rank_diagnostic": rank_diag,
        "surface_weighting":
            "Within each model endpoint, adjusted estimates equally average "
            "over prompt variants and system-prompt design strata.",
    }

    (DATA / "latency_surface_diagnostics.json").write_text(
        json.dumps(diagnostic, indent=2),
        encoding="utf-8",
    )

    print("\n=== REAL H1 RANK DIAGNOSTIC ===")
    print(json.dumps(rank_diag, indent=2))

    print("\n=== ADJUSTED LATENCY SURFACES ===")
    for model_key in sorted(surfaces["model_key"].unique()):
        print(f"\n{model_key}")
        p = surfaces[surfaces["model_key"] == model_key].pivot(
            index="relationship",
            columns="certainty",
            values="adjusted_estimate",
        )
        print(p.round(2).to_string())

    print("\n=== ACROSS-RELATIONSHIP SPREAD ===")
    print(
        spreads[
            ["model_key", "certainty", "relationship_range_words",
             "sd_across_relationship_estimates"]
        ].round(3).to_string(index=False)
    )

    print("\n=== MODEL-SPECIFIC MATCHED-PAIR DIFFERENCES ===")
    for model_key in sorted(pairs["model_key"].unique()):
        print(f"\n{model_key}")
        x = pairs[pairs["model_key"] == model_key][
            ["pair", "certainty", "estimate", "ci_low", "ci_high", "p_raw"]
        ].copy()
        print(x.round(3).to_string(index=False))

    print("\nWrote:")
    print("  data/model_relationship_certainty_latency_surfaces.csv")
    print("  data/model_matched_pair_latency_differences.csv")
    print("  data/model_relationship_certainty_spread.csv")
    print("  data/latency_surface_diagnostics.json")


if __name__ == "__main__":
    main()
