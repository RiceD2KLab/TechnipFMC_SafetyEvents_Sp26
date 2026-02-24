# Causal Chain Annotation Guidelines

## Purpose
You are annotating causal relationships in safety incident narratives. Your
annotations will be used to train and evaluate an automated system that extracts
causal information from incident reports.

## What to Annotate

Read the NARRATIVE column for each record. Identify three types of causal
relationships:

### CAUSED_BY — Primary cause of the incident
What failed, broke, or went wrong to directly cause the incident?

- Must be stated or strongly implied in the narrative.
- Copy the exact evidence phrase(s) into the evidence column.
- Example: "The crane cable snapped during lifting operations"
  - cause: "crane cable failure"
  - evidence: "The crane cable snapped"
  - confidence: high

### CONTRIBUTED_TO — Secondary contributing factors
What conditions made the incident possible or worse? (Swiss cheese model)

- Only annotate if explicitly mentioned in the narrative.
- Example: "No safety briefing was conducted that morning"
  - factor: "missing safety briefing"
  - evidence: "No safety briefing was conducted that morning"
  - confidence: high

### LED_TO — Intra-incident causal sequence
What happened step by step within the incident?

- Each step is an event -> outcome pair.
- Example: "The valve leaked hydraulic fluid. Pressure built up in the line.
  The pipe burst, striking the operator."
  - Step 1: event="valve leak", outcome="pressure buildup",
    evidence="The valve leaked hydraulic fluid. Pressure built up in the line."
  - Step 2: event="pressure buildup", outcome="pipe burst / operator struck",
    evidence="The pipe burst, striking the operator."

## Confidence Levels
- **HIGH**: Explicit causal language ("caused by", "due to", "resulted in",
  "because", "led to", "failure of")
- **MEDIUM**: Strongly implied by context or temporal sequence but no explicit
  causal language
- **LOW**: Possible interpretation but ambiguous

## Rules
1. Only annotate what the NARRATIVE says. Do not infer from metadata columns.
2. If no causal relationship is present, leave all annotation columns blank.
   This is correct and expected for some records.
3. Copy exact evidence spans from the narrative.
4. One cause per field. Use caused_by_2 for a second independent cause.
5. LED_TO captures SEQUENCE: if A->B->C, annotate A->B and B->C as separate entries.

### Edge Cases

**What if causal language spans multiple sentences?**
Quote the minimal span that captures the relationship. If the relevant phrases
are not contiguous, use "..." to bridge them — but always prefer a contiguous
quote when possible. Do not paraphrase.

**What if the narrative contradicts itself?**
Annotate the most specific and detailed account. Add a note explaining the
contradiction in the annotator_notes field.

**What if an entity from existing_entities is the cause but is not mentioned by
name in the narrative?**
Only annotate what is in the narrative text. Do not use the existing_entities
column to fill in information that is absent from the narrative. The
existing_entities column is reference context, not annotation source material.

**What if the same cause type appears twice — two independent causes?**
Use caused_by_1 for the first cause and caused_by_2 for the second. Each field
set is independent. Do not combine two causes into a single caused_by_1 entry.

**What about non-English text mixed into the narrative?**
Skip non-English portions entirely. Only annotate English causal relationships.
If the entire causal relationship is expressed in a non-English sentence, leave
the relevant fields blank and add a note in annotator_notes.

## Distinguishing CAUSED_BY vs CONTRIBUTED_TO

CAUSED_BY is the direct, proximate trigger of the incident. Without this event
or failure, the incident would not have occurred.

CONTRIBUTED_TO is an enabling condition or background factor. It increased the
likelihood or severity of the incident, but did not directly trigger it.

**Test to apply:** Ask "Would the incident still have happened without this
factor?" If yes, it is a contributing factor. If no, it is a cause.

**Example:**
- "The worker slipped on oil" — the oil is CAUSED_BY: it was the immediate
  trigger of the slip.
- "The worker was not wearing safety boots" — this is CONTRIBUTED_TO: it made
  the outcome worse but was not the trigger.

