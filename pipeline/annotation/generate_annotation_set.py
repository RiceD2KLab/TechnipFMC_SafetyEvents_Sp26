#!/usr/bin/env python3
"""
Causal Chain Annotation Template Generator

Produces annotation templates for evaluating Layer 2 causal extraction.
Selects 200 records stratified by category and causal language density,
pulls pre-extracted entities, and generates annotation CSVs + guidelines.

Outputs (all in pipeline/annotation/):
  - selected_records.csv
  - annotation_template.csv
  - annotation_guidelines.md
  - worked_examples.md
  - annotation_summary.md
"""

import json
import re
import textwrap
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = Path(__file__).resolve().parent.parent  # pipeline/
OUT_DIR = BASE / "annotation"
OUT_DIR.mkdir(exist_ok=True)

METADATA_PATH = BASE / "outputs" / "metadata_parsed.parquet"
ENTITIES_PATH = BASE / "er_execution" / "outputs" / "entities_post_er.parquet"
RELATIONS_PATH = BASE / "er_execution" / "outputs" / "relations_post_er.parquet"

# ---------------------------------------------------------------------------
# Step 1: Causal Language Scoring
# ---------------------------------------------------------------------------
CAUSAL_PATTERNS = [
    r"\bcaus(e|ed|ing)\b",
    r"\bresult(ed|ing|s)?\s+(in|from)\b",
    r"\bled\s+to\b",
    r"\bdue\s+to\b",
    r"\bbecause\b",
    r"\bcontribut(e|ed|ing)\s+to\b",
    r"\bfail(ed|ure|ing)\b",
    r"\bmalfunction(ed|ing)?\b",
    r"\bcollaps(e|ed|ing)\b",
    r"\brupt(ure|ured)\b",
    r"\boverload(ed)?\b",
    r"\bcorrosi(on|ve)\b",
    r"\bwear\b",
    r"\bfatigu(e|ed)\b",
    r"\bdefect(ive|s)?\b",
    r"\bimprop(er|erly)\b",
    r"\binadequat(e|ely)\b",
    r"\broot\s+cause\b",
    r"\bcontributing\s+factor\b",
    r"\bsequence\s+of\s+events\b",
    r"\bchain\s+of\b",
    r"\btriggered\b",
    r"\bprecipitat(e|ed|ing)\b",
    r"\bstemm(ed|ing)\s+from\b",
]

_compiled = [re.compile(p, re.IGNORECASE) for p in CAUSAL_PATTERNS]


def score_narrative(text: str) -> tuple[int, int, float]:
    """Count causal pattern matches and compute density."""
    if not isinstance(text, str) or len(text.strip()) < 10:
        return 0, 0, 0.0
    matches = sum(len(p.findall(text)) for p in _compiled)
    tokens = len(text.split())
    density = matches / tokens if tokens > 0 else 0.0
    return matches, tokens, density


def is_english(text: str) -> bool:
    """Reject if >30% non-ASCII characters."""
    if not isinstance(text, str) or len(text) == 0:
        return False
    non_ascii = sum(1 for c in text if ord(c) > 127)
    return (non_ascii / len(text)) < 0.30


# ---------------------------------------------------------------------------
# Step 2: Stratified Selection
# ---------------------------------------------------------------------------
STRATA = [
    ("fire_explosion", 50,
     lambda df: df["case_categorization"].str.contains(
         r"fire|explosion|flammable|explosive|chemical reaction", case=False, na=False),
     "Highest causal density (~54%). Priority for CJ-01 evaluation."),
    ("falls_slips", 40,
     lambda df: df["case_categorization"].str.contains(
         r"fall|slip|trip", case=False, na=False),
     "Largest category (3,619 records). Priority for AG-05, CJ-06."),
    ("dropped_objects", 30,
     lambda df: df["case_categorization"].str.contains(
         r"dropped object|stored energy", case=False, na=False),
     "Priority for CJ-05 (procedural -> dropped -> injury chain)."),
    ("transportation", 20,
     lambda df: df["case_categorization"].str.contains(
         r"motor vehicle|transport", case=False, na=False),
     "Priority for CJ-06 (vehicle + fall co-occurrence)."),
    ("containment_loss", 20,
     lambda df: df["case_categorization"].str.contains(
         r"hazardous|containment|spill|loss of containment", case=False, na=False),
     "Priority for MH-01 (offshore containment -> injury)."),
    ("high_causal_any", 40,
     lambda df: pd.Series(True, index=df.index),
     "Top causal density records not in other strata. Maximizes L2 signal."),
]


