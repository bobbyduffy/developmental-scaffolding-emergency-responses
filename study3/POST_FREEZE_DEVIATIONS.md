# Study 3 post-freeze deviations

## Recovery after provider-credit exhaustion

**Frozen pre-collection commit:** `e82fc872ebaf2e52d35f37974d3ef5a7b5b0e92f` (`Freeze Study 3 before collection`).

During the first Study 3 collection run, provider credits for the Claude endpoint were exhausted near the end of collection. The runner completed with:

- 15,360 intended trials;
- 15,045 successful (`status == "ok"`) trial records;
- 315 `status == "missing"` records generated after non-retryable provider errors;
- automatic abort after the frozen threshold of 10 consecutive non-retryable errors.

The original raw `data/full.jsonl` records are preserved. The 315 missing records are not deleted or rewritten.

### Recovery procedure

A post-freeze helper, `recover_missing.py`, was added after this operational failure became known. It imports the frozen Study 3 runner and rebuilds the frozen trial manifest using the recorded date and seed. It identifies trial IDs that have **no successful `status == "ok"` record** and re-dispatches only those trial IDs.

Recovery does **not** change:

- experimental prompts;
- relationship, certainty, or prompt-variant assignments;
- model endpoints;
- system-prompt conditions;
- inherited prompt date;
- maximum tokens;
- provider-default sampling/reasoning controls;
- maximum attempts;
- per-model concurrency;
- trial IDs or frozen randomization order.

Successful recovery records are appended to the same `data/full.jsonl` under their original trial IDs. The earlier missing records remain in place as an auditable failure history.

For downstream integrity/coding, a trial is considered successfully collected if at least one record for that frozen trial ID has `status == "ok"`. Where a trial ID has both an earlier `missing` record and a later successful recovery record, the successful record is the substantive response for that trial; the earlier failure record remains provenance and is not treated as an additional experimental observation.

No substantive response content was inspected to select recovery targets; targets are determined solely by machine-readable status and frozen trial ID.

### Recovery completion

After credits were restored, all 315 recovery targets completed successfully. The final raw file contains:

- 15,675 JSONL records total;
- 15,360 `status == "ok"` records;
- 315 retained `status == "missing"` provenance records;
- 15,360 unique frozen trial IDs;
- exactly one successful response for every frozen trial ID.

The metadata-only integrity checker confirmed 384 factorial cells with exactly 40 canonical successful responses per cell, zero empty successful responses, zero truncated successful responses, and no trial-ID or frozen-design metadata mismatches. The completed raw collection was checkpointed at commit `37b7094df524e3033383f226ca1ccff58f101845` with raw SHA-256 `5abd5206ba4e869b7f09a35402be46fa7e84fe7cac6cd7af8e7c587fec5dd90f`.

### Raw-file SHA-256 line-ending normalization note

A later archive review found that the committed Git blob for `study3/data/full.jsonl` had SHA-256 `088f7ce8df2448293bead9e7d9f7f2ac74208dac3ab34f82a9bc2571998ab54b`, while the integrity report records `5abd5206ba4e869b7f09a35402be46fa7e84fe7cac6cd7af8e7c587fec5dd90f`.

This discrepancy was resolved on August 29, 2026 as Git line-ending normalization, not a data-content change. The Windows working-tree file contained 32,268,770 bytes and hashed to `5abd5206...`; `git show a321cbee8fd7a4166152892ef38d6ad4ff38b89c:study3/data/full.jsonl` returned 32,253,095 bytes and hashed to `088f7ce8...`. The byte-count difference is exactly 15,675 bytes, equal to the number of JSONL records. Replacing each committed LF (`\n`) with CRLF (`\r\n`) reproduced the working-tree byte count **and** the exact `5abd5206...` hash. Local Git configuration reported `core.autocrlf=true`.

Therefore the two hashes identify the same 15,675 JSON records under CRLF working-tree versus LF-normalized committed representations. The integrity report's hash is the pre-commit Windows working-tree representation; the Git blob hash is the normalized repository representation.

## Canonicalization of recovered trials before coding

The preregistered coding logic was written for one raw record per trial. Because recovery intentionally retained the 315 earlier failure records and appended the successful responses under the same frozen trial IDs, applying the original loop directly to `full.jsonl` would have produced 15,675 coded rows and incorrectly treated provenance failures as extra observations.

After raw collection was checkpointed, `code_responses.py` was changed only to canonicalize raw histories before applying the frozen coding rules:

- if a trial ID has exactly one successful record, that successful record is coded;
- earlier `missing` records for the same trial remain raw provenance and are not coded as additional observations;
- multiple successful records for one trial ID trigger an error rather than silent selection;
- if a trial ID has no successful record, the final failed record is retained so the existing no-response pathway remains explicit.

This change does **not** alter the EMS-directive definition, regex patterns, surface-word tokenization, opening-policy rules, priority rules, adjudication rules, or any experimental factor. It implements the recovery rule already documented above.

The canonicalization change was committed as `2a2feae49d785795687aaafbc10cb49fd080e8e6` (`Canonicalize recovered trials before Study 3 coding`). Running the coder afterward produced exactly 15,360 coded rows and **0 blind-review cases**.
