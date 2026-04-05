"""Step 2: Deterministic metadata parsing from structured text fields.

No model required — pure regex/string parsing. Runs in seconds.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pandas as pd
from tqdm import tqdm

from .gliner_extract import parse_narrative


def _unescape(text: str) -> str:
    """Convert literal \\n sequences to real newlines."""
    return text.replace("\\n", "\n")


def parse_entity_facts(raw_text: str) -> dict[str, str]:
    """Extract key-value pairs from ENTITY_FACTS section."""
    text = _unescape(raw_text)
    facts: dict[str, str] = {}
    if "ENTITY_FACTS:" not in text:
        return facts

    start = text.index("ENTITY_FACTS:") + len("ENTITY_FACTS:")
    end = text.index("META_FACTS:") if "META_FACTS:" in text else len(text)
    section = text[start:end]

    for line in section.strip().split("\n"):
        line = line.strip()
        if line.startswith("- ") and ":" in line[2:]:
            key, _, value = line[2:].partition(":")
            facts[key.strip()] = value.strip()
    return facts


def parse_meta_facts(raw_text: str) -> dict[str, str]:
    """Extract key-value pairs from META_FACTS section."""
    text = _unescape(raw_text)
    facts: dict[str, str] = {}
    if "META_FACTS:" not in text:
        return facts

    start = text.index("META_FACTS:") + len("META_FACTS:")
    section = text[start:]

    for line in section.strip().split("\n"):
        line = line.strip()
        match = re.match(r"- META\[(.+?)\]:\s*(.+)", line)
        if match:
            facts[match.group(1)] = match.group(2).strip()
    return facts


def parse_workplace_hierarchy(workplace_str: str | None) -> dict[str, str]:
    """Parse 'Site, City, Country, Region[, TechnipFMC]' into hierarchy dict.

    Returns dict with keys: site, city, country, region (whichever are present).

    NOTE: Positional parsing assumes TechnipFMC's fixed WORKPLACE format.
    With fewer than 4 parts, the most specific levels (site, then city) are
    dropped — e.g. 2 parts = "Country, Region", not "Site, City".
    """
    if not workplace_str or not workplace_str.strip():
        return {}

    parts = [p.strip() for p in workplace_str.split(",")]

    # Remove trailing "TechnipFMC" if present
    if parts and parts[-1].strip().lower() == "technipfmc":
        parts = parts[:-1]

    hierarchy: dict[str, str] = {}
    if len(parts) >= 4:
        hierarchy = {"site": parts[0], "city": parts[1], "country": parts[2], "region": parts[3]}
    elif len(parts) == 3:
        hierarchy = {"city": parts[0], "country": parts[1], "region": parts[2]}
    elif len(parts) == 2:
        hierarchy = {"country": parts[0], "region": parts[1]}
    elif len(parts) == 1:
        hierarchy = {"country": parts[0]}

    return hierarchy


def parse_severity_bin(severity_desc: str | None) -> int | None:
    """Extract leading digit from severity description as bin 1-5."""
    if not severity_desc:
        return None
    match = re.match(r"(\d)", str(severity_desc))
    return int(match.group(1)) if match else None


def parse_incident_label(raw_text: str) -> str:
    """Extract INCIDENT_LABEL from the text field."""
    text = _unescape(raw_text)
    if "INCIDENT_LABEL:" not in text:
        return ""
    start = text.index("INCIDENT_LABEL:") + len("INCIDENT_LABEL:")
    end = text.index("\n", start) if "\n" in text[start:] else len(text)
    return text[start:end].strip()


def run_metadata_parsing(
    df: pd.DataFrame,
    output_path: Path,
) -> pd.DataFrame:
    """Parse metadata from all records and save results.

    Args:
        df: DataFrame with columns RECORD_NO_LOSS_POTENTIAL, text.
        output_path: Where to save parquet output.

    Returns:
        DataFrame of parsed metadata (one row per incident).
    """
    rows: list[dict[str, Any]] = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Metadata parsing"):
        record_no = row["RECORD_NO_LOSS_POTENTIAL"]
        text = str(row.get("text", ""))

        entity_facts = parse_entity_facts(text)
        meta_facts = parse_meta_facts(text)
        workplace = parse_workplace_hierarchy(entity_facts.get("WORKPLACE", ""))
        label = parse_incident_label(text)
        narrative = parse_narrative(text)

        rows.append({
            "record_no": record_no,
            "incident_label": label,
            "narrative": narrative,
            # Properties (stored on Incident node)
            "incident_type": entity_facts.get("INCIDENT_TYPE"),
            "severity": entity_facts.get("SEVERITY_DESC"),
            "severity_bin": parse_severity_bin(entity_facts.get("SEVERITY_DESC")),
            "likelihood": entity_facts.get("LIKELIHOOD_RANGE"),
            "impact_type": entity_facts.get("IMPACT_TYPE"),
            "work_process": entity_facts.get("WORK_PROCESS"),
            "reported_date": entity_facts.get("REPORTED_DATE"),
            "event_datetime": entity_facts.get("EVENT_DATETIME"),
            "risk_color": meta_facts.get("RISK_COLOR"),
            "business_unit": meta_facts.get("GENERAL_BUSINESS_UNIT"),
            # Entities (become separate nodes)
            "client": entity_facts.get("CLIENT"),
            "case_categorization": meta_facts.get("CASE_CATEGORIZATION"),
            "operating_center": entity_facts.get("OPERATING_CENTER"),
            # Location hierarchy
            "loc_site": workplace.get("site"),
            "loc_city": workplace.get("city"),
            "loc_country": workplace.get("country"),
            "loc_region": workplace.get("region"),
        })

    metadata_df = pd.DataFrame(rows)

    # Deduplicate: source CSV has one row per incident × impact_type.
    # Keep first occurrence per record_no to avoid non-deterministic properties.
    pre_dedup = len(metadata_df)
    metadata_df = metadata_df.drop_duplicates(subset="record_no", keep="first")
    if pre_dedup != len(metadata_df):
        print(f"  Deduplicated: {pre_dedup:,} → {len(metadata_df):,} (removed {pre_dedup - len(metadata_df):,} duplicate record_nos)")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_df.to_parquet(output_path, index=False)
    print(f"Metadata parsing complete: {len(metadata_df):,} records")
    return metadata_df
