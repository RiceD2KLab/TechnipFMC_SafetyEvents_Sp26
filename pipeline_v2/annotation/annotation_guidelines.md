# Causal Chain Annotation Guidelines

## Purpose
You are annotating causal relationships in safety incident narratives. Your
annotations will be used to train and evaluate an automated system that extracts
causal information from incident reports.

## Output Format

Each annotation is a **JSONL edge** with these fields:

```json
{
  "record_no": 574147,
  "source": "corrosion on pipe wall",
  "source_type": "Condition",
  "relation": "CAUSAL",
  "target": "pipe rupture",
  "target_type": "Event",
  "evidence": "the pipe ruptured due to corrosion",
  "annotator": "your-id"
}
```

## Relation Types (3)

### CAUSAL — One thing caused, led to, or contributed to another
The primary relation. Covers direct causes, contributing factors, and sequential
causal steps. **Direction rule: source = cause, target = effect.**

- "fire due to corrosion" → source="corrosion", target="fire"
- "worker slipped on oil" → source="oil on floor", target="worker slipped"
- "missing safety briefing contributed to incident" → source="missing safety briefing", target="incident"

Use CAUSAL for:
- Direct causes (what triggered the incident)
- Contributing factors (conditions that made it worse or more likely)
- Causal chain steps (A caused B, B caused C — each is a separate CAUSAL edge)

### PRECEDED_BY — Temporal sequence with causal link
Use when one event happened before another and the sequence matters causally,
but the earlier event did not directly cause the later one.

- source = the later event, target = the earlier event
- Example: "RTM toppled prematurely" PRECEDED_BY "scheduled toppling procedure"

### FAILED_CONTROL — A safety barrier that failed to prevent something
Use when a control, barrier, or safety measure was in place but failed.

- source = the failed control/barrier, target = what it failed to prevent
- Example: source="safety interlock", target="machine started while worker inside"

## Entity Types (9)

Classify each source and target entity using one of these types:

| Type | Description | Examples |
|------|-------------|---------|
| Incident | The overall incident event | "the accident", "near miss" |
| Event | A specific event in the causal chain | "pipe rupture", "fire", "fall" |
| Equipment | Physical equipment, tools, machinery | "crane", "valve", "scaffold" |
| Location | Places | "deck 3", "pump room" |
| Person | People or roles | "operator", "supervisor" |
| Injury | Injuries or harm | "laceration to hand", "burns" |
| Material | Substances, chemicals, materials | "hydraulic fluid", "diesel" |
| Condition | States, situations, environmental factors | "corrosion", "poor lighting", "fatigue" |
| Action | Human actions or procedures | "lifting operation", "manual handling" |

## Rules

1. Only annotate what the NARRATIVE says. Do not infer from metadata columns.
2. If no causal relationship is present, produce zero edges. This is correct
   and expected for some records.
3. Copy exact evidence spans from the narrative. Evidence must be an exact,
   unbroken substring — do not bridge non-contiguous phrases.
4. **Direction matters:** For CAUSAL edges, source is ALWAYS the cause and
   target is ALWAYS the effect. Ask: "X caused Y" — X is source, Y is target.
5. Each edge captures ONE causal link. For a chain A→B→C, create two edges:
   A→B and B→C.
6. Use the most specific entity type that applies.

### Edge Cases

**Multiple causes for the same effect?**
Create separate CAUSAL edges, each with source = a different cause and
target = the same effect.

**Contributing factors vs direct causes?**
Both use CAUSAL. The distinction is in the entity description, not the relation
type. The model does not need to distinguish — both are valid causal links.

**Hypothetical or speculative language?**
Do not annotate. "Could potentially cause" or "might lead to" are not actual
causal relationships. Only annotate what actually happened.

**Non-English text?**
Skip non-English portions entirely. Only annotate English causal relationships.

## The "existing_entities" Column
Shows entities already in our knowledge graph for this record (equipment, body
parts, injuries, locations, organizations, root cause categories). Your causal
annotations ADD the "why" and "how" connections between these entities.

## Assignment and Submission

- Each annotator receives approximately 100 records.
- Records 81-120 are the overlap set. Both annotators complete these
  independently, without coordinating. This is used to measure agreement.
- Work in batches of approximately 25 records.
- Output: one JSONL file with all your edges.
