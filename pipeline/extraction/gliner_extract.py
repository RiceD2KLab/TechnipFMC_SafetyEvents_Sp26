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
from pathlib import Path
from typing import Any

import pandas as pd
from tqdm import tqdm

from kg_schema import CHUNK_MAX_TOKENS, CHUNK_OVERLAP, GLINER_LABELS, GLINER_TYPE_MAP


def _unescape(text: str) -> str:
    """Convert literal \\n sequences to real newlines and strip _x000D_ artifacts."""
    return text.replace("\\n", "\n").replace("_x000D_", "")


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
        (r"\bTMS\b", "TMS"),   # Tubing Management System
        (r"\bBOP\b", "BOP"),   # Blowout Preventer
        (r"\bHPU\b", "HPU"),   # Hydraulic Power Unit
        (r"\bESD\b", "ESD"),   # Emergency Shutdown Device
        (r"\bROV\b", "ROV"),   # Remotely Operated Vehicle
        (r"\bPRV\b", "PRV"),   # Pressure Relief Valve
        (r"\bPPE\b", "PPE"),   # Personal Protective Equipment
        (r"\bLOTO\b", "LOTO"), # Lock Out Tag Out
        (r"\bMCM\b", "MCM"),   # Multi-Cable Mooring
        (r"\bXT\b", "XT"),     # Christmas Tree (subsea)
        (r"\bFPSO\b", "FPSO"), # Floating Production Storage Offloading
        (r"\bUTA\b", "UTA"),   # Umbilical Termination Assembly
        (r"\bSCSSV\b", "SCSSV"),  # Surface-Controlled Subsurface Safety Valve
        (r"\bPCP\b", "PCP"),   # Progressing Cavity Pump
        (r"\bVSD\b", "VSD"),   # Variable Speed Drive
        (r"\bSWL\b", "SWL"),   # Safe Working Load
        (r"\bUAV\b", "UAV"),   # Unmanned Aerial Vehicle
        (r"\bMEWP\b", "MEWP"), # Mobile Elevating Work Platform
        (r"\bPGB\b", "PGB"),   # Pipe Guide Base
        (r"\bSCBA\b", "SCBA"), # Self-Contained Breathing Apparatus
        (r"\bRCD\b", "RCD"),   # Residual Current Device
        (r"\bGFCI\b", "GFCI"), # Ground Fault Circuit Interrupter
        (r"\bJSA\b", "JSA"),   # Job Safety Analysis (often references the doc itself)
        (r"\bSDS\b", "SDS"),   # Safety Data Sheet (chemical equipment context)
        (r"\bAED\b", "AED"),   # Automated External Defibrillator
        (r"\bSWBP\b", "SWBP"), # Surface Well Bore Pressure
        (r"\bCTD\b", "CTD"),   # Coiled Tubing Drilling
        (r"\bBHA\b", "BHA"),   # Bottom Hole Assembly
        (r"\bWHP\b", "WHP"),   # Wellhead Platform
    ],
    "INJURY_TYPE": [
        (r"\bLTI\b", "LTI"),   # Lost Time Injury
        (r"\bMTC\b", "MTC"),   # Medical Treatment Case
        (r"\bFAC\b", "FAC"),   # First Aid Case
        (r"\bRWC\b", "RWC"),   # Restricted Work Case
        (r"\bTBI\b", "TBI"),   # Traumatic Brain Injury
        (r"\bRSI\b", "RSI"),   # Repetitive Strain Injury
        (r"\bNIHL\b", "NIHL"), # Noise-Induced Hearing Loss
    ],
    "BODY_PART": [
        (r"\bCNS\b", "CNS"),   # Central Nervous System
    ],
}