When in doubt, assign CAUSED_BY to the most proximate factor and CONTRIBUTED_TO
to background conditions such as missing PPE, inadequate training, or
environmental conditions that were present before the triggering event.

---

## LED_TO Chain Rules

LED_TO captures the step-by-step sequence of events within the incident. Each
entry represents one step: a triggering event and the outcome it produced.

- Each LED_TO entry captures ONE step: event -> outcome.
- For a chain A -> B -> C, use:
  - led_to_1_event = A, led_to_1_outcome = B
  - led_to_2_event = B, led_to_2_outcome = C
- The event of step N+1 should match the outcome of step N. This keeps the
  chain connected.
- Maximum 3 chain steps (led_to_1, led_to_2, led_to_3).
- If the chain in the narrative has more than 3 steps, capture the 3 most
  significant steps. Prefer the initial trigger and the final outcome as
  anchors, and pick the most consequential intermediate step.
- Do not repeat CAUSED_BY content in led_to_1. The LED_TO chain describes what
  happened after the incident began, not what caused it to start.

---

## The "existing_entities" Column
Shows entities already in our knowledge graph for this record (equipment, body
parts, injuries, locations, organizations, root cause categories). Your causal
annotations ADD the "why" and "how" connections between these entities.

## Assignment and Submission

- Each annotator receives approximately 100 records.
- Records 81-120 are the overlap set. Both annotators complete these
  independently, without coordinating. This is used to measure agreement.
- Work in batches of approximately 25 records. Take a break between batches.
- Estimated time: 3-5 minutes per record (approximately 5-8 hours total).
- Save your work frequently. Do not wait until the end of a batch to save.
- Return your completed CSV via the method provided by your project coordinator.
- Questions? Contact your project coordinator.

---

## Quick Reference Card

Use this table as an at-a-glance reminder of what goes in each field.

| Field | What to write | Example |
|-------|---------------|---------|
| caused_by_1_cause | Direct trigger of the incident, in your own words | "oil spill on floor" |
| caused_by_1_evidence | Exact quote from narrative | "worker slipped on oil that had leaked" |
| caused_by_1_confidence | HIGH, MEDIUM, or LOW | HIGH |
| caused_by_2_cause | Second independent direct cause (if present) | "faulty valve seal" |
| caused_by_2_evidence | Exact quote from narrative | "the valve seal had deteriorated" |
| caused_by_2_confidence | HIGH, MEDIUM, or LOW | MEDIUM |
| contributed_to_1_factor | Background condition that made incident worse or more likely | "missing safety boots" |
| contributed_to_1_evidence | Exact quote from narrative | "worker was not wearing PPE" |
| contributed_to_1_confidence | HIGH, MEDIUM, or LOW | HIGH |
| contributed_to_2_factor | Second contributing factor (if present) | "poor lighting" |
| contributed_to_2_evidence | Exact quote from narrative | "the area was poorly lit" |
| contributed_to_2_confidence | HIGH, MEDIUM, or LOW | LOW |
| led_to_1_event | First event in chain | "valve failure" |
| led_to_1_outcome | What the first event led to | "pressure buildup" |
| led_to_1_evidence | Exact quote for this step | "the valve failed, causing pressure to build" |
| led_to_1_confidence | HIGH, MEDIUM, or LOW | HIGH |
| led_to_2_event | Second event (should match led_to_1_outcome) | "pressure buildup" |
| led_to_2_outcome | What the second event led to | "pipe burst" |
| led_to_2_evidence | Exact quote for this step | "pressure buildup caused the pipe to burst" |
| led_to_2_confidence | HIGH, MEDIUM, or LOW | HIGH |
| led_to_3_event | Third event (should match led_to_2_outcome) | "pipe burst" |
| led_to_3_outcome | Final outcome of the chain | "operator struck by debris" |
| led_to_3_evidence | Exact quote for this step | "the burst pipe struck the operator" |
| led_to_3_confidence | HIGH, MEDIUM, or LOW | MEDIUM |
| annotator_notes | Free text for anything unusual or unclear | "Narrative unclear about timeline" |
