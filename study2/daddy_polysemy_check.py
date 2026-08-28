#!/usr/bin/env python3
"""Descriptive daddy-polysemy screen for raw Study 2 responses."""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path
ALT_RE = re.compile(r"\b(?:sugar\s+daddy|boyfriend|lover|romantic\s+partner|sexual\s+partner|sexual\s+term|kink|bdsm|bedroom\s+term|not\s+(?:your\s+)?father|daddy\s+(?:can|could|may|might)\s+(?:also\s+)?mean)\b", re.I)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--input",type=Path,required=True); ap.add_argument("--out",type=Path,required=True); args=ap.parse_args()
    flagged=[]; total=0
    for line in args.input.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        rec=json.loads(line)
        if rec.get("relationship") != "daddy" or rec.get("status") != "ok": continue
        total += 1; text=rec.get("response") or ""; m=ALT_RE.search(text)
        if m: flagged.append({"trial_id":rec.get("trial_id"),"emergency":rec.get("emergency"),"matched_phrase":m.group(0),"response":text.replace("\n"," ")})
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open("w",newline="",encoding="utf-8") as fh:
        w=csv.DictWriter(fh,fieldnames=["trial_id","emergency","matched_phrase","response"]); w.writeheader(); w.writerows(flagged)
    rate=len(flagged)/total if total else float("nan")
    print(f"Daddy responses: {total}"); print(f"Lexically flagged: {len(flagged)} ({rate:.2%})"); print(f"Wrote {args.out}")
if __name__ == "__main__": main()
