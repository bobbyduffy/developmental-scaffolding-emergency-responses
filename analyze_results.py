#!/usr/bin/env python3
"""
Frozen confirmatory analysis for Developmental Scaffolding of Challenging or
Emergency Responses.

This script is intended to be tested on synthetic/results.jsonl before any real
experimental responses are collected, then run unchanged on data/results.jsonl.
"""

from __future__ import annotations

import argparse
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import chi2
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import confint_proportions_2indep, proportions_ztest

RELATIONSHIP_ORDER = ["mommy", "mom", "girlfriend", "wife"]
ALPHA = 0.05

PRIMARY_FULL = (
    "ems_instruction ~ emergency * C(relationship, Treatment(reference='mommy')) "
    "+ C(model_key) + C(sysprompt_condition)"
)
PRIMARY_REDUCED = (
    "ems_instruction ~ emergency + C(relationship, Treatment(reference='mommy')) "
    "+ C(model_key) + C(sysprompt_condition)"
)
READABILITY_FORMULA = (
    "fk_grade ~ emergency * C(relationship, Treatment(reference='mommy')) "
    "+ C(model_key) + C(sysprompt_condition)"
)


def load_jsonl(path: Path) -> pd.DataFrame:
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return pd.DataFrame(rows)


def validate(df: pd.DataFrame) -> pd.DataFrame:
    required = {
        "trial_id",
        "model_key",
        "sysprompt_condition",
        "relationship",
        "emergency",
        "status",
        "ems_instruction",
        "fk_grade",
    }
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"Missing required columns: {sorted(missing)}")

    unresolved = df[(df["status"] == "ok") & (df["ems_instruction"].isna())]
    if len(unresolved):
        raise SystemExit(
            f"Refusing confirmatory analysis: {len(unresolved)} successful rows "
            "still lack a final EMS code. Complete blinded adjudication first."
        )

    analysis = df[df["status"] == "ok"].copy()
    analysis = analysis[analysis["ems_instruction"].notna()].copy()
    analysis["emergency"] = analysis["emergency"].astype(int)
    analysis["ems_instruction"] = analysis["ems_instruction"].astype(int)
    analysis["relationship"] = pd.Categorical(
        analysis["relationship"], categories=RELATIONSHIP_ORDER, ordered=False
    )
    return analysis


def prop_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["model_key", "sysprompt_condition", "relationship", "emergency"], observed=True)
        .agg(n=("ems_instruction", "size"), ems_rate=("ems_instruction", "mean"), fk_mean=("fk_grade", "mean"))
        .reset_index()
    )


def two_group_test(df: pd.DataFrame, relationship: str | None = None) -> dict:
    sub = df if relationship is None else df[df["relationship"] == relationship]
    e1 = sub[sub["emergency"] == 1]["ems_instruction"]
    e0 = sub[sub["emergency"] == 0]["ems_instruction"]
    c1, n1 = int(e1.sum()), int(e1.size)
    c0, n0 = int(e0.sum()), int(e0.size)
    stat, p = proportions_ztest([c1, c0], [n1, n0])
    diff = c1 / n1 - c0 / n0
    low, high = confint_proportions_2indep(c1, n1, c0, n0, method="newcomb", compare="diff")
    return {
        "relationship": relationship or "ALL",
        "n_emergency": n1,
        "rate_emergency": c1 / n1,
        "n_nonemergency": n0,
        "rate_nonemergency": c0 / n0,
        "difference": diff,
        "ci95_low": low,
        "ci95_high": high,
        "z": float(stat),
        "p_raw": float(p),
    }


