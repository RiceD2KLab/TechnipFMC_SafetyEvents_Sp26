"""Step 1: GLiNER entity extraction from narrative text.

GLiNER (~300M params) runs on CPU at ~278ms/incident.
Full dataset: ~90 min sequential, ~25 min with 4-way parallelism.

Chunking: GLiNER's model window is 384 **subword** tokens.  At full scale
(23,311 records), 4.9% of narratives exceed this limit, and 32.7% of
those long narratives contain unique entity keywords only in the
truncated tail — ~588 missed entity instances from the most detailed
investigation reports.  The extraction step splits long narratives into
overlapping chunks sized by actual subword token count (max 350, overlap
50), runs GLiNER on each chunk, then deduplicates by (normalized_span,
type), keeping the highest score.  Chunking uses the model's own
tokenizer to count subword tokens, so non-ASCII text (Portuguese,
Norwegian) that expands heavily under subword tokenization is correctly
handled.  Short narratives (<=350 subword tokens, ~95% of data) pass
through unchunked.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import pandas as pd
from tqdm import tqdm

# Add parent to path for config imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config.schema_v2 import CHUNK_MAX_TOKENS, CHUNK_OVERLAP, GLINER_LABELS, GLINER_TYPE_MAP


def _unescape(text: str) -> str:
    """Convert literal \\n sequences to real newlines."""
    return text.replace("\\n", "\n")


def parse_narrative(raw_text: str) -> str:
    """Extract NARRATIVE section from the serialized text field.

    The CSV stores literal '\\n' characters, not real newlines.
    """
    text = _unescape(raw_text)
    if "NARRATIVE:" not in text:
        return ""
    start = text.index("NARRATIVE:") + len("NARRATIVE:")
    if "ENTITY_FACTS:" in text:
        end = text.index("ENTITY_FACTS:")
    else:
        end = len(text)
    return text[start:end].strip()


def _chunk_narrative(
    text: str,
    tokenizer,
    max_tokens: int = CHUNK_MAX_TOKENS,
    overlap: int = CHUNK_OVERLAP,
) -> list[tuple[str, int]]:
    """Split a narrative into overlapping chunks sized by subword tokens.

    Uses the model's tokenizer to count subword tokens per word, ensuring
    each chunk fits within GLiNER's 384-token window.  Non-ASCII text
    (Portuguese, Norwegian) can expand 1.5-2x under subword tokenization;
    whitespace-based chunking misses this and still triggers truncation.

    Returns list of (chunk_text, char_offset) tuples.
    """
    words = text.split()
    if not words:
        return [(text, 0)]

    # Count subword tokens per whitespace word
    word_subtokens = [len(tokenizer.encode(w, add_special_tokens=False)) for w in words]

    # Fast path: total subword tokens fit in one chunk
    if sum(word_subtokens) <= max_tokens:
        return [(text, 0)]

    # Pre-compute character positions for each word in original text
    char_positions = []
    search_from = 0
    for w in words:
        idx = text.index(w, search_from)
        char_positions.append(idx)
        search_from = idx + len(w)

    # Build chunks by subword token budget
    stride_tokens = max_tokens - overlap
    chunks: list[tuple[str, int]] = []
    pos = 0  # current word index

    while pos < len(words):
        # Greedily add words until subword budget exhausted
        budget = max_tokens
        end = pos
        while end < len(words) and budget >= word_subtokens[end]:
            budget -= word_subtokens[end]
            end += 1

        # Ensure at least one word per chunk to avoid infinite loop
        if end == pos:
            end = pos + 1

        chunk_text = " ".join(words[pos:end])
        chunks.append((chunk_text, char_positions[pos]))

        if end >= len(words):
            break

        # Advance by stride (in subword tokens)
        stride_remaining = stride_tokens
        next_pos = pos
        while next_pos < end and stride_remaining > 0:
            stride_remaining -= word_subtokens[next_pos]
            next_pos += 1
        # Ensure forward progress
        pos = max(next_pos, pos + 1)

    return chunks


DOMAIN_ACRONYMS = {
    "EQUIPMENT": [
        (r"\bTMS\b", "TMS"),
        (r"\bBOP\b", "BOP"),
        (r"\bHPU\b", "HPU"),
        (r"\bESD\b", "ESD"),
        (r"\bROV\b", "ROV"),
        (r"\bPRV\b", "PRV"),
    ],
}


def _supplement_acronyms(entities: list[dict], narrative: str) -> list[dict]:
    """Add known domain acronyms not already found by GLiNER."""
    existing = {(e["span"].strip().upper(), e["type"]) for e in entities}
    for entity_type, patterns in DOMAIN_ACRONYMS.items():
        for pattern, canonical in patterns:
            if (canonical, entity_type) not in existing and re.search(pattern, narrative):
                match = re.search(pattern, narrative)
                entities.append({
                    "span": canonical,
                    "type": entity_type,
                    "score": 1.0,
                    "start": match.start(),
                    "end": match.end(),
                    "source": "acronym_supplement",
                })
    return entities


def load_model(model_name: str = "urchade/gliner_medium-v2.1"):
    """Load GLiNER model. Import is deferred so metadata-only runs skip it."""
    from gliner import GLiNER
    return GLiNER.from_pretrained(model_name)


def extract_entities(
    model,
    narrative_text: str,
    threshold: float = 0.5,
) -> list[dict[str, Any]]:
    """Run GLiNER on a single narrative with automatic chunking.

    Long narratives (>350 subword tokens) are split into overlapping
    chunks.  Entities are deduplicated across chunks by (normalized_span,
    type), keeping the highest confidence score.

    Returns list of dicts with keys: span, type, score, start, end.
    """
    if not narrative_text or not narrative_text.strip():
        return []

    tokenizer = model.data_processor.transformer_tokenizer
    chunks = _chunk_narrative(narrative_text, tokenizer)

    # Collect raw entities from all chunks
    raw: list[dict[str, Any]] = []
    for chunk_text, char_offset in chunks:
        entities = model.predict_entities(chunk_text, GLINER_LABELS, threshold=threshold)
        for ent in entities:
            raw.append({
                "span": ent["text"],
                "type": GLINER_TYPE_MAP.get(ent["label"], ent["label"].upper().replace(" ", "_")),
                "score": round(ent["score"], 4),
                "start": ent["start"] + char_offset,
                "end": ent["end"] + char_offset,
            })

    # Deduplicate: same (normalized_span, type) → keep highest score
    best: dict[tuple[str, str], dict[str, Any]] = {}
    for ent in raw:
        key = (ent["span"].strip().upper(), ent["type"])
        if key not in best or ent["score"] > best[key]["score"]:
            best[key] = ent

    deduped = list(best.values())

    # Supplement known domain acronyms missed by GLiNER
    deduped = _supplement_acronyms(deduped, narrative_text)

    return deduped


def run_gliner_extraction(
    df: pd.DataFrame,
    output_path: Path,
    threshold: float = 0.5,
    model_name: str = "urchade/gliner_medium-v2.1",
) -> pd.DataFrame:
    """Run GLiNER extraction on all records and save results.

    Args:
        df: DataFrame with columns RECORD_NO_LOSS_POTENTIAL, text.
        output_path: Where to save parquet output.
        threshold: GLiNER confidence threshold.
        model_name: HuggingFace model identifier.

    Returns:
        DataFrame of extracted entities.
    """
    print(f"Loading GLiNER model: {model_name}")
    model = load_model(model_name)
    print("Model loaded.")

    results: list[dict[str, Any]] = []
    skipped = 0

    for _, row in tqdm(df.iterrows(), total=len(df), desc="GLiNER extraction"):
        record_no = row["RECORD_NO_LOSS_POTENTIAL"]
        narrative = parse_narrative(str(row.get("text", "")))
        if not narrative:
            skipped += 1
            continue

        entities = extract_entities(model, narrative, threshold=threshold)
        for ent in entities:
            ent["record_no"] = record_no
            results.append(ent)

    entities_df = pd.DataFrame(results)
    if entities_df.empty:
        # Ensure expected columns exist even if no entities found
        entities_df = pd.DataFrame(columns=["record_no", "span", "type", "score", "start", "end"])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    entities_df.to_parquet(output_path, index=False)
    print(f"GLiNER extraction complete: {len(entities_df):,} entities from {len(df) - skipped:,} narratives ({skipped} skipped)")
    return entities_df
