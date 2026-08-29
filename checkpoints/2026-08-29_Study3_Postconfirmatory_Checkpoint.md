# Study 3 Checkpoint — 2026-08-29

## Repository / provenance state

Study 3 has completed collection, recovery, coding, confirmatory analysis, and the first round of prespecified secondary/reporting analysis.

Key commits:

- Pre-collection Study 3 freeze: `e82fc872ebaf2e52d35f37974d3ef5a7b5b0e92f`
- Raw collection checkpoint: `37b7094df524e3033383f226ca1ccff58f101845`
- Canonicalization change: `2a2feae49d785795687aaafbc10cb49fd080e8e6`
- Coded-data checkpoint: `a0dbe0ddb0d5a78abf80886b0b6282d4512d8f6c`
- Confirmatory-analysis checkpoint: `a321cbee8fd7a4166152892ef38d6ad4ff38b89c`
- Raw hash line-ending documentation: `dba6b1bd41935c6bf69caf6e7248cf50aefd8591`
- Prespecified secondary-reporting script: `56da68a1837311325d4bcca218454d8ac44fc41a`
- EMS-presence sensitivity specification: `ccef3450279e98fa944ad312a20e92372441eb15`

Main currently represents the completed Study 1 + Study 2 record. Study 3 is being prepared for merge via pull request. Preserve the individual Study 3 commits; do not squash.

---

## Collection and recovery

Frozen design:

- 8 relationship referents
- 4 certainty levels
- 2 prompt variants
- 3 system-prompt conditions
- 2 model endpoints
- 40 repetitions per exact cell
- Planned N = **15,360**

Final raw state:

- **15,675 JSONL records**
- **15,360 successful responses**
- **315 retained missing/failure provenance records**
- **15,360 unique frozen trial IDs**
- **384 factorial cells**
- **40 canonical successful responses per cell**
- **0 empty successful responses**
- **0 truncated successful responses**

The 315 missing records came from Claude provider-credit exhaustion. Recovery was append-only under the same trial IDs, preserving earlier failures.

### Raw hash discrepancy — resolved

The apparent mismatch between:

- Windows working-tree SHA-256: `5abd5206ba4e869b7f09a35402be46fa7e84fe7cac6cd7af8e7c587fec5dd90f`
- committed Git blob SHA-256: `088f7ce8df2448293bead9e7d9f7f2ac74208dac3ab34f82a9bc2571998ab54b`

was entirely due to CRLF → LF normalization.

- working tree: **32,268,770 bytes**
- committed blob: **32,253,095 bytes**
- difference: **15,675 bytes**, exactly one extra carriage-return byte per JSONL line
- converting the committed LF blob back to CRLF reproduced the exact `5abd5206...` hash
- local `core.autocrlf=true`

Conclusion: **same records, different line-ending representation; no data-content discrepancy.**

---

## Coding

Canonical coding produced:

- **15,360 coded rows**
- **0 blind-review cases**

The post-freeze canonicalization change was operational only: one successful record per frozen trial ID was coded while prior failed histories remained raw provenance. No EMS definitions, regexes, opening-policy rules, adjudication rules, or experimental factors were changed.

---

## Confirmatory results

### EMS presence

- **14,991 / 15,360 EMS-present**
- overall rate = **97.60%**
- **369 EMS-absent responses**

Relationship × certainty omnibus:

- Wald = **487.90**
- df = **21**
- p ≈ **4.96 × 10^-90**

### Primary H1 — latency conditional on EMS presence

N = **14,991**

Relationship × certainty omnibus:

- Wald = **1334.96**
- df = **21**
- p ≈ **7.95 × 10^-270**

This remains the single primary confirmatory test.

### H2 — matched-pair L4 minus L2 contrasts

- daddy − mommy: **+1.51**, Holm p ≈ **.151**
- dad − mom: **+2.87**, Holm p ≈ **.042**
- boyfriend − girlfriend: **−3.24**, Holm p ≈ **.151**
- husband − wife: **+6.18**, Holm p ≈ **.00053**

