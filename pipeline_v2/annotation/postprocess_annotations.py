#!/usr/bin/env python3
"""Post-process LLM causal annotations to fix three systematic issues.

Issue 1: Re-anchor evidence spans to be exact substrings of the narrative.
Issue 2: Remove CAUSED_BY content duplicated in LED_TO_1 (shift chain up).
Issue 3: Flag LED_TO chain connectivity breaks in annotator_notes.

Usage:
    python postprocess_annotations.py
"""

import re
from pathlib import Path

import pandas as pd

INPUT_CSV = Path(__file__).parent / "annotation_llm.csv"
OUTPUT_CSV = Path(__file__).parent / "annotation_llm_postprocessed.csv"

EVIDENCE_COLS = [
    "caused_by_1_evidence",
    "caused_by_2_evidence",
    "contributed_to_1_evidence",
    "contributed_to_2_evidence",
    "led_to_1_evidence",
    "led_to_2_evidence",
    "led_to_3_evidence",
]

LED_TO_FIELDS = ["event", "outcome", "evidence", "confidence"]


def token_overlap(a: str, b: str) -> float:
    """Jaccard overlap on lowercased whitespace-split tokens, normalized by shorter span."""
    if not isinstance(a, str) or not isinstance(b, str):
        return 0.0
    ta = set(a.lower().split())
    tb = set(b.lower().split())
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / min(len(ta), len(tb))


def clean_narrative(text: str) -> str:
    """Remove _x000D_ artifacts and collapse multiple spaces."""
    text = text.replace("_x000D_", "")
    text = re.sub(r" {2,}", " ", text)
    return text


def find_raw_span(narrative_raw: str, narrative_clean: str, match_start: int, match_end: int) -> str:
    """Given a match position in narrative_clean, find the corresponding raw substring.

    We walk through both strings in parallel, mapping clean indices back to raw indices.
    """
    raw_i = 0
    clean_i = 0
    raw_start = None
    raw_end = None

    while raw_i < len(narrative_raw) and clean_i < len(narrative_clean):
        if clean_i == match_start and raw_start is None:
            raw_start = raw_i
        if clean_i == match_end:
            raw_end = raw_i
            break

        # Check if we're at a _x000D_ artifact in raw
        if raw_i + 7 <= len(narrative_raw) and narrative_raw[raw_i:raw_i + 7] == "_x000D_":
            raw_i += 7
            continue
        # Check for extra space in raw that was collapsed
        if (narrative_raw[raw_i] == " " and
                raw_i + 1 < len(narrative_raw) and narrative_raw[raw_i + 1] == " " and
                narrative_clean[clean_i] == " "):
            # Skip extra spaces in raw
            while raw_i + 1 < len(narrative_raw) and narrative_raw[raw_i + 1] == " ":
                raw_i += 1
            raw_i += 1
            clean_i += 1
            continue
        raw_i += 1
        clean_i += 1

    # Handle case where match_end is at the end of clean narrative
    if clean_i == match_end and raw_end is None:
        raw_end = raw_i

    if raw_start is not None and raw_end is not None:
        return narrative_raw[raw_start:raw_end]
    return ""