# Common safety equipment terms GLiNER under-extracts.  Case-insensitive,
# only added if GLiNER missed them entirely for this narrative.
DOMAIN_KEYWORDS = {
    "EQUIPMENT": [
        # --- Original set ---
        (r"\b(fire\s+extinguisher)s?\b", "fire extinguisher"),
        (r"(?<!language )\b(barrier)s?\b", "barrier"),
        (r"\b(lanyard)s?\b", "lanyard"),
        (r"\b(sling)s?\b", "sling"),
        (r"\b(harness)\b", "harness"),
        (r"\b(ladder)s?\b", "ladder"),
        (r"\b(scaffold(?:ing)?)\b", "scaffold"),
        (r"\b(grinder)s?\b", "grinder"),
        (r"\b(winch)\b", "winch"),
        (r"\b(valve)s?\b", "valve"),
        (r"\b(hose)s?\b", "hose"),
        (r"\b(reel)s?\b", "reel"),
        (r"\b(manifold)s?\b", "manifold"),
        (r"\b(mirror)s?\b", "mirror"),
        # --- Gap-fill from golden set EXTRACTION_GAP queries ---
        (r"\b(crane)s?\b", "crane"),
        (r"\b(forklift)s?\b", "forklift"),
        (r"\b(helicopter)s?\b", "helicopter"),
        (r"\b(stretcher)s?\b", "stretcher"),
        (r"\b(deck\s+winch)\b", "deck winch"),
        (r"\b(hydraulic\s+jack)s?\b", "hydraulic jack"),
        (r"\b(robot)s?\b", "robot"),
        (r"\b(drone)s?\b", "drone"),
        (r"\b(sideboom)s?\b", "Sideboom"),
        (r"\b(pipelayer)s?\b", "pipelayer"),
        (r"\b(Billy\s+Pugh)\b", "Billy Pugh"),
        # --- High-frequency offshore / industrial equipment ---
        (r"\b(chain\s+block)s?\b", "chain block"),
        (r"\b(come[-\s]?along)s?\b", "come-along"),
        (r"\b(shackle)s?\b", "shackle"),
        (r"\b(torque\s+wrench)\b", "torque wrench"),
        (r"\b(impact\s+wrench)\b", "impact wrench"),
        (r"\b(angle\s+grinder)s?\b", "angle grinder"),
        (r"\b(cutting\s+disc)s?\b", "cutting disc"),
        (r"\b(welding\s+machine)s?\b", "welding machine"),
        (r"\b(gas\s+detector)s?\b", "gas detector"),
        (r"\b(breathing\s+apparatus)\b", "breathing apparatus"),
        (r"\b(safety\s+harness)\b", "safety harness"),
        (r"\b(fall\s+arrest(?:er|or)?)\b", "fall arrestor"),
        (r"\b(life\s*(?:jacket|vest))s?\b", "life jacket"),
        (r"\b(hard\s*hat)s?\b", "hard hat"),
        (r"\b(safety\s+glass(?:es)?)\b", "safety glasses"),
        (r"\b(face\s+shield)s?\b", "face shield"),
        (r"\b(ear\s+(?:plug|muff))s?\b", "ear plug"),
        (r"\b(respirator)s?\b", "respirator"),
        (r"\b(generator)s?\b", "generator"),
        (r"\b(compressor)s?\b", "compressor"),
        (r"\b(conveyor)s?\b", "conveyor"),
        (r"\b(catwalk)s?\b", "catwalk"),
        (r"\b(gangway)s?\b", "gangway"),
        (r"\b(tugger)s?\b", "tugger"),
        (r"\b(cherry\s+picker)s?\b", "cherry picker"),
        (r"\b(boom\s+lift)s?\b", "boom lift"),
        (r"\b(scissor\s+lift)s?\b", "scissor lift"),
        (r"\b(personnel\s+basket)s?\b", "personnel basket"),
        (r"\b(rigging)\b", "rigging"),
        (r"\b(swivel)s?\b", "swivel"),
        (r"\b(flange)s?\b", "flange"),
        (r"\b(gasket)s?\b", "gasket"),
        (r"\b(hammer)s?\b", "hammer"),
        (r"\b(chisel)s?\b", "chisel"),
        (r"\b(jack\s*hammer)s?\b", "jackhammer"),
        (r"\b(nail\s+gun)s?\b", "nail gun"),
        (r"(?<!fire\s)\b(drill(?:\s+press)?)s?\b", "drill"),
        (r"\b(lathe)s?\b", "lathe"),
        (r"\b(press\s+brake)s?\b", "press brake"),
        (r"\b(guillotine)s?\b", "guillotine"),
        (r"\b(chain\s*saw)s?\b", "chainsaw"),
        (r"\b(circular\s+saw)s?\b", "circular saw"),
        (r"\b(band\s+saw)s?\b", "band saw"),
    ],
    "INJURY_TYPE": [
        (r"\b(chemical\s+burn)s?\b", "chemical burn"),
        (r"\b(heat\s*stroke)\b", "heat stroke"),
        (r"\b(heat\s+exhaustion)\b", "heat exhaustion"),
        (r"\b(frost\s*bite)\b", "frostbite"),
        (r"\b(dermatitis)\b", "dermatitis"),
        (r"\b(hearing\s+loss)\b", "hearing loss"),
        (r"\b(tinnitus)\b", "tinnitus"),
        (r"\b(concussion)s?\b", "concussion"),
        (r"\b(whiplash)\b", "whiplash"),
        (r"\b(electrocution)\b", "electrocution"),
        (r"\b(electric\s+shock)\b", "electric shock"),
        (r"\b(asphyxia(?:tion)?)\b", "asphyxiation"),
        (r"\b(smoke\s+inhalation)\b", "smoke inhalation"),
        (r"\b(carbon\s+monoxide\s+poisoning)\b", "carbon monoxide poisoning"),
        (r"\b(hydrogen\s+sulfide\s+exposure)\b", "hydrogen sulfide exposure"),
        (r"\b(foreign\s+body)\b", "foreign body"),
        (r"\b(amputation)s?\b", "amputation"),
        (r"\b(dislocation)s?\b", "dislocation"),
        (r"\b(hernia)s?\b", "hernia"),
        (r"\b(tendon(?:itis)?)\b", "tendonitis"),
        (r"\b(carpal\s+tunnel)\b", "carpal tunnel"),
    ],
    "BODY_PART": [
        (r"\b(lower\s+back)\b", "lower back"),
        (r"\b(lumbar)\b", "lumbar"),
        (r"\b(cervical\s+spine)\b", "cervical spine"),
        (r"\b(rotator\s+cuff)\b", "rotator cuff"),
        (r"\b(achilles)\b", "Achilles"),
        (r"\b(ribcage|rib\s+cage)\b", "rib cage"),
        (r"\b(collar\s*bone|clavicle)\b", "collarbone"),
        (r"\b(shin)\b", "shin"),
        (r"\b(groin)\b", "groin"),
        (r"\b(pelvis)\b", "pelvis"),
        (r"\b(abdomen)\b", "abdomen"),
        (r"\b(sternum)\b", "sternum"),
        (r"\b(vertebra[e]?)\b", "vertebra"),
        (r"\b(femur)\b", "femur"),
        (r"\b(tibia)\b", "tibia"),
        (r"\b(fibula)\b", "fibula"),
        (r"\b(meniscus)\b", "meniscus"),
        (r"\b(cornea)\b", "cornea"),
        (r"\b(retina)\b", "retina"),
        (r"\b(ear\s*drum|tympanic)\b", "eardrum"),
    ],
}