def select_records(df: pd.DataFrame) -> pd.DataFrame:
    """Select 200 records via stratified sampling by causal density."""
    # Pre-filter: English, 30+ tokens, at least 1 causal match
    eligible = df[
        df["narrative"].apply(is_english)
        & (df["token_count"] >= 30)
        & (df["causal_matches"] > 0)
    ].copy()
    pre_dedup = len(eligible)
    eligible = eligible.drop_duplicates(subset="record_no", keep="first")
    print(f"Eligible records (English, 30+ tokens, causal>0): {pre_dedup} ({len(eligible)} unique)")


    selected_ids: set[int] = set()
    frames = []

    for name, count, filter_fn, _reason in STRATA:
        pool = eligible[filter_fn(eligible) & ~eligible["record_no"].isin(selected_ids)]
        pool = pool.sort_values("causal_density", ascending=False)
        take = pool.head(count).copy()
        take["stratum"] = name
        frames.append(take)
        selected_ids.update(take["record_no"].tolist())
        print(f"  {name}: requested {count}, got {len(take)}")

    result = pd.concat(frames, ignore_index=True)
    print(f"Total selected: {len(result)}")
    return result


# ---------------------------------------------------------------------------
# Step 3: Pull Pre-Extracted Entities
# ---------------------------------------------------------------------------
def build_entity_lookup(entities_df: pd.DataFrame) -> dict:
    return dict(zip(
        entities_df["entity_id"],
        zip(entities_df["entity_type"], entities_df["value"]),
    ))


def get_incident_entities(record_no: int, relations_df: pd.DataFrame,
                          entity_lookup: dict) -> list[dict]:
    inc_id = f"INCIDENT::{record_no}"
    connected = relations_df[
        (relations_df["source"] == inc_id) | (relations_df["target"] == inc_id)
    ]
    entities = []
    for _, row in connected.iterrows():
        other = row["target"] if row["source"] == inc_id else row["source"]
        if other in entity_lookup:
            etype, evalue = entity_lookup[other]
            if etype != "INCIDENT":
                entities.append({
                    "entity_type": etype,
                    "value": evalue,
                    "relation": row["relation"],
                })
    return entities


# ---------------------------------------------------------------------------
# Step 4: Annotation Template Columns
# ---------------------------------------------------------------------------
ANNOTATION_COLUMNS = [
    # Pre-filled metadata
    "record_no", "stratum", "narrative", "case_categorization",
    "severity", "impact_type", "work_process",
    "causal_density", "causal_matches", "token_count",
    "existing_entities",
    # CAUSED_BY (annotator fills)
    "caused_by_1_cause", "caused_by_1_evidence", "caused_by_1_confidence",
    "caused_by_2_cause", "caused_by_2_evidence", "caused_by_2_confidence",
    # CONTRIBUTED_TO (annotator fills)
    "contributed_to_1_factor", "contributed_to_1_evidence", "contributed_to_1_confidence",
    "contributed_to_2_factor", "contributed_to_2_evidence", "contributed_to_2_confidence",
    # LED_TO (annotator fills)
    "led_to_1_event", "led_to_1_outcome", "led_to_1_evidence", "led_to_1_confidence",
    "led_to_2_event", "led_to_2_outcome", "led_to_2_evidence", "led_to_2_confidence",
    "led_to_3_event", "led_to_3_outcome", "led_to_3_evidence", "led_to_3_confidence",
    # Annotator metadata
    "annotator_notes", "annotator_id",
]