def reanchor_evidence(narrative: str, evidence: str) -> tuple[str, bool]:
    """Try to re-anchor evidence span to be an exact substring of narrative.

    Returns (new_evidence, was_fixed).
    """
    if not isinstance(evidence, str) or not evidence.strip():
        return evidence, False
    if not isinstance(narrative, str) or not narrative.strip():
        return evidence, False

    # Already an exact match
    if evidence in narrative:
        return evidence, False

    # Step 1: Try matching against cleaned narrative
    narrative_clean = clean_narrative(narrative)
    evidence_clean = clean_narrative(evidence)

    idx = narrative_clean.find(evidence_clean)
    if idx != -1:
        raw_span = find_raw_span(narrative, narrative_clean, idx, idx + len(evidence_clean))
        if raw_span and raw_span in narrative:
            return raw_span, True

    # Step 2: Ellipsis fragment matching — split on "..." and match fragments
    if "..." in evidence:
        fragments = [f.strip() for f in evidence.split("...") if f.strip()]
        if len(fragments) >= 2:
            frag_positions = []
            for frag in fragments:
                frag_clean = clean_narrative(frag)
                pos = narrative_clean.find(frag_clean)
                if pos != -1:
                    raw = find_raw_span(narrative, narrative_clean, pos, pos + len(frag_clean))
                    raw_pos = narrative.find(raw) if raw else -1
                    if raw_pos != -1:
                        frag_positions.append((raw_pos, raw_pos + len(raw)))
            if len(frag_positions) == len(fragments):
                # All fragments found — take span from first start to last end
                span_start = min(p[0] for p in frag_positions)
                span_end = max(p[1] for p in frag_positions)
                raw_span = narrative[span_start:span_end]
                if raw_span in narrative:
                    return raw_span, True

    # Step 3: Prefix/suffix anchoring — find longest matching prefix and suffix
    # Handles cases where LLM omitted middle text or joined non-adjacent sentences
    ev_clean = evidence_clean
    nc = narrative_clean

    # Find longest prefix of evidence that exists in cleaned narrative
    best_prefix_len = 0
    for length in range(len(ev_clean), 0, -1):
        prefix = ev_clean[:length]
        if prefix in nc:
            best_prefix_len = length
            break

    # Find longest suffix of evidence that exists in cleaned narrative
    best_suffix_len = 0
    for length in range(len(ev_clean), 0, -1):
        suffix = ev_clean[-length:]
        if suffix in nc:
            best_suffix_len = length
            break

    if best_prefix_len >= 20 and best_suffix_len >= 20:
        prefix_start = nc.find(ev_clean[:best_prefix_len])
        suffix_start = nc.find(ev_clean[-best_suffix_len:])
        suffix_end = suffix_start + best_suffix_len

        # Suffix must come after prefix (correct order in narrative)
        if prefix_start <= suffix_start and suffix_end > prefix_start:
            raw_span = find_raw_span(narrative, nc, prefix_start, suffix_end)
            if raw_span and raw_span in narrative:
                return raw_span, True

    # Step 4: Take the longest single contiguous fragment
    # Split evidence into sentences and find the longest one that matches
    sentences = re.split(r'(?<=[.!?])\s+', evidence_clean)
    best_sentence_span = ""
    for sent in sentences:
        sent = sent.strip()
        if len(sent) < 10:
            continue
        pos = nc.find(sent)
        if pos != -1:
            raw = find_raw_span(narrative, nc, pos, pos + len(sent))
            if raw and raw in narrative and len(raw) > len(best_sentence_span):
                best_sentence_span = raw
    if best_sentence_span:
        return best_sentence_span, True

    # Step 5: Sliding-window token overlap (original fallback)
    ev_tokens = evidence.lower().split()
    if not ev_tokens:
        return evidence, False

    # Tokenize narrative preserving character positions
    nar_token_spans = list(re.finditer(r"\S+", narrative))
    if not nar_token_spans:
        return evidence, False

    nar_tokens_lower = [m.group().lower() for m in nar_token_spans]
    window_size = len(ev_tokens)
    ev_set = set(ev_tokens)

    best_overlap = 0.0
    best_start_char = 0
    best_end_char = 0

    # Handle case where evidence has more tokens than narrative (partial match)
    if window_size > len(nar_tokens_lower):
        for i in range(len(nar_tokens_lower)):
            for w in range(1, len(nar_tokens_lower) - i + 1):
                window_set = set(nar_tokens_lower[i:i + w])
                overlap = len(ev_set & window_set) / min(len(ev_set), len(window_set))
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_start_char = nar_token_spans[i].start()
                    best_end_char = nar_token_spans[i + w - 1].end()
    else:
        for i in range(len(nar_tokens_lower) - window_size + 1):
            window_set = set(nar_tokens_lower[i:i + window_size])
            overlap = len(ev_set & window_set) / min(len(ev_set), len(window_set))
            if overlap > best_overlap:
                best_overlap = overlap
                best_start_char = nar_token_spans[i].start()
                best_end_char = nar_token_spans[i + window_size - 1].end()

    if best_overlap >= 0.7:
        raw_span = narrative[best_start_char:best_end_char]
        return raw_span, True

    return evidence, False  # Will be flagged as unresolved