At Level 4, all male-minus-female pair differences are near zero:

- daddy − mommy: **−0.13**
- dad − mom: **+0.54**
- boyfriend − girlfriend: **+0.25**
- husband − wife: **+0.16**

### Other confirmatory outcomes

Prompt-variant heterogeneity:

- Wald = **153.54**
- df = **21**
- p ≈ **3.73 × 10^-22**

EMS-priority opening:

- rate ≈ **70.34%**
- Wald = **1589.98**
- numerical p-value underflowed to 0; do not describe as literally p = 0

EMS within first 10 words:

- rate ≈ **68.69%**
- Wald = **1054.43**
- df = **21**
- p ≈ **7.03 × 10^-210**

---

## Prespecified secondary / sensitivity results so far

### Ordered certainty trend

- Wald = **781.64**
- df = **7**
- p ≈ **1.70 × 10^-164**

Categorical certainty retains interpretive priority.

### Model heterogeneity

Relationship × certainty × model:

- Wald = **1201.07**
- df = **21**
- p ≈ **3.46 × 10^-241**

Stratified relationship × certainty tests:

- Claude Sonnet 5: Wald = **1763.71**, df = 21
- GPT-5.6 Terra: Wald = **859.24**, df = 21, p ≈ **2.44 × 10^-168**

The latency interaction is therefore strong in both endpoints, but its shape differs substantially by model.

### System heterogeneity

Relationship × certainty × system:

- Wald = **176.74**
- df = **42**
- p ≈ **1.87 × 10^-18**

All three system strata independently show strong relationship × certainty interactions.

### Variant-stratified latency

- Variant A: Wald = **501.39**, df = 21, p ≈ **7.57 × 10^-93**
- Variant B: Wald = **945.36**, df = 21, p ≈ **1.20 × 10^-186**

The phenomenon is not confined to one wording variant.

---

## Matched-pair trajectories across all certainty levels

Male-coded minus female-coded latency differences:

### daddy − mommy
- L1: **+9.29**
- L2: **−1.65**
- L3: **−0.22**
- L4: **−0.13**

### dad − mom
- L1: **+2.74**
- L2: **−2.33**
- L3: **+1.14**
- L4: **+0.54**

### boyfriend − girlfriend
- L1: **−0.11**
- L2: **+3.49**
- L3: **+0.80**
- L4: **+0.25**

### husband − wife
- L1: **−0.69**
- L2: **−6.02**
- L3: **−0.53**
- L4: **+0.16**

Working interpretation:

> Relationship-specific timing differences are strongest under ambiguous/intermediate evidence and collapse rapidly once respiratory compromise is supplied. The pattern is not a simple monotonic common sex effect.

### Role / referent-sex decomposition

pair_key × referent_sex × certainty:

- Wald = **34.80**
- df = **9**
- p ≈ **6.46 × 10^-5**

referent_sex × certainty:

- Wald = **49.34**
- df = **3**
- p ≈ **1.10 × 10^-10**

Interpretation: a sex-coded component exists, but it varies materially across relationship roles. Do not reduce this to a generic male-vs-female referent effect.

---

## EMS-presence structure

### By model

GPT-5.6 Terra:

- **7,680 / 7,680 EMS-present**
- **0 omissions**

Claude Sonnet 5:

- **7,311 / 7,680 EMS-present**
- **369 omissions**
- presence rate ≈ **95.20%**

Therefore **all 369 EMS omissions occurred in Claude**.

### Claude omissions by certainty

- L1: **365 / 1,920 = 19.01%**
- L2: **4 / 1,920 = 0.21%**
- L3: **0 / 1,920**
- L4: **0 / 1,920**

So **98.9% of Claude omissions occurred at L1**.

### Claude L1 omissions by relationship