# ---------------------------------------------------------------------------
# Step 5: Annotation Guidelines
# ---------------------------------------------------------------------------
GUIDELINES = textwrap.dedent("""\
# Causal Chain Annotation Guidelines

## Purpose
You are annotating causal relationships in safety incident narratives. Your
annotations will be used as ground truth to evaluate an LLM-based causal
extraction system (Layer 2 of our knowledge graph).

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

## The "existing_entities" Column
Shows entities already in our knowledge graph for this record (equipment, body
parts, injuries, locations, organizations, root cause categories). Your causal
annotations ADD the "why" and "how" connections between these entities.

## Logistics
- ~3-5 minutes per record
- 100 records per annotator
- Records 81-120 are the overlap set — both annotators do these independently
- Annotate in batches of 25, take breaks between batches
""")


# ---------------------------------------------------------------------------
# Step 6: Worked Examples
# ---------------------------------------------------------------------------
def generate_worked_examples(selected: pd.DataFrame) -> str:
    """Pick 5 records and generate pre-filled demonstration annotations."""
    lines = [
        "# Worked Examples for Causal Chain Annotation\n",
        "These examples show how to fill out the annotation template. ",
        "Each example includes the full narrative, existing entities, ",
        "and completed annotation fields with reasoning.\n",
        "---\n",
    ]

    # 1. Simple single cause: 1 causal match, shortest narrative
    single = selected[selected["causal_matches"] == 1].sort_values("token_count")
    if len(single) == 0:
        single = selected.sort_values("causal_matches").head(1)

    # 2. Multi-factor: 2-3 causal matches
    multi = selected[selected["causal_matches"].between(2, 3)].sort_values(
        "causal_density", ascending=False)

    # 3. Causal chain: fire_explosion with 4+ matches
    chain = selected[
        (selected["stratum"] == "fire_explosion") & (selected["causal_matches"] >= 4)
    ].sort_values("causal_density", ascending=False)
    if len(chain) == 0:
        chain = selected[selected["causal_matches"] >= 4].sort_values(
            "causal_density", ascending=False)

    # 4. No causal language candidate: lowest causal_matches among selected
    no_causal = selected.sort_values(["causal_matches", "causal_density"]).head(5)

    # 5. Ambiguous: medium density, falls/slips
    ambig = selected[selected["stratum"] == "falls_slips"].sort_values("causal_density")
    if len(ambig) == 0:
        ambig = selected.sort_values("causal_density")

    examples = [
        ("Example 1: Simple Single Cause", single.iloc[0] if len(single) > 0 else None,
         "simple_single_cause"),
        ("Example 2: Multi-Factor", multi.iloc[0] if len(multi) > 0 else None,
         "multi_factor"),
        ("Example 3: Causal Chain", chain.iloc[0] if len(chain) > 0 else None,
         "causal_chain"),
        ("Example 4: No Causal Relationship", no_causal.iloc[0] if len(no_causal) > 0 else None,
         "no_causal"),
        ("Example 5: Ambiguous", ambig.iloc[0] if len(ambig) > 0 else None,
         "ambiguous"),
    ]

    for title, row, etype in examples:
        if row is None:
            continue
        lines.append(f"\n## {title}\n")
        lines.append(f"**Record:** {row['record_no']}  ")
        lines.append(f"**Stratum:** {row['stratum']}  ")
        lines.append(f"**Causal Matches:** {row['causal_matches']}  ")
        lines.append(f"**Causal Density:** {row['causal_density']:.4f}  ")
        lines.append(f"**Category:** {row['case_categorization']}\n")
        lines.append(f"### Narrative\n")
        narrative = str(row["narrative"])
        # Truncate very long narratives in examples
        if len(narrative) > 2000:
            narrative = narrative[:2000] + "... [truncated]"
        lines.append(f"> {narrative}\n")

        # Existing entities
        entities_str = row.get("existing_entities", "[]")
        try:
            entities = json.loads(entities_str) if isinstance(entities_str, str) else entities_str
        except (json.JSONDecodeError, TypeError):
            entities = []
        if entities:
            lines.append("### Existing Entities\n")
            lines.append("| Type | Value | Relation |")
            lines.append("|------|-------|----------|")
            for ent in entities[:15]:
                lines.append(
                    f"| {ent.get('entity_type', '')} "
                    f"| {ent.get('value', '')} "
                    f"| {ent.get('relation', '')} |"
                )
            lines.append("")

        # Annotation guidance per type
        lines.append("### Annotation\n")
        if etype == "simple_single_cause":
            lines.append(
                "This record has a single, clear causal indicator. "
                "Fill in `caused_by_1` only. Leave all other annotation fields blank.\n"
            )
            lines.append("| Field | Value |")
            lines.append("|-------|-------|")
            lines.append("| caused_by_1_cause | *(identify the cause from the narrative)* |")
            lines.append("| caused_by_1_evidence | *(exact quote containing the causal language)* |")
            lines.append("| caused_by_1_confidence | high |")
            lines.append("| *(all other fields)* | *(blank)* |")
        elif etype == "multi_factor":
            lines.append(
                "This record has multiple causal indicators suggesting both a primary cause "
                "and a contributing factor.\n"
            )
            lines.append("| Field | Value |")
            lines.append("|-------|-------|")
            lines.append("| caused_by_1_cause | *(primary cause)* |")
            lines.append("| caused_by_1_evidence | *(exact quote)* |")
            lines.append("| caused_by_1_confidence | high |")
            lines.append("| contributed_to_1_factor | *(contributing factor)* |")
            lines.append("| contributed_to_1_evidence | *(exact quote)* |")
            lines.append("| contributed_to_1_confidence | medium |")
        elif etype == "causal_chain":
            lines.append(
                "This record has a rich causal sequence with multiple steps. "
                "Use the LED_TO fields to capture the chain.\n"
            )
            lines.append("| Field | Value |")
            lines.append("|-------|-------|")
            lines.append("| caused_by_1_cause | *(root cause)* |")
            lines.append("| caused_by_1_evidence | *(exact quote)* |")
            lines.append("| caused_by_1_confidence | high |")
            lines.append("| led_to_1_event | *(first event in chain)* |")
            lines.append("| led_to_1_outcome | *(what it led to)* |")
            lines.append("| led_to_1_evidence | *(exact quote)* |")
            lines.append("| led_to_1_confidence | high |")
            lines.append("| led_to_2_event | *(second event)* |")
            lines.append("| led_to_2_outcome | *(final outcome)* |")
            lines.append("| led_to_2_evidence | *(exact quote)* |")
            lines.append("| led_to_2_confidence | high |")
        elif etype == "no_causal":
            lines.append(
                "This record was selected due to having causal keyword matches, but "
                "on close reading the causal language is incidental (e.g., 'wear' used "
                "in non-causal context). **It is correct to leave all annotation fields blank.**\n"
            )
            lines.append("| Field | Value |")
            lines.append("|-------|-------|")
            lines.append("| *(all annotation fields)* | *(blank)* |")
            lines.append("| annotator_notes | No causal relationship identifiable in narrative |")
        elif etype == "ambiguous":
            lines.append(
                "This record describes an incident but the cause is unclear or only "
                "implied. Use LOW or MEDIUM confidence.\n"
            )
            lines.append("| Field | Value |")
            lines.append("|-------|-------|")
            lines.append("| caused_by_1_cause | *(best interpretation)* |")
            lines.append("| caused_by_1_evidence | *(relevant passage)* |")
            lines.append("| caused_by_1_confidence | low |")
            lines.append("| annotator_notes | Cause ambiguous — [explain reasoning] |")

        lines.append("")
        lines.append("---\n")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Step 7: Summary Statistics