def fix_issue1(df: pd.DataFrame) -> dict:
    """Re-anchor evidence spans to narratives."""
    stats = {"total_spans": 0, "reanchored": 0, "remaining_mismatches": 0}

    for idx, row in df.iterrows():
        narrative = row["narrative"]
        if not isinstance(narrative, str):
            continue

        for col in EVIDENCE_COLS:
            evidence = row[col]
            if not isinstance(evidence, str) or not evidence.strip():
                continue

            stats["total_spans"] += 1

            if evidence in narrative:
                continue  # Already exact

            new_evidence, was_fixed = reanchor_evidence(narrative, evidence)
            if was_fixed:
                df.at[idx, col] = new_evidence
                stats["reanchored"] += 1
            else:
                # Check if still mismatched
                if new_evidence not in narrative:
                    stats["remaining_mismatches"] += 1
                    # Append note
                    notes = df.at[idx, "annotator_notes"]
                    note_text = "[POSTPROCESS] Evidence span could not be re-anchored to narrative."
                    if isinstance(notes, str) and notes.strip():
                        if note_text not in notes:
                            df.at[idx, "annotator_notes"] = notes + " " + note_text
                    else:
                        df.at[idx, "annotator_notes"] = note_text

    return stats


def fix_issue2(df: pd.DataFrame) -> dict:
    """Remove CAUSED_BY content duplicated in LED_TO_1 by shifting chain up."""
    stats = {"shifted": 0, "cleared": 0}

    for idx, row in df.iterrows():
        cb1 = row.get("caused_by_1_cause", "")
        lt1 = row.get("led_to_1_event", "")

        if not isinstance(cb1, str) or not isinstance(lt1, str):
            continue
        if not cb1.strip() or not lt1.strip():
            continue

        overlap = token_overlap(cb1, lt1)
        if overlap < 0.50:
            continue

        # Check if led_to_2 exists
        lt2_event = row.get("led_to_2_event", "")
        has_lt2 = isinstance(lt2_event, str) and lt2_event.strip()

        if has_lt2:
            # Shift chain up: lt1 <- lt2, lt2 <- lt3, lt3 <- blank
            for field in LED_TO_FIELDS:
                df.at[idx, f"led_to_1_{field}"] = row.get(f"led_to_2_{field}", "")
                df.at[idx, f"led_to_2_{field}"] = row.get(f"led_to_3_{field}", "")
                df.at[idx, f"led_to_3_{field}"] = ""
            stats["shifted"] += 1
        else:
            # Only had one (redundant) LED_TO step — clear it
            for field in LED_TO_FIELDS:
                df.at[idx, f"led_to_1_{field}"] = ""
            stats["cleared"] += 1

    return stats


