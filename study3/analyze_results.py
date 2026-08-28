#!/usr/bin/env python3
"""Frozen-candidate Study 3 confirmatory analysis."""
from __future__ import annotations

import argparse, json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests

PRIMARY_FORMULA = "first_ems_directive_word ~ C(relationship) * C(certainty) + C(relationship) * C(prompt_variant) + C(certainty) * C(prompt_variant) + C(model_key) + C(sysprompt_condition)"
BINARY_FORMULA_TEMPLATE = "{outcome} ~ C(relationship) * C(certainty) + C(relationship) * C(prompt_variant) + C(certainty) * C(prompt_variant) + C(model_key) + C(sysprompt_condition)"
HET_FORMULA = "first_ems_directive_word ~ C(relationship) * C(certainty) * C(prompt_variant) + C(model_key) + C(sysprompt_condition)"

PAIRS = [("mommy","daddy"),("mom","dad"),("girlfriend","boyfriend"),("wife","husband")]


def load_jsonl(path: Path) -> pd.DataFrame:
    return pd.read_json(path, lines=True)


def valid_rows(df: pd.DataFrame) -> pd.DataFrame:
    ok = df["status"].eq("ok")
    if "empty_response" in df: ok &= ~df["empty_response"].fillna(False)
    if "truncated" in df: ok &= ~df["truncated"].fillna(False)
    return df.loc[ok].copy()


def interaction_names(model, a="C(relationship)", b="C(certainty)", require_variant=False):
    names=[]
    for name in model.params.index:
        if a in name and b in name:
            if require_variant:
                if "C(prompt_variant)" in name: names.append(name)
            else:
                if "C(prompt_variant)" not in name: names.append(name)
    return names


def joint_wald(model, names):
    if not names: return {"estimable":False,"reason":"no matching coefficients"}
    pnames=list(model.params.index); R=np.zeros((len(names),len(pnames)))
    for i,n in enumerate(names): R[i,pnames.index(n)]=1
    try:
        w=model.wald_test(R, scalar=True)
        cov_r = R @ np.asarray(model.cov_params()) @ R.T
        rank = int(np.linalg.matrix_rank(cov_r))
        out={"estimable":True,"statistic":float(w.statistic),"df":int(len(names)),"p":float(w.pvalue)}
        if rank < len(names):
            out["covariance_rank"] = rank
            out["rank_deficient"] = True
        return out
    except Exception as exc:
        return {"estimable":False,"reason":str(exc)}


def fit_hc3(df, formula):
    return smf.ols(formula, data=df).fit(cov_type="HC3")


def _design_info(model):
    """Return Patsy DesignInfo across statsmodels versions.

    statsmodels 0.14 commonly exposes data.design_info directly; 0.15 may use
    PandasData without that attribute while retaining DesignInfo on orig_exog.
    """
    data = model.model.data
    info = getattr(data, "design_info", None)
    if info is None:
        info = getattr(getattr(data, "orig_exog", None), "design_info", None)
    if info is None:
        raise RuntimeError("Patsy design_info unavailable; cannot build frozen contrasts")
    return info


def equal_variant_prediction(model, relationship, certainty):
    rows=[]
    frame=model.model.data.frame
    for variant in ("A","B"):
        for model_key in sorted(frame["model_key"].dropna().unique()):
            for sys in sorted(frame["sysprompt_condition"].dropna().unique()):
                rows.append({"relationship":relationship,"certainty":certainty,"prompt_variant":variant,"model_key":model_key,"sysprompt_condition":sys})
    from patsy import build_design_matrices
    mat=np.asarray(build_design_matrices([_design_info(model)],pd.DataFrame(rows))[0])
    v=mat.mean(axis=0)
    est=float(v@model.params.values)
    return est,v


def contrast(model, v):
    beta=model.params.values; cov=np.asarray(model.cov_params()); est=float(v@beta); se=float(np.sqrt(max(float(v@cov@v),0.0)))
    from scipy.stats import norm
    z=est/se if se>0 else np.nan; p=float(2*norm.sf(abs(z))) if np.isfinite(z) else np.nan
    return {"estimate":est,"se":se,"ci_low":est-1.96*se,"ci_high":est+1.96*se,"p_raw":p}


