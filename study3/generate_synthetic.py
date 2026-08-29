#!/usr/bin/env python3
"""Generate deterministic synthetic Study 3 coded results for analysis validation."""
from __future__ import annotations

import argparse, json, random
from pathlib import Path

import run_experiment as r


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--outdir",type=Path,default=Path("./synthetic_data")); ap.add_argument("--seed",type=int,default=3003); args=ap.parse_args()
    args.outdir.mkdir(parents=True,exist_ok=True); rng=random.Random(args.seed)
    trials=r.build_trials(r.INHERITED_PROMPT_DATE,r.DEFAULT_SEED)
    rel_base={"mommy":0,"daddy":5,"mom":2,"dad":4,"girlfriend":10,"boyfriend":9,"wife":7,"husband":4}
    certainty_shift={1:10,2:5,3:2,4:0}
    rows=[]
    for t in trials:
        # Deliberately leave some EMS absence at L1 and create attenuation with certainty.
        p_ems={1:.82,2:.96,3:.995,4:1.0}[t.certainty]
        ems=int(rng.random()<p_ems)
        if ems:
            scale={1:1.0,2:.8,3:.45,4:.15}[t.certainty]
            rel=rel_base[t.relationship]*scale
            variant=2 if t.prompt_variant=="B" else 0
            pos=max(1,round(6+certainty_shift[t.certainty]+rel+variant+rng.gauss(0,4)))
            priority=int(pos<=12 and rng.random()<.8)
            within10=int(pos<=10)
        else:
            pos=None; priority=None; within10=None
        rows.append({
            "trial_id":t.trial_id,"order_index":t.order_index,"model_key":t.model_key,"api_model":t.api_model,
            "sysprompt_condition":t.sysprompt_condition,"prompt_id":t.prompt_id,"relationship":t.relationship,
            "referent_sex":t.referent_sex,"pair_key":t.pair_key,"prompt_variant":t.prompt_variant,"certainty":t.certainty,
            "certainty_label":t.certainty_label,"rep":t.rep,"status":"ok","truncated":False,"empty_response":False,
            "ems_instruction":ems,"first_ems_directive_word":pos,"ems_priority_opening":priority,"ems_within_10_words":within10,
        })
    path=args.outdir/"results.jsonl"
    with open(path,"w",encoding="utf-8") as fh:
        for row in rows: fh.write(json.dumps(row)+"\n")
    print(f"Wrote {path} ({len(rows)} rows)")

if __name__=="__main__": main()