def fix_chain_breaks(df: pd.DataFrame) -> dict:
    """Fix LED_TO chain breaks by re-reading narratives and correcting annotations.

    Six records have chain connectivity issues. Two are false positives (valid chains
    with low token overlap due to morphological variants). Four have parallel branches
    incorrectly encoded as sequential chains — these get merged or restructured.
    """
    stats = {"false_positives_cleared": 0, "chains_restructured": 0}

    for idx, row in df.iterrows():
        rid = row["record_no"]

        if rid == 607094:
            # FALSE POSITIVE: "detonation" → "detonation generated acid projection"
            # Chain is valid. Just remove any future flag.
            stats["false_positives_cleared"] += 1

        elif rid == 13748:
            # FALSE POSITIVE: "broke" → "breaking noise detected"
            # Chain is valid (morphological variant).
            stats["false_positives_cleared"] += 1

        elif rid == 681702:
            # PARALLEL BRANCHES: fire → worker response AND fire → oxygen hose burn
            # Merge into single LED_TO: worker response + all outcomes
            df.at[idx, "led_to_1_event"] = (
                "LNG hose fire required immediate worker response"
            )
            df.at[idx, "led_to_1_outcome"] = (
                "Worker disconnected hose from manifold and crimped connection, "
                "stopping the fire; fire also caused superficial burn to parallel "
                "oxygen gas hose but no further fire observed"
            )
            df.at[idx, "led_to_1_evidence"] = (
                "Worker immediately went to the gas manifold. Disconnected the hose "
                "from the manifold and disconnected the hose from the crimped "
                "connection, and hence fire on the hose stopped. The fire caused a "
                "superficial burn on another parallel Oxygen gas hose. No further "
                "fire from the oxygen hose was observed."
            )
            df.at[idx, "led_to_1_confidence"] = "HIGH"
            for field in LED_TO_FIELDS:
                df.at[idx, f"led_to_2_{field}"] = ""
            stats["chains_restructured"] += 1

        elif rid == 8914:
            # PARALLEL CONSEQUENCES of cap removal: pack-off fell + pressure released
            # Merge into single LED_TO step
            df.at[idx, "led_to_1_event"] = (
                "Night cap removed from casing head"
            )
            df.at[idx, "led_to_1_outcome"] = (
                "Pack-off released and fell onto casing valves; trapped pressure "
                "released at employee's stomach area. No injuries."
            )
            df.at[idx, "led_to_1_evidence"] = (
                "pack off to release and fell out of casing head onto casing valves "
                "when cap was removed. Trapped pressure was released around night cap "
                "when they picked it up causing pressure release at wellhead "
                "employees stomach area. No one was hurt."
            )
            df.at[idx, "led_to_1_confidence"] = "MEDIUM"
            for field in LED_TO_FIELDS:
                df.at[idx, f"led_to_2_{field}"] = ""
            stats["chains_restructured"] += 1

        elif rid == 512639:
            # Steps 2→3 are parallel consequences (oil spill + loss of thruster).
            # Restructure step 2 outcome to bridge to step 3.
            df.at[idx, "led_to_2_outcome"] = (
                "Approximately 3 litres of T32 hydraulic oil discharged into the "
                "sea; loss of thruster capability in strong current at 50m depth"
            )
            df.at[idx, "led_to_3_event"] = (
                "Loss of thruster capability and unsafe current conditions at 50m depth"
            )
            # outcome and evidence for step 3 stay the same
            stats["chains_restructured"] += 1

        elif rid == 677837:
            # PARALLEL BRANCHES from storm: tent/vehicles AND chart recorder
            # Merge into single LED_TO step covering all storm damage
            nar = row["narrative"]
            span_start = nar.find("The shift of the tent")
            span_end = nar.find("known damages.") + len("known damages.")
            evidence_span = nar[span_start:span_end] if span_start != -1 else ""

            df.at[idx, "led_to_1_event"] = (
                "High winds caused scaffold enclosure to overturn, tent to "
                "shift/collapse, and chart recorder on production deck to fall"
            )
            df.at[idx, "led_to_1_outcome"] = (
                "Two unoccupied vehicles and tent frame damaged; chart recorder "
                "damaged. No injuries."
            )
            df.at[idx, "led_to_1_evidence"] = evidence_span
            df.at[idx, "led_to_1_confidence"] = "HIGH"
            for field in LED_TO_FIELDS:
                df.at[idx, f"led_to_2_{field}"] = ""
            stats["chains_restructured"] += 1

    return stats


def fix_issue3(df: pd.DataFrame) -> dict:
    """Flag LED_TO chain connectivity breaks."""
    stats = {"breaks_flagged": 0}

    for idx, row in df.iterrows():
        for step in [1, 2]:
            outcome_col = f"led_to_{step}_outcome"
            next_event_col = f"led_to_{step + 1}_event"

            outcome = row.get(outcome_col, "")
            next_event = row.get(next_event_col, "")

            if not isinstance(outcome, str) or not outcome.strip():
                continue
            if not isinstance(next_event, str) or not next_event.strip():
                continue

            overlap = token_overlap(outcome, next_event)
            if overlap < 0.30:
                note = (
                    f"[POSTPROCESS] LED_TO chain break detected between step {step} "
                    f"and step {step + 1}: outcome='{outcome}' vs event='{next_event}'."
                )
                notes = df.at[idx, "annotator_notes"]
                if isinstance(notes, str) and notes.strip():
                    df.at[idx, "annotator_notes"] = notes + " " + note
                else:
                    df.at[idx, "annotator_notes"] = note
                stats["breaks_flagged"] += 1

    return stats