# Per-type domain stopwords mirroring `pipeline/er_prep/run_er_prep.py`.
# Filtered at extraction time so the raw parquets stay clean.  Keep this in
# sync with `DOMAIN_STOPWORDS` in run_er_prep.py.
_DOMAIN_STOPWORDS = {
    "ORGANIZATION": {
        "client", "clients", "company", "contractor", "contractors",
        "subcontractor", "subcontractors",
        "crew", "customer", "customers", "employee", "employees",
        "employer", "foreman", "operator", "operators", "personnel",
        "project", "staff", "supervisor", "team", "worker", "workers",
        "witness", "witnesses",
        "medic", "nurse", "doctor", "patient", "visitor", "driver",
        "manager", "engineer", "technician",
        "maintenance", "management", "operations", "production",
        "hse department", "hse team", "safety team", "safety department",
        "jsa", "sds", "toolbox talk",
        "ip", "we", "they", "he", "she", "it", "everyone", "someone",
        "vessel", "vehicle",
        "911", "999", "118",
    },
    "EQUIPMENT": {
        "equipment", "machine", "machinery", "tool", "tools",
        "item", "items", "object", "objects", "unit", "units",
        "device", "devices", "part", "parts", "component", "components",
    },
    "LOCATION": {
        "area", "site", "location", "place", "building", "floor",
        "ground", "workplace", "worksite", "facility",
        "room", "the area", "the site", "the location", "the place",
        "the floor", "the ground", "the building", "work area",
    },
    "INJURY_TYPE": {
        "injury", "injuries", "damage", "harm", "wound", "wounds",
    },
    "BODY_PART": {
        "body", "ip",
    },
}