def interaction_test(df: pd.DataFrame) -> dict:
    """Logistic LRT, with preregistered HC3 LPM fallback if non-estimable."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            full = smf.glm(PRIMARY_FULL, data=df, family=sm.families.Binomial()).fit()
            reduced = smf.glm(PRIMARY_REDUCED, data=df, family=sm.families.Binomial()).fit()
        lr = 2 * (full.llf - reduced.llf)
        df_diff = int(full.df_model - reduced.df_model)
        p = float(chi2.sf(lr, df_diff))
        return {
            "method": "logistic likelihood-ratio test",
            "statistic": float(lr),
            "df": df_diff,
            "p": p,
            "fallback_used": False,
        }
    except Exception as exc:  # preregistered separation/non-estimation fallback
        lpm = smf.ols(PRIMARY_FULL, data=df).fit(cov_type="HC3")
        interaction_names = [
            name
            for name in lpm.params.index
            if "emergency:C(relationship" in name or "C(relationship" in name and ":emergency" in name
        ]
        if not interaction_names:
            raise RuntimeError("Could not identify interaction terms for LPM fallback") from exc
        restriction = " = 0, ".join(interaction_names) + " = 0"
        test = lpm.wald_test(restriction, scalar=True)
        return {
            "method": "HC3 linear probability model Wald test",
            "statistic": float(test.statistic),
            "df": int(len(interaction_names)),
            "p": float(test.pvalue),
            "fallback_used": True,
            "logistic_failure": f"{type(exc).__name__}: {str(exc)[:300]}",
        }


def readability_analysis(df: pd.DataFrame) -> dict:
    rdf = df[df["fk_grade"].notna()].copy()
    fit = smf.ols(READABILITY_FORMULA, data=rdf).fit(cov_type="HC3")
    interaction_names = [
        name
        for name in fit.params.index
        if "emergency:C(relationship" in name or "C(relationship" in name and ":emergency" in name
    ]
    restriction = " = 0, ".join(interaction_names) + " = 0"
    interaction = fit.wald_test(restriction, scalar=True)
    return {
        "n": int(len(rdf)),
        "interaction_statistic": float(interaction.statistic),
        "interaction_df": int(len(interaction_names)),
        "interaction_p": float(interaction.pvalue),
        "coefficients": {
            name: {
                "estimate": float(fit.params[name]),
                "se_hc3": float(fit.bse[name]),
                "p": float(fit.pvalues[name]),
            }
            for name in fit.params.index
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, default=Path("./data/results.jsonl"))
    ap.add_argument("--outdir", type=Path, default=Path("./analysis"))
    args = ap.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    raw = load_jsonl(args.input)
    df = validate(raw)

    cell = prop_summary(df)
    cell.to_csv(args.outdir / "cell_summary.csv", index=False)

    overall = two_group_test(df)
    planned = [two_group_test(df, rel) for rel in RELATIONSHIP_ORDER]
    _, p_adj, _, _ = multipletests([x["p_raw"] for x in planned], alpha=ALPHA, method="holm")
    for row, adjusted in zip(planned, p_adj):
        row["p_holm"] = float(adjusted)

    interaction = interaction_test(df)
    readability = readability_analysis(df)

    results = {
        "analysis_version": "1.0.0",
        "n_successfully_coded": int(len(df)),
        "alpha": ALPHA,
        "primary": {
            "overall_emergency_effect": overall,
            "emergency_by_relationship_interaction": interaction,
            "within_relationship": planned,
        },
        "secondary_readability": readability,
    }

    (args.outdir / "confirmatory_results.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )

    lines = [
        "# Confirmatory analysis output",
        "",
        f"Coded successful responses analyzed: {len(df)}",
        "",
        "## Primary outcome",
        "",
        f"Overall emergency effect: difference = {overall['difference']:.3f}, "
        f"95% CI [{overall['ci95_low']:.3f}, {overall['ci95_high']:.3f}], "
        f"p = {overall['p_raw']:.6g}.",
        "",
        f"Emergency × relationship interaction: {interaction['method']}, "
        f"p = {interaction['p']:.6g}.",
        "",
        "### Planned within-relationship comparisons",
        "",
        "| Relationship | Emergency rate | Non-emergency rate | Difference | 95% CI | Raw p | Holm p |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in planned:
        lines.append(
            f"| {row['relationship']} | {row['rate_emergency']:.3f} | "
            f"{row['rate_nonemergency']:.3f} | {row['difference']:.3f} | "
            f"[{row['ci95_low']:.3f}, {row['ci95_high']:.3f}] | "
            f"{row['p_raw']:.6g} | {row['p_holm']:.6g} |"
        )
    lines += [
        "",
        "## Secondary readability outcome",
        "",
        f"Emergency × relationship interaction (HC3 OLS): p = "
        f"{readability['interaction_p']:.6g}.",
        "",
        "This file is mechanically generated by analyze_results.py. Interpretive or "
        "exploratory analysis belongs outside the confirmatory output.",
    ]
    (args.outdir / "confirmatory_results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {args.outdir / 'confirmatory_results.json'}")
    print(f"Wrote {args.outdir / 'confirmatory_results.md'}")
    print(f"Wrote {args.outdir / 'cell_summary.csv'}")


if __name__ == "__main__":
    main()
