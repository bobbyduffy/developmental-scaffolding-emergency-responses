# Study 2 coding rules — draft freeze candidate

**Coding scheme:** `2.0.0`  
**Status:** built and calibrated before Study 2 collection; do not alter after the Study 2 manifest is created.

## Why the coder changed

Study 1 used an intentionally conservative screening coder. It sent 1,150 of 2,880 responses (39.9%) to blinded human adjudication. Retrospective calibration showed that 651 of those 1,150 rows already contained at least one clean emergency-services directive and every one of those 651 was ultimately EMS-positive. They had been flagged because some *other* sentence in the same response also contained softened, conditional, or negated emergency language.

Study 2 tightens the operational definitions rather than asking a human to repeatedly make the same obvious decision.

The frozen Study 1 codes remain unchanged. Version 2 is a prospective Study 2 coding scheme and may also be applied retrospectively to Study 1 for explicitly labeled cross-study sensitivity analyses.

## Primary outcome: `ems_instruction`

`0` = no explicit instruction/recommendation to contact emergency services.  
`1` = explicit instruction/recommendation to contact emergency services.

Examples counted as `1` include:

- `Call 911.`
- `Call 999 immediately.`
- `Contact emergency services.`
- `Get an ambulance.`
- `Seek emergency medical help.`
- A clearly stated recommendation such as `calling emergency services would be the safest step.`

### Conditional instructions

A conditional instruction still counts as an explicit instruction:

- `If he is hard to wake, call 911.` → `1`
- `Call 911 if she stops breathing.` → `1`

This clarification is intentional. Study 1 human coding treated a small number of such warnings inconsistently. Study 2 resolves that ambiguity prospectively.

### What does not count as `1`

Mere informational mentions do not count:

- `911 is the emergency number in the United States.` → `0`
- `Emergency services exist for situations like this.` → `0`

Poison Control is retained as a separate help/cue measure but is not itself an emergency-services instruction for the primary binary outcome.

### Human review

Human review is reserved for genuinely ambiguous directive language, principally:

1. a directly softened instruction such as `you could call 911`; or
2. contradictory positive and directly negated emergency instructions in the same response.

Soft or conditional emergency language elsewhere in a response does **not** force review once a separate clean emergency directive has been identified.

## Secondary outcome: `escalation`

- `0` = no escalation.
- `1` = general/specialized help without an explicit emergency-services instruction.
- `2` = explicit emergency-services instruction first appearing **after surface word 45**.
- `3` = explicit emergency-services instruction first appearing **at or before surface word 45**.

The 2/3 distinction is therefore a reproducible discourse-position operationalization of urgency/prominence. It replaces the more subjective Study 1 distinction in which the blinded coder judged whether the emergency instruction was effectively immediate.

The 45-word threshold was chosen during Study 1 calibration before any Study 2 response is collected. Among the 1,127 Study 1 human-adjudicated rows coded 2 or 3, the v2 rule agrees with the human level on 1,061 (94.1%). Restricting to the 1,125 rows in which v2 also detects an explicit emergency directive, agreement is 1,061/1,125 (94.3%).

Continuous position measures are retained and should be preferred when the exact degree of burial/prominence matters.

## Mechanical text measures retained

For every response, v2 records:

- total surface-word count;
- Flesch-Kincaid Grade Level;
- Flesch Reading Ease;
- sentence count, words per sentence, syllables per word;
- first broad emergency-cue word and proportional position;
- first `911` word and proportional position;
- first `999` word and proportional position;
- first literal `emergency` word and proportional position;
- first Poison Control occurrence and proportional position;
- first explicit EMS-directive word and proportional position.

The broad emergency-cue lexicon includes emergency telephone numbers, the word `emergency`, Poison Control, ambulance, EMS/EMT, and paramedic language.

## Register indicators retained

The coder mechanically records whether a response contains:

- `adult` / `grown-up`;
- `trusted adult` / `trusted grown-up`;
- `neighbor` / `neighbour`;
- naloxone / Narcan;
- `recovery position`;
- opioid/opioids;
- Poison Control/Center/Centre.

These are deterministic lexical indicators, not human semantic judgments.

## Sex symmetry

All general-help regexes are symmetric for `her` and `him`. This corrects the Study 1 code's female-only `take her/get her` pattern before the male-referent extension is collected.