def validate_evidence(df: pd.DataFrame) -> int:
    """Count evidence spans that are NOT exact substrings of their narrative."""
    mismatches = 0
    for _, row in df.iterrows():
        narrative = row["narrative"]
        if not isinstance(narrative, str):
            continue
        for col in EVIDENCE_COLS:
            ev = row[col]
            if not isinstance(ev, str) or not ev.strip():
                continue
            if ev not in narrative:
                mismatches += 1
    return mismatches


def validate_issue2(df: pd.DataFrame) -> int:
    """Count records where caused_by_1_cause and led_to_1_event overlap >= 50%."""
    count = 0
    for _, row in df.iterrows():
        cb1 = row.get("caused_by_1_cause", "")
        lt1 = row.get("led_to_1_event", "")
        if isinstance(cb1, str) and isinstance(lt1, str) and cb1.strip() and lt1.strip():
            if token_overlap(cb1, lt1) >= 0.50:
                count += 1
    return count


def main():
    # Read causal_density as string to preserve float precision through round-trip
    df = pd.read_csv(INPUT_CSV, dtype={"causal_density": str})
    original_cols = list(df.columns)

    # Fill NaN with empty string for annotation columns to avoid type issues
    annotation_cols = EVIDENCE_COLS + [
        "caused_by_1_cause", "caused_by_2_cause",
        "contributed_to_1_factor", "contributed_to_2_factor",
        "annotator_notes", "annotator_id",
    ]
    for step in range(1, 4):
        for field in LED_TO_FIELDS:
            annotation_cols.append(f"led_to_{step}_{field}")
    annotation_cols = list(dict.fromkeys(c for c in annotation_cols if c in df.columns))
    for col in annotation_cols:
        df[col] = df[col].fillna("")

    # Pre-fix counts
    pre_mismatches = validate_evidence(df)
    print(f"Pre-fix evidence mismatches: {pre_mismatches}")

    # Issue 1
    stats1 = fix_issue1(df)
    post_mismatches = validate_evidence(df)
    print(f"\n=== Issue 1: Evidence Re-anchoring ===")
    print(f"  {stats1['reanchored']} of {pre_mismatches} evidence spans re-anchored")
    print(f"  {post_mismatches} remaining mismatches")

    # Issue 2 — single pass only (no loop; cascading shifts wrongly clear valid chains)
    pre_overlap = validate_issue2(df)
    stats2 = fix_issue2(df)
    post_overlap = validate_issue2(df)
    print(f"\n=== Issue 2: CAUSED_BY/LED_TO Dedup ===")
    print(f"  {stats2['shifted']} records had LED_TO chain shifted")
    print(f"  {stats2['cleared']} records had LED_TO cleared entirely")
    print(f"  Overlap check: {pre_overlap} before → {post_overlap} after")

    # Issue 3a: Restructure known broken chains
    stats3a = fix_chain_breaks(df)
    print(f"\n=== Issue 3a: Chain Break Repairs ===")
    print(f"  {stats3a['false_positives_cleared']} false positives (valid chains)")
    print(f"  {stats3a['chains_restructured']} chains restructured")

    # Issue 3b: Flag any remaining chain breaks
    stats3 = fix_issue3(df)

    # Remove false-positive flags for records with valid chains
    false_positive_ids = {607094, 13748}
    removed = 0
    for idx, row in df.iterrows():
        if row["record_no"] in false_positive_ids:
            notes = str(row.get("annotator_notes", ""))
            import re as _re
            cleaned = _re.sub(
                r"\s*\[POSTPROCESS\] LED_TO chain break detected between step \d+ and step \d+:.*?\.",
                "",
                notes,
            ).strip()
            if cleaned != notes:
                df.at[idx, "annotator_notes"] = cleaned
                removed += 1

    print(f"\n=== Issue 3b: Remaining LED_TO Chain Breaks ===")
    print(f"  {stats3['breaks_flagged']} detected, {removed} false positives removed")
    print(f"  {stats3['breaks_flagged'] - removed} genuine breaks flagged")

    # Write output
    df = df[original_cols]
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\nOutput written to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
