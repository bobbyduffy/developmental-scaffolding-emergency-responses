#!/usr/bin/env python3
"""Frozen Study 2 confirmatory analysis.

Usage:
    python analyze_results.py --input data/results.jsonl --outdir analysis

The primary confirmatory analysis is restricted to explicit-emergency responses
with a final positive EMS instruction and a nonmissing first EMS-directive word.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests

REL_ORDER = ["mommy", "daddy", "mom", "dad", "girlfriend", "boyfriend", "wife", "husband"]
PAIR_CONTRASTS = [("daddy", "mommy"), ("dad", "mom"), ("boyfriend", "girlfriend"), ("husband", "wife")]
ACCESSIBILITY = ["surface_word_count", "fk_grade", "flesch_reading_ease", "words_per_sentence", "syllables_per_word"]
REGISTER = ["mentions_adult", "mentions_trusted_adult", "mentions_neighbor", "mentions_naloxone_or_narcan", "mentions_recovery_position", "mentions_opioid", "mentions_poison_control"]
PROMINENCE = ["first_ems_directive_prop", "first_911_word", "first_911_prop", "first_emergency_cue_word", "first_emergency_cue_prop"]


def load_jsonl(path: Path) -> pd.DataFrame:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return pd.DataFrame(rows)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "status" in out:
        out = out[out["status"].eq("ok")]
    if "empty_response" in out:
        out = out[~out["empty_response"].fillna(False)]
    if "truncated" in out:
        out = out[~out["truncated"].fillna(False)]
    if "needs_human_review" in out:
        out = out[~out["needs_human_review"].fillna(False)]
    out["relationship"] = pd.Categorical(out["relationship"], categories=REL_ORDER, ordered=True)
    out["referent_sex"] = pd.Categorical(out["referent_sex"], categories=["female", "male"], ordered=True)
    out["pair_key"] = pd.Categorical(out["pair_key"], categories=["parent_childlike", "parent_plain", "partner_unmarried", "partner_married"], ordered=True)
    out["emergency"] = pd.to_numeric(out["emergency"], errors="coerce")
    return out


def wald_terms(model, prefixes: list[str]) -> dict:
    names = list(model.params.index)
    idx = [i for i, n in enumerate(names) if any(n.startswith(p) for p in prefixes)]
    if not idx:
        return {"stat": None, "df": 0, "p": None}
    R = np.zeros((len(idx), len(names)))
    for r, i in enumerate(idx):
        R[r, i] = 1.0
    wt = model.wald_test(R, scalar=True)
    return {"stat": float(wt.statistic), "df": len(idx), "p": float(wt.pvalue)}


def fit_ols(df: pd.DataFrame, outcome: str, formula_rhs: str):
    d = df.dropna(subset=[outcome]).copy()
    if len(d) == 0:
        return None, d
    if pd.api.types.is_bool_dtype(d[outcome]):
        d[outcome] = d[outcome].astype(int)
    else:
        d[outcome] = pd.to_numeric(d[outcome], errors="coerce")
        d = d.dropna(subset=[outcome])
    if len(d) == 0:
        return None, d
    model = smf.ols(f"{outcome} ~ {formula_rhs}", data=d).fit(cov_type="HC3")
    return model, d


def relationship_omnibus(model) -> dict:
    return wald_terms(model, ["C(relationship)[T."])


def interaction_omnibus(model, left: str, right: str) -> dict:
    names = list(model.params.index)
    idx = [i for i, n in enumerate(names) if left in n and right in n and ":" in n]
    if not idx:
        return {"stat": None, "df": 0, "p": None}
    R = np.zeros((len(idx), len(names)))
    for r, i in enumerate(idx):
        R[r, i] = 1.0
    wt = model.wald_test(R, scalar=True)
    return {"stat": float(wt.statistic), "df": len(idx), "p": float(wt.pvalue)}


def design_row(model, relationship: str, model_key: str, sysprompt: str) -> np.ndarray:
    import patsy
    frame = pd.DataFrame({"relationship": pd.Categorical([relationship], categories=REL_ORDER, ordered=True), "model_key": [model_key], "sysprompt_condition": [sysprompt]})
    X = patsy.build_design_matrices([model.model.data.design_info], frame, return_type="dataframe")[0]
    return np.asarray(X.iloc[0], dtype=float)


def average_pair_contrast(model, data: pd.DataFrame, male_term: str, female_term: str) -> dict:
    combos = data[["model_key", "sysprompt_condition"]].drop_duplicates().sort_values(["model_key", "sysprompt_condition"])
    vecs = []
    for _, r in combos.iterrows():
        xm = design_row(model, male_term, r["model_key"], r["sysprompt_condition"])
        xf = design_row(model, female_term, r["model_key"], r["sysprompt_condition"])
        vecs.append(xm - xf)
    c = np.mean(vecs, axis=0)
    est = float(c @ np.asarray(model.params))
    cov = np.asarray(model.cov_params())
    se = float(np.sqrt(c @ cov @ c))
    z = est / se if se > 0 else np.nan
    from scipy.stats import norm
    p = float(2 * norm.sf(abs(z))) if np.isfinite(z) else np.nan
    lo, hi = est - 1.96 * se, est + 1.96 * se
    return {"male_term": male_term, "female_term": female_term, "estimate": est, "se": se, "ci95": [lo, hi], "p": p}


def summarize_by_relationship(df: pd.DataFrame, outcome: str) -> list[dict]:
    rows = []
    for rel in REL_ORDER:
        x = pd.to_numeric(df.loc[df["relationship"].eq(rel), outcome], errors="coerce").dropna()
        rows.append({"relationship": rel, "n": int(x.size), "mean": float(x.mean()) if x.size else None, "sd": float(x.std(ddof=1)) if x.size > 1 else None, "median": float(x.median()) if x.size else None})
    return rows


def constant_binary_summary(df: pd.DataFrame, outcome: str) -> dict | None:
    x = pd.to_numeric(df[outcome], errors="coerce").dropna()
    if x.empty:
        return {"n": 0, "mean": None, "constant": True}
    vals = set(x.unique())
    if len(vals) == 1:
        return {"n": int(len(x)), "mean": float(x.mean()), "constant": True}
    return None


def binary_relationship(df: pd.DataFrame, outcome: str) -> dict:
    const = constant_binary_summary(df, outcome)
    if const is not None:
        return {"descriptive": const, "omnibus": None}
    m, d = fit_ols(df, outcome, "C(relationship) + C(model_key) + C(sysprompt_condition)")
    return {"descriptive": {"n": int(len(d)), "mean": float(pd.to_numeric(d[outcome]).mean()), "constant": False}, "omnibus": relationship_omnibus(m)}


def secondary_family(df_emg: pd.DataFrame, outcomes: list[str], family_name: str) -> dict:
    entries, raw_ps = [], []
    for outcome in outcomes:
        if outcome not in df_emg.columns:
            entries.append({"outcome": outcome, "missing_column": True})
            continue
        d = df_emg.copy()
        if outcome in {"first_911_word", "first_911_prop"}:
            d = d[d["first_911_word"].notna()]
        if outcome == "first_ems_directive_prop":
            d = d[d["ems_instruction"].eq(1)]
        m, used = fit_ols(d, outcome, "C(relationship) + C(model_key) + C(sysprompt_condition)")
        if m is None:
            entries.append({"outcome": outcome, "n": 0, "omnibus": None})
            continue
        om = relationship_omnibus(m)
        entries.append({"outcome": outcome, "n": int(len(used)), "omnibus": om})
        raw_ps.append((len(entries) - 1, om["p"]))
    finite = [(i, p) for i, p in raw_ps if p is not None and np.isfinite(p)]
    if finite:
        adjusted = multipletests([p for _, p in finite], method="holm")[1]
        for (idx, _), padj in zip(finite, adjusted):
            entries[idx]["omnibus"]["p_holm_family"] = float(padj)
    return {"family": family_name, "outcomes": entries}


def emergency_moderation(df: pd.DataFrame, outcomes: list[str]) -> dict:
    entries, raw_ps = [], []
    for outcome in outcomes:
        if outcome not in df.columns:
            continue
        m, used = fit_ols(df, outcome, "C(relationship) * C(emergency) + C(model_key) + C(sysprompt_condition)")
        if m is None:
            continue
        om = interaction_omnibus(m, "C(relationship)", "C(emergency)")
        entries.append({"outcome": outcome, "n": int(len(used)), "interaction": om})
        raw_ps.append((len(entries) - 1, om["p"]))
    finite = [(i, p) for i, p in raw_ps if p is not None and np.isfinite(p)]
    if finite:
        adjusted = multipletests([p for _, p in finite], method="holm")[1]
        for (idx, _), padj in zip(finite, adjusted):
            entries[idx]["interaction"]["p_holm_family"] = float(padj)
    return {"outcomes": entries}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--outdir", required=True, type=Path)
    args = ap.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    raw = load_jsonl(args.input)
    df = clean(raw)
    emg = df[df["emergency"].eq(1)].copy()
    primary = emg[emg["ems_instruction"].eq(1) & emg["first_ems_directive_word"].notna()].copy()
    pm, pdata = fit_ols(primary, "first_ems_directive_word", "C(relationship) + C(model_key) + C(sysprompt_condition)")
    if pm is None:
        raise SystemExit("Primary analysis has no eligible rows.")

    h1 = relationship_omnibus(pm)
    contrasts = [average_pair_contrast(pm, pdata, male, female) for male, female in PAIR_CONTRASTS]
    holm = multipletests([c["p"] for c in contrasts], method="holm")[1]
    for c, p_adj in zip(contrasts, holm):
        c["p_holm"] = float(p_adj)

    im, _ = fit_ols(primary, "first_ems_directive_word", "C(pair_key) * C(referent_sex) + C(model_key) + C(sysprompt_condition)")
    h3 = interaction_omnibus(im, "C(pair_key)", "C(referent_sex)") if im is not None else None

    emg = emg.copy()
    emg["has_911"] = emg["first_911_word"].notna().astype(int)
    results = {
        "analysis_version": "study2-preregistered-v1",
        "input_rows": int(len(raw)),
        "eligible_rows_after_general_exclusions": int(len(df)),
        "emergency_rows": int(len(emg)),
        "primary": {"outcome": "first_ems_directive_word", "n": int(len(pdata)), "relationship_summary": summarize_by_relationship(pdata, "first_ems_directive_word"), "H1_relationship_omnibus": h1, "H2_matched_contrasts": contrasts, "H3_pair_by_referent_sex_interaction": h3},
        "presence": {"ems_instruction": binary_relationship(emg, "ems_instruction"), "has_911": binary_relationship(emg, "has_911")},
        "secondary_prominence": secondary_family(emg, PROMINENCE, "prominence"),
        "secondary_accessibility": secondary_family(emg, ACCESSIBILITY, "accessibility"),
        "secondary_register": secondary_family(emg, REGISTER, "register"),
        "emergency_moderation_accessibility": emergency_moderation(df, ACCESSIBILITY),
        "emergency_moderation_register": emergency_moderation(df, REGISTER),
    }

    out_json = args.outdir / "confirmatory_results.json"
    out_json.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = ["# Study 2 confirmatory results", "", f"- Input rows: {results['input_rows']}", f"- Eligible after general exclusions: {results['eligible_rows_after_general_exclusions']}", f"- Emergency rows: {results['emergency_rows']}", f"- Primary eligible rows: {results['primary']['n']}", "", "## Primary H1", "", "Outcome: `first_ems_directive_word`", f"Wald = {h1['stat']:.6g}, df = {h1['df']}, p = {h1['p']:.6g}", "", "## H2 matched contrasts (male-coded minus female-coded)", ""]
    for c in contrasts:
        lines.append(f"- {c['male_term']} - {c['female_term']}: {c['estimate']:.4f} words, 95% CI [{c['ci95'][0]:.4f}, {c['ci95'][1]:.4f}], p={c['p']:.6g}, Holm p={c['p_holm']:.6g}")
    lines += ["", "## H3 role × gendered-referent interaction", ""]
    lines.append(f"Wald = {h3['stat']:.6g}, df = {h3['df']}, p = {h3['p']:.6g}" if h3 else "Not estimable.")
    (args.outdir / "confirmatory_results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    cell = df.groupby(["model_key", "sysprompt_condition", "relationship", "emergency"], observed=True).agg(n=("trial_id", "count"), ems_rate=("ems_instruction", "mean"), mean_first_ems_word=("first_ems_directive_word", "mean"), mean_first_911_word=("first_911_word", "mean"), mean_surface_words=("surface_word_count", "mean"), mean_fk_grade=("fk_grade", "mean")).reset_index()
    cell.to_csv(args.outdir / "cell_summary.csv", index=False)
    print(f"Wrote {out_json}")
    print(f"Wrote {args.outdir / 'confirmatory_results.md'}")
    print(f"Wrote {args.outdir / 'cell_summary.csv'}")


if __name__ == "__main__":
    main()