# ---------------------------------------------------------------------------
def generate_summary(selected: pd.DataFrame, total_eligible: int) -> str:
    strat_stats = selected.groupby("stratum").agg(
        count=("record_no", "count"),
        mean_density=("causal_density", "mean"),
        mean_tokens=("token_count", "mean"),
    )
    # Reorder to match STRATA definition
    strat_order = [name for name, _, _, _ in STRATA]
    strat_stats = strat_stats.reindex(strat_order)

    table_rows = []
    for name in strat_order:
        if name in strat_stats.index:
            row = strat_stats.loc[name]
            table_rows.append(
                f"| {name} | {int(row['count'])} | {row['mean_density']:.4f} | {row['mean_tokens']:.0f} |"
            )

    matches = selected["causal_matches"]
    five_plus = int((matches >= 5).sum())

    return textwrap.dedent(f"""\
# Annotation Set Summary

## Selection
- Total records with English narrative + 30+ tokens + causal match: {total_eligible}
- Total selected: {len(selected)}

## Distribution by Stratum
| Stratum | Count | Mean Causal Density | Mean Tokens |
|---------|------:|-------------------:|------------:|
{chr(10).join(table_rows)}

## Causal Language Statistics
- Mean causal matches per record: {matches.mean():.1f}
- Median: {matches.median():.0f}
- Records with 5+ matches: {five_plus}

## Evaluation Plan
After annotation complete:
1. Inter-annotator agreement on 40-record overlap (Cohen's kappa)
2. Run Qwen3-30B-A3B on same 200 records
3. Compare: precision (LLM edges in annotation), recall (annotation edges found by LLM)
4. Evidence span overlap (do LLM spans match annotator spans)
5. Gate 3 thresholds: 70% precision, 50% recall
""")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Loading data...")
    metadata_df = pd.read_parquet(METADATA_PATH)
    entities_df = pd.read_parquet(ENTITIES_PATH)
    relations_df = pd.read_parquet(RELATIONS_PATH)

    # Step 1: Score causal density
    print("Scoring causal language density...")
    scores = metadata_df["narrative"].apply(lambda x: pd.Series(score_narrative(str(x))))
    scores.columns = ["causal_matches", "token_count", "causal_density"]
    metadata_df = pd.concat([metadata_df, scores], axis=1)

    # Step 2: Stratified selection
    print("Selecting records...")
    selected = select_records(metadata_df)

    # Count eligible before selection (for summary)
    total_eligible = int((
        metadata_df["narrative"].apply(is_english)
        & (metadata_df["token_count"] >= 30)
        & (metadata_df["causal_matches"] > 0)
    ).sum())

    # Step 3: Pull pre-extracted entities
    print("Looking up existing entities...")
    entity_lookup = build_entity_lookup(entities_df)
    selected["existing_entities"] = selected["record_no"].apply(
        lambda rn: json.dumps(get_incident_entities(rn, relations_df, entity_lookup))
    )

    # Step 4a: Save selected_records.csv
    select_cols = [
        "record_no", "narrative", "case_categorization", "severity",
        "impact_type", "work_process", "causal_density", "causal_matches",
        "token_count", "stratum",
    ]
    selected[select_cols].to_csv(OUT_DIR / "selected_records.csv", index=False)
    print(f"Wrote selected_records.csv ({len(selected)} rows)")

    # Step 4b: Save annotation_template.csv
    template = selected.reindex(columns=ANNOTATION_COLUMNS)
    template.to_csv(OUT_DIR / "annotation_template.csv", index=False)
    print(f"Wrote annotation_template.csv ({len(template)} rows, {len(ANNOTATION_COLUMNS)} cols)")

    # Step 5: Guidelines
    (OUT_DIR / "annotation_guidelines.md").write_text(GUIDELINES)
    print("Wrote annotation_guidelines.md")

    # Step 6: Worked examples
    examples_md = generate_worked_examples(selected)
    (OUT_DIR / "worked_examples.md").write_text(examples_md)
    print("Wrote worked_examples.md")

    # Step 7: Summary
    summary_md = generate_summary(selected, total_eligible)
    (OUT_DIR / "annotation_summary.md").write_text(summary_md)
    print("Wrote annotation_summary.md")

    print("\nDone! All outputs in:", OUT_DIR)


if __name__ == "__main__":
    main()
