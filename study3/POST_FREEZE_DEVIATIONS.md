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