# Negation phrases that GLiNER mislabels as INJURY_TYPE.  These mean the
# OPPOSITE of an injury and must be filtered.
_INJURY_NEGATION_RE = re.compile(
    r"(?:^no\s+\w+|^none\b|\bno\s+one\b|\bnobody\b|\bnothing\b"
    r"|^limited\s+or\s+no\b|^without\b)",
    re.IGNORECASE,
)


def _filter_noise(entities: list[dict]) -> list[dict]:
    """Drop entries that match per-type domain stopwords or injury negations.

    Catches GLiNER mislabels like "IP" → ORGANIZATION (Injured Person, not a
    company) and "No injuries" → INJURY_TYPE (negation, not an injury).
    """
    cleaned = []
    for e in entities:
        val = e["span"].strip().lower()
        stop_set = _DOMAIN_STOPWORDS.get(e["type"], set())
        if val in stop_set:
            continue
        if e["type"] == "INJURY_TYPE" and _INJURY_NEGATION_RE.search(e["span"]):
            continue
        cleaned.append(e)
    return cleaned


def _supplement_acronyms(entities: list[dict], narrative: str) -> list[dict]:
    """Add known domain acronyms and keywords not already found by GLiNER."""
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
    # Case-insensitive keyword supplements — use substring containment to
    # avoid duplicating "valve" when GLiNER already extracted "valves" or
    # "hydraulic valve".  Process longer canonicals first so that e.g.
    # "angle grinder" is added before "grinder", and the latter is then
    # correctly suppressed by the substring check against the former.
    existing_by_type: dict[str, set[str]] = {}
    for e in entities:
        existing_by_type.setdefault(e["type"], set()).add(e["span"].strip().upper())
    for entity_type, patterns in DOMAIN_KEYWORDS.items():
        sorted_patterns = sorted(patterns, key=lambda p: len(p[1]), reverse=True)
        for pattern, canonical in sorted_patterns:
            canon_up = canonical.upper()
            type_existing = existing_by_type.setdefault(entity_type, set())
            already = any(
                canon_up in span or (span in canon_up and len(span) >= 3)
                for span in type_existing
            )
            if not already:
                match = re.search(pattern, narrative, re.IGNORECASE)
                if match:
                    entities.append({
                        "span": match.group(1),
                        "type": entity_type,
                        "score": 0.90,
                        "start": match.start(1),
                        "end": match.end(1),
                        "source": "keyword_supplement",
                    })
                    # Update existing set so later (shorter) keywords in this
                    # type see the new supplement and avoid duplicating it.
                    type_existing.add(match.group(1).strip().upper())
    return entities


# Injury verbs — if a BODY_PART span contains one of these, the span is
# actually describing an injury (e.g. "dislocated shoulder", "fractured
# pelvis", "crushed finger") and should be reclassified as INJURY_TYPE.
_INJURY_VERB_RE = re.compile(
    r"(?:fractur|dislocat|crush|lacerat|sprain|strain|broke|broken|break"
    r"|crack|burn|punctur|torn|tear|amputat|contusion|abrasion"
    r"|bruise|bruising|swelling|hemorrhag|hematoma|wound"
    r"|cut\b|pinch|scald|electr|numb|paralys|infect|inflam"
    r"|hernia|avuls|impal|sever(?!al|e\s)|blister)",
    re.IGNORECASE,
)


def _reclassify_injury_body(entities: list[dict]) -> list[dict]:
    """Reclassify BODY_PART spans that contain injury verbs as INJURY_TYPE.

    GLiNER sometimes classifies compound injury-body terms like "dislocated
    shoulder" as BODY_PART because the body-part noun is a stronger token
    match.  This post-processing step corrects the type assignment.
    """
    for ent in entities:
        if ent["type"] == "BODY_PART" and _INJURY_VERB_RE.search(ent["span"]):
            ent["type"] = "INJURY_TYPE"
    return entities


def load_model(model_name: str = "urchade/gliner_large-v2.1"):
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

    # Fix BODY_PART spans that are really injuries (e.g. "dislocated shoulder")
    deduped = _reclassify_injury_body(deduped)

    # Drop per-type domain noise (e.g. "IP" as ORG, "No injury" as INJURY_TYPE)
    deduped = _filter_noise(deduped)

    return deduped


def run_gliner_extraction(
    df: pd.DataFrame,
    output_path: Path,
    threshold: float = 0.5,
    model_name: str = "urchade/gliner_large-v2.1",
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
