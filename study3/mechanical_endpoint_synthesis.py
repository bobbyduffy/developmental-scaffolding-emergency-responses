#!/usr/bin/env python3
"""Study 3 mechanical-endpoint synthesis.

Post-confirmatory descriptive synthesis only.

Combines, on the same model × relationship × certainty grid:

1. EMS presence, all valid responses;
2. EMS within 10 words, conditional on EMS presence;
3. first EMS-directive word position, conditional on EMS presence.

No new inferential tests are performed.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from patsy import build_design_matrices

import analyze_results as frozen


DATA = Path("data")

PRESENCE_FORMULA = (
    "ems_instruction ~ C(relationship) * C(certainty) "
    "+ C(relationship) * C(prompt_variant) "
    "+ C(certainty) * C(prompt_variant) "
    "+ C(sysprompt_condition)"
)

H4_FORMULA = (
    "ems_within_10_words ~ C(relationship) * C(certainty) "
    "+ C(relationship) * C(prompt_variant) "
    "+ C(certainty) * C(prompt_variant) "
    "+ C(sysprompt_condition)"
)

LATENCY_FORMULA = (
    "first_ems_directive_word ~ C(relationship) * C(certainty) "
    "+ C(relationship) * C(prompt_variant) "
    "+ C(certainty) * C(prompt_variant) "
    "+ C(sysprompt_condition)"
)


def prediction_vector(model, relationship, certainty):
    """Equal-average prediction over variant × system strata."""
    frame = model.model.data.frame

    rows = []

    for variant in sorted(frame["prompt_variant"].dropna().unique()):
        for system in sorted(
            frame["sysprompt_condition"].dropna().unique()
        ):
            rows.append({
                "relationship": relationship,
                "certainty": certainty,
                "prompt_variant": variant,
                "sysprompt_condition": system,
            })

    mat = np.asarray(
        build_design_matrices(
            [frozen._design_info(model)],
            pd.DataFrame(rows),
        )[0],
        dtype=float,
    )

    return mat.mean(axis=0)


def estimate(model, vector):
    beta = np.asarray(model.params, dtype=float)
    return float(vector @ beta)


def build_surface(valid):
    rows = []

    for model_key, all_model in valid.groupby(
        "model_key", sort=True
    ):
        all_model = all_model.copy()

        ems_model = all_model[
            (all_model["ems_instruction"] == 1)
            & all_model["first_ems_directive_word"].notna()
        ].copy()

        h4_model = ems_model[
            ems_model["ems_within_10_words"].notna()
        ].copy()

        presence_fit = frozen.fit_hc3(
            all_model,
            PRESENCE_FORMULA,
        )

        h4_fit = frozen.fit_hc3(
            h4_model,
            H4_FORMULA,
        )

        latency_fit = frozen.fit_hc3(
            ems_model,
            LATENCY_FORMULA,
        )

        relationships = sorted(
            all_model["relationship"].unique()
        )

        for relationship in relationships:
            for certainty in (1, 2, 3, 4):

                all_cell = all_model[
                    (all_model["relationship"] == relationship)
                    & (all_model["certainty"] == certainty)
                ]

                ems_cell = ems_model[
                    (ems_model["relationship"] == relationship)
                    & (ems_model["certainty"] == certainty)
                ]

                h4_cell = h4_model[
                    (h4_model["relationship"] == relationship)
                    & (h4_model["certainty"] == certainty)
                ]

                vp = prediction_vector(
                    presence_fit,
                    relationship,
                    certainty,
                )

                vh = prediction_vector(
                    h4_fit,
                    relationship,
                    certainty,
                )

                vl = prediction_vector(
                    latency_fit,
                    relationship,
                    certainty,
                )

                n_all = int(len(all_cell))
                n_ems = int(len(ems_cell))

                raw_presence = float(
                    all_cell["ems_instruction"].mean()
                )

                raw_within10 = (
                    float(
                        pd.to_numeric(
                            h4_cell["ems_within_10_words"],
                            errors="raise",
                        ).mean()
                    )
                    if len(h4_cell)
                    else None
                )

                raw_latency_mean = (
                    float(
                        pd.to_numeric(
                            ems_cell["first_ems_directive_word"],
                            errors="raise",
                        ).mean()
                    )
                    if len(ems_cell)
                    else None
                )

                raw_latency_median = (
                    float(
                        pd.to_numeric(
                            ems_cell["first_ems_directive_word"],
                            errors="raise",
                        ).median()
                    )
                    if len(ems_cell)
                    else None
                )

                rows.append({
                    "model_key": model_key,
                    "relationship": relationship,
                    "certainty": certainty,

                    "n_all": n_all,
                    "n_ems_present": n_ems,

                    "raw_ems_presence_probability":
                        raw_presence,
                    "adjusted_ems_presence_probability":
                        estimate(presence_fit, vp),

                    "raw_within10_conditional_probability":
                        raw_within10,
                    "adjusted_within10_conditional_probability":
                        estimate(h4_fit, vh),

                    "raw_latency_mean_conditional_words":
                        raw_latency_mean,
                    "raw_latency_median_conditional_words":
                        raw_latency_median,
                    "adjusted_latency_conditional_words":
                        estimate(latency_fit, vl),
                })

    return pd.DataFrame(rows)


def relationship_spreads(surface):
    rows = []

    for (model_key, certainty), g in surface.groupby(
        ["model_key", "certainty"],
        sort=True,
    ):
        presence = g[
            "adjusted_ems_presence_probability"
        ].astype(float)

        within10 = g[
            "adjusted_within10_conditional_probability"
        ].astype(float)

        latency = g[
            "adjusted_latency_conditional_words"
        ].astype(float)

        rows.append({
            "model_key": model_key,
            "certainty": int(certainty),

            "presence_relationship_range_pp":
                float(
                    100 * (presence.max() - presence.min())
                ),

            "within10_relationship_range_pp":
                float(
                    100 * (within10.max() - within10.min())
                ),

            "latency_relationship_range_words":
                float(latency.max() - latency.min()),

            "presence_min_pct":
                float(100 * presence.min()),
            "presence_max_pct":
                float(100 * presence.max()),

            "within10_min_pct":
                float(100 * within10.min()),
            "within10_max_pct":
                float(100 * within10.max()),

            "latency_min_words":
                float(latency.min()),
            "latency_max_words":
                float(latency.max()),
        })

    return pd.DataFrame(rows)


def main():
    df = frozen.load_jsonl(DATA / "results.jsonl")
    valid = frozen.valid_rows(df).copy()

    valid["certainty"] = pd.to_numeric(
        valid["certainty"],
        errors="raise",
    ).astype(int)

    surface = build_surface(valid)
    spreads = relationship_spreads(surface)

    surface.to_csv(
        DATA / "mechanical_endpoint_surface.csv",
        index=False,
    )

    spreads.to_csv(
        DATA / "mechanical_endpoint_relationship_spreads.csv",
        index=False,
    )

    metadata = {
        "status":
            "post-confirmatory descriptive mechanical-endpoint synthesis",

        "n_valid": int(len(valid)),

        "endpoints": {
            "ems_presence": {
                "population":
                    "all valid canonical responses",
                "definition":
                    "explicit EMS directive present",
            },

            "ems_within_10_words": {
                "population":
                    "EMS-present responses",
                "definition":
                    "first clean EMS directive begins at word 10 or earlier",
            },

            "first_ems_directive_word": {
                "population":
                    "EMS-present responses",
                "definition":
                    "1-indexed surface-word position where first clean EMS directive begins",
            },
        },

        "adjustment":
            "Within each model, adjusted estimates equally average "
            "prompt-variant and system-prompt design strata.",

        "inferential_scope":
            "No new statistical tests. This file synthesizes already-defined "
            "mechanical endpoints for descriptive interpretation.",

        "excluded_from_synthesis": {
            "ems_priority_opening":
                "failed prospective human validation",
            "opening_policy":
                "failed prospective human validation",
        },
    }

    (
        DATA / "mechanical_endpoint_synthesis.json"
    ).write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    print("\n=== MECHANICAL-ENDPOINT RELATIONSHIP SPREADS ===")
    print(
        spreads[
            [
                "model_key",
                "certainty",
                "presence_relationship_range_pp",
                "within10_relationship_range_pp",
                "latency_relationship_range_words",
            ]
        ]
        .round(3)
        .to_string(index=False)
    )

    print("\n=== ADJUSTED SURFACES ===")

    for model_key in sorted(surface["model_key"].unique()):

        s = surface[
            surface["model_key"] == model_key
        ]

        print(f"\n{'=' * 72}")
        print(model_key)
        print("=" * 72)

        print("\nEMS PRESENCE (%)")
        print(
            (
                100 * s.pivot(
                    index="relationship",
                    columns="certainty",
                    values="adjusted_ems_presence_probability",
                )
            )
            .round(1)
            .to_string()
        )

        print("\nEMS WITHIN 10 WORDS, CONDITIONAL ON PRESENCE (%)")
        print(
            (
                100 * s.pivot(
                    index="relationship",
                    columns="certainty",
                    values="adjusted_within10_conditional_probability",
                )
            )
            .round(1)
            .to_string()
        )

        print("\nFIRST EMS DIRECTIVE WORD, CONDITIONAL ON PRESENCE")
        print(
            s.pivot(
                index="relationship",
                columns="certainty",
                values="adjusted_latency_conditional_words",
            )
            .round(2)
            .to_string()
        )

    print("\nWrote:")
    print("  data/mechanical_endpoint_surface.csv")
    print("  data/mechanical_endpoint_relationship_spreads.csv")
    print("  data/mechanical_endpoint_synthesis.json")


if __name__ == "__main__":
    main()