- girlfriend: **128 / 240 = 53.3%**
- boyfriend: **94 / 240 = 39.2%**
- wife: **90 / 240 = 37.5%**
- husband: **47 / 240 = 19.6%**
- dad: **4 / 240 = 1.7%**
- daddy: **1 / 240 = 0.4%**
- mommy: **1 / 240 = 0.4%**
- mom: **0 / 240**

The presence effect is overwhelmingly a **Claude × low-certainty × romantic-partner** phenomenon.

### Claude L1 wording dependence

Variant A omission rates among romantic-partner referents were much higher than Variant B:

- girlfriend: A **79.2%**, B **27.5%**
- wife: A **57.5%**, B **17.5%**
- boyfriend: A **44.2%**, B **34.2%**
- husband: A **32.5%**, B **6.7%**

System-prompt effects also vary strongly by relationship and wording.

---

## Frozen basis for next EMS-presence sensitivity tests

`PRESENCE_SENSITIVITY_SPEC.md` was committed before executing the next formal models.

Allowed prespecified formal sensitivity tests:

1. **relationship × certainty × model** on `ems_instruction`
2. **relationship × certainty × system prompt** on `ems_instruction`

Both use the frozen HC3 linear-probability framework.

Important restraint:

- no new formal EMS-presence relationship × certainty × variant test was promoted, because frozen H5 applied to latency
- no special within-Claude interaction test was promoted after seeing the omission pattern
- such analyses may remain descriptive or be labeled exploratory if later modeled

Rank / estimability diagnostics must be reported explicitly.

---

## Current conceptual picture

Two empirically distinct escalation dimensions are emerging:

1. **Whether EMS is mentioned at all**
   - model-specific
   - entirely Claude in this dataset
   - concentrated in low-certainty romantic-partner prompts
   - nearly disappears at unresponsiveness
   - fully disappears once respiratory abnormality is supplied

2. **How early EMS is foregrounded once present**
   - strongly relationship-sensitive in both Claude and GPT
   - heterogeneous by model, system prompt, and wording
   - pair differences largely collapse by L3/L4

Cautious working formulation:

> Relationship framing strongly affects emergency-response policy under ambiguous or intermediate evidence, but these differences contract sharply as decisive respiratory evidence is supplied. The manifestation differs across model endpoints and prompt surfaces: in Claude it can affect whether EMS appears at all under low certainty, while in both Claude and GPT it affects how quickly EMS is foregrounded once present.

This is consistent with a threshold / convergence account, but it does not directly identify a latent psychological mechanism.

---

## Important unresolved / next steps

1. Execute the already-frozen EMS-presence model and system sensitivity tests from `PRESENCE_SENSITIVITY_SPEC.md`.
2. Confirm robust covariance rank / estimability for the real H1 and new presence restrictions.
3. Checkpoint `secondary_reporting.json` if not already committed.
4. Complete model/system/variant descriptive tables and figures.
5. Consider a blinded validation audit for `ems_priority_opening`, because that outcome was coded automatically and received no human adjudication.
6. Update stale repository-facing documentation:
   - `study3/README.md` still says preflight / do not collect
   - root README does not yet list Study 3
7. Improve archival reproducibility:
   - root-level test invocation
   - dependency/environment pinning or lock record
8. Merge the Study 3 pull request into `main` using a **merge commit**, not squash.
9. Keep historical preflight branches rather than catching them up to main.
10. Consider protecting `main` against force pushes/deletion after Study 3 lands.

---

## Do not do

- Do not modify the frozen confirmatory output.
- Do not silently patch coding rules after seeing results.
- Do not merge categories or change estimator to recover significance.
- Do not turn descriptive wording/system patterns into newly “prespecified” hypotheses.
- Do not interpret the two tested endpoints as a representative random sample of all language models.
- Do not describe numerical p-value underflow as literal p = 0.

---

## Resume point

When work resumes, the clean next move is:

**implement and run the already-frozen EMS-presence model and system sensitivity tests, with explicit rank diagnostics, then checkpoint those outputs before further interpretation.**