def pair_attenuation(model):
    out=[]
    for female,male in PAIRS:
        ef2,vf2=equal_variant_prediction(model,female,2); em2,vm2=equal_variant_prediction(model,male,2)
        ef4,vf4=equal_variant_prediction(model,female,4); em4,vm4=equal_variant_prediction(model,male,4)
        d2=em2-ef2; d4=em4-ef4
        c=contrast(model,(vm4-vf4)-(vm2-vf2))
        c.update({"pair":f"{male}-{female}","level2_difference":d2,"level4_difference":d4,"attenuation_L4_minus_L2":c.pop("estimate")})
        out.append(c)
    ps=[x["p_raw"] for x in out]
    adj=multipletests(ps,method="holm")[1]
    for x,p in zip(out,adj): x["p_holm"]=float(p)
    return out


def cell_summary(df, outcome):
    g=df.groupby(["relationship","certainty","prompt_variant","model_key","sysprompt_condition"],dropna=False)[outcome]
    s=g.agg(["count","mean","std","median"]).reset_index()
    return s.to_dict(orient="records")


def analyze(df):
    v=valid_rows(df)
    results={"n_input":len(df),"n_valid":len(v)}

    # EMS presence: constant outcomes are descriptive only.
    presence=v.dropna(subset=["ems_instruction"]).copy()
    results["ems_presence_rate"]=float(presence["ems_instruction"].mean()) if len(presence) else None
    if len(presence) and presence["ems_instruction"].nunique()>1:
        m=fit_hc3(presence,BINARY_FORMULA_TEMPLATE.format(outcome="ems_instruction"))
        results["ems_presence_omnibus"]=joint_wald(m,interaction_names(m))
    else:
        results["ems_presence_omnibus"]={"estimable":False,"reason":"constant or empty outcome"}

    lat=v[(v["ems_instruction"]==1)&v["first_ems_directive_word"].notna()].copy()
    results["n_latency"]=len(lat)
    if not len(lat):
        raise RuntimeError("No EMS-present rows with latency; primary analysis cannot be fit")
    primary=fit_hc3(lat,PRIMARY_FORMULA)
    results["H1_relationship_x_certainty"]=joint_wald(primary,interaction_names(primary))
    results["pair_attenuation"]=pair_attenuation(primary)
    results["latency_cells"]=cell_summary(lat,"first_ems_directive_word")

    het=fit_hc3(lat,HET_FORMULA)
    results["variant_heterogeneity"]=joint_wald(het,interaction_names(het,require_variant=True))

    binary_ps=[]; binary_keys=[]
    for outcome in ("ems_priority_opening","ems_within_10_words"):
        sub=lat.dropna(subset=[outcome]).copy()
        results[f"{outcome}_rate"]=float(sub[outcome].mean()) if len(sub) else None
        if len(sub) and sub[outcome].nunique()>1:
            m=fit_hc3(sub,BINARY_FORMULA_TEMPLATE.format(outcome=outcome))
            test=joint_wald(m,interaction_names(m))
        else: test={"estimable":False,"reason":"constant or empty outcome"}
        results[f"{outcome}_omnibus"]=test
        if test.get("estimable"): binary_ps.append(test["p"]); binary_keys.append(f"{outcome}_omnibus")

    pres_test=results["ems_presence_omnibus"]
    if pres_test.get("estimable"): binary_ps.insert(0,pres_test["p"]); binary_keys.insert(0,"ems_presence_omnibus")
    if binary_ps:
        adj=multipletests(binary_ps,method="holm")[1]
        results["binary_guidance_holm"]={k:float(p) for k,p in zip(binary_keys,adj)}
    else: results["binary_guidance_holm"]={}

    return results


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--indir",type=Path,default=Path("./data")); args=ap.parse_args()
    path=args.indir/"results.jsonl"; df=load_jsonl(path); results=analyze(df)
    out=args.indir/"confirmatory_analysis.json"; out.write_text(json.dumps(results,indent=2),encoding="utf-8")
    print(f"Wrote {out}")
    print("H1:",results["H1_relationship_x_certainty"])

if __name__=="__main__": main()
