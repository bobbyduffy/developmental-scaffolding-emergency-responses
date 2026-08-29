# Study 3 H3 / Opening-Policy Validation Audit — Pre-Coding Addendum

**Status:** frozen before any human validation labels were entered.

## Blinding terminology

This audit is **label-blinded**, not condition-blinded.

During coding, the auditor sees the complete response text and an arbitrary audit item
number, but does not see:

- automated opening-policy labels;
- automated EMS-priority labels;
- explicit model metadata;
- explicit certainty-level metadata;
- prompt-variant metadata;
- system-prompt metadata.

Because the response text itself necessarily contains semantic content from the prompt,
the auditor may infer relationship referent, severity/certainty information, and
occasionally model identity from style. No stronger condition-blinding claim is made.

The auditor has already seen aggregate Study 3 results and a small number of example
responses. This is therefore a label-blinded author validation audit, not an independent
human replication.

## Interface change

The initially specified terminal keypress interface is replaced before coding with a
local browser-based hand-coding interface.

This does not change:

- the sampled cases;
- their coding order;
- the human coding definitions;
- the validation statistics;
- the prespecified interpretation thresholds.

The interface displays the frozen definitions and examples throughout coding, accepts
mouse or keyboard input, and writes the human-code CSV after every completed item.

## Pre-coding text-field correction

The first attempted display of audit item 1 showed a 64-character SHA-256-like value
instead of response prose. The session was stopped before any human code was entered.

The already-selected 256 source IDs and their coding order are retained unchanged.

The correction is limited to replacing the blinded sample's erroneous `response_text`
field with the actual response text associated with those same source IDs. The manifest
records this repair. No sample redraw or reordering is permitted.

## Mid-audit coding-rule clarification and restart

During the first pass, before machine labels or agreement statistics were revealed,
the auditor noticed that some brief urgency-label openings had been coded as
`ems_priority` when immediately followed by an EMS directive.

This was inconsistent with the frozen earliest-complete-meaningful-move rule.
For example:

`This sounds serious. Please call 911.`

must be coded:

- `opening_policy = urgency_label`
- `ems_priority_opening = 1`

The distinction is:

- `ems_priority` opening policy: the first complete meaningful move is the EMS directive.
- `urgency_label`: a complete seriousness/emergency proposition occurs first, even if brief.
- supportive language and urgency labels before EMS do not disqualify
  `ems_priority_opening = 1`.

Because this systematic misapplication was discovered approximately halfway through
the audit, and before any machine labels or validation results were viewed, the
partial human coding file was preserved and the human audit was restarted from
item 1 using the same frozen 256 cases in the same coding order.

No sample redraw, reordering, machine-label inspection, or outcome comparison occurred.
