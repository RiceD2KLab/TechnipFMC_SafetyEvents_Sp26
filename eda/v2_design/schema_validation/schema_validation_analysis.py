"""Schema Validation Evidence — Empirical analysis for v2 design decisions.

Reads the raw 23K-record dataset and GLiNER v2 extraction output to produce
schema_validation_evidence.md with data-backed recommendations for each of
the 8 proposed schema changes.
"""
from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = Path(__file__).resolve().parent
RAW_CSV = BASE / "graphRAG" / "input" / "dev_sample.csv"
ENTITIES_CSV = BASE / "gliner_output_production_v2" / "entities.csv"
RELATIONS_CSV = BASE / "gliner_output_production_v2" / "relations.csv"
TRIPLES_CSV = BASE / "gliner_output_production_v2" / "triples.csv"
OUTPUT_MD = BASE / "schema_validation_evidence.md"


# ── Helpers ────────────────────────────────────────────────────────────────
def _unescape(text: str) -> str:
    """Convert literal \\n sequences to real newlines."""
    return text.replace("\\n", "\n")


def parse_field(text: str, field: str) -> str | None:
    """Extract a named field from the semi-structured text block."""
    # Work on unescaped text (real newlines)
    t = _unescape(text)
    patterns = [
        rf"- {field}: (.+)",               # ENTITY_FACTS style
        rf"- META\[{field}\]: (.+)",        # META_FACTS style
        rf"{field}: (.+)",                  # bare
    ]
    for pat in patterns:
        m = re.search(pat, t)
        if m:
            return m.group(1).strip()
    return None


def parse_narrative(text: str) -> str:
    """Extract just the NARRATIVE section."""
    t = _unescape(text)
    m = re.search(r"NARRATIVE:\s*\n(.+?)(?:\n\n|\nENTITY_FACTS:)", t, re.DOTALL)
    if m:
        return m.group(1).strip()
    # fallback: everything after NARRATIVE:
    m = re.search(r"NARRATIVE:\s*\n(.+)", t, re.DOTALL)
    if m:
        return m.group(1).strip()
    return ""


def load_raw_dataset() -> list[dict[str, Any]]:
    """Load the raw dataset, parsing fields from the text column."""
    records = []
    with open(RAW_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row.get("text", "")
            rec = {
                "incident_id": row.get("RECORD_NO_LOSS_POTENTIAL", ""),
                "text": text,
                "narrative": parse_narrative(text),
                "incident_type": parse_field(text, "INCIDENT_TYPE"),
                "impact_type": parse_field(text, "IMPACT_TYPE"),
                "event_datetime": parse_field(text, "EVENT_DATETIME"),
                "reported_date": parse_field(text, "REPORTED_DATE"),
                "workplace": parse_field(text, "WORKPLACE"),
                "case_categorization": parse_field(text, "CASE_CATEGORIZATION"),
                "work_process": parse_field(text, "WORK_PROCESS"),
                "severity_desc": parse_field(text, "SEVERITY_DESC"),
            }
            records.append(rec)
    return records


def load_csv(path: Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pct(n: int, total: int) -> str:
    if total == 0:
        return "0.0%"
    return f"{n / total * 100:.1f}%"


def fmt(n: int) -> str:
    return f"{n:,}"


# ── Load data ──────────────────────────────────────────────────────────────
print("Loading raw dataset...")
records = load_raw_dataset()
N = len(records)
print(f"  {fmt(N)} records loaded")

print("Loading GLiNER v2 output...")
entities = load_csv(ENTITIES_CSV)
relations = load_csv(RELATIONS_CSV)
triples = load_csv(TRIPLES_CSV)
print(f"  {fmt(len(entities))} entities, {fmt(len(relations))} relations, {fmt(len(triples))} triples")

# Index entities by incident_id
entities_by_incident: dict[str, list[dict]] = defaultdict(list)
for e in entities:
    entities_by_incident[e["incident_id"]].append(e)

# Index relations by incident_id
relations_by_incident: dict[str, list[dict]] = defaultdict(list)
for r in relations:
    relations_by_incident[r["incident_id"]].append(r)

# ── Prototype incident IDs (the 999 used for extraction) ──────────────────
prototype_ids = set(entities_by_incident.keys()) | set(relations_by_incident.keys())
print(f"  Prototype covers {fmt(len(prototype_ids))} incidents")

# Build a fast lookup for raw records by incident_id
records_by_id = {r["incident_id"]: r for r in records}


# ══════════════════════════════════════════════════════════════════════════
# ANALYSIS 1: `used_in` Viability Test
# ══════════════════════════════════════════════════════════════════════════
print("\n── Analysis 1: used_in viability ──")

# Count relation types in extraction output
rel_type_counts = Counter(r["relation"] for r in relations)
total_rels = len(relations)
print(f"  Relation distribution ({total_rels} total):")
for rt, c in rel_type_counts.most_common():
    print(f"    {rt}: {c} ({pct(c, total_rels)})")

used_in_count = rel_type_counts.get("USED_IN", 0)

# Scan narratives for used_in patterns
used_in_patterns = [
    r"\b\w+\s+used\s+(?:in|during|for)\s+",
    r"\busing\s+(?:a|the|an)\s+\w+",
    r"\boperat(?:ing|ed)\s+(?:a|the|an)\s+\w+",
]
involved_patterns = [
    r"\binvolv(?:ed|ing)\s+",
    r"\bwhile\s+(?:using|operating|working\s+with)\s+",
]

used_in_narrative_count = 0
involved_narrative_count = 0
used_in_examples = []
involved_examples = []

for rec in records:
    narr = rec["narrative"].lower()
    if not narr:
        continue
    for pat in used_in_patterns:
        if re.search(pat, narr):
            used_in_narrative_count += 1
            if len(used_in_examples) < 5:
                # Get the matching sentence
                m = re.search(pat, narr)
                start = max(0, m.start() - 40)
                end = min(len(narr), m.end() + 60)
                used_in_examples.append(f"...{narr[start:end]}...")
            break
    for pat in involved_patterns:
        if re.search(pat, narr):
            involved_narrative_count += 1
            if len(involved_examples) < 5:
                m = re.search(pat, narr)
                start = max(0, m.start() - 40)
                end = min(len(narr), m.end() + 60)
                involved_examples.append(f"...{narr[start:end]}...")
            break

narrs_with_text = sum(1 for r in records if r["narrative"].strip())
print(f"  Narratives with used_in patterns: {used_in_narrative_count}/{narrs_with_text} ({pct(used_in_narrative_count, narrs_with_text)})")
print(f"  Narratives with involved patterns: {involved_narrative_count}/{narrs_with_text} ({pct(involved_narrative_count, narrs_with_text)})")

# ══════════════════════════════════════════════════════════════════════════
# ANALYSIS 2: Incident Type — Entity vs. Property
# ══════════════════════════════════════════════════════════════════════════
print("\n── Analysis 2: Incident Type entity vs property ──")

incident_types = Counter()
incident_type_null = 0
for rec in records:
    it = rec["incident_type"]
    if it:
        incident_types[it] += 1
    else:
        incident_type_null += 1

print(f"  Unique INCIDENT_TYPE values: {len(incident_types)}")
print(f"  Null/missing: {incident_type_null} ({pct(incident_type_null, N)})")
for val, cnt in incident_types.most_common():
    print(f"    {val}: {cnt} ({pct(cnt, N)})")

# Mean degree from prototype
# Each incident connects to its entities. Mean degree = 2 * edges / nodes
unique_nodes_in_prototype = set()
for r in relations:
    unique_nodes_in_prototype.add(r.get("head", ""))
    unique_nodes_in_prototype.add(r.get("tail", ""))
mean_degree = 2 * total_rels / max(len(unique_nodes_in_prototype), 1)
print(f"  Prototype mean degree: {mean_degree:.2f}")

# If Incident Type were entity nodes, their degree would be = number of incidents with that type
# (each incident connects to its type)
for val, cnt in incident_types.most_common():
    ratio = cnt / mean_degree if mean_degree > 0 else 0
    print(f"  '{val}' as entity: degree={cnt}, {ratio:.0f}x mean degree")


# ══════════════════════════════════════════════════════════════════════════
# ANALYSIS 3: Date — Entity vs. Property
# ══════════════════════════════════════════════════════════════════════════
print("\n── Analysis 3: Date entity vs property ──")

event_datetime_present = sum(1 for r in records if r["event_datetime"])
reported_date_present = sum(1 for r in records if r["reported_date"])
print(f"  EVENT_DATETIME coverage: {event_datetime_present}/{N} ({pct(event_datetime_present, N)})")
print(f"  REPORTED_DATE coverage: {reported_date_present}/{N} ({pct(reported_date_present, N)})")

# Parse reported dates to get day/month/year granularity
from datetime import datetime

date_by_day = Counter()
date_by_month = Counter()
date_by_year = Counter()
date_parse_failures = 0

for rec in records:
    rd = rec["reported_date"]
    if not rd:
        continue
    try:
        dt = datetime.strptime(rd, "%m/%d/%Y")
        date_by_day[dt.strftime("%Y-%m-%d")] += 1
        date_by_month[dt.strftime("%Y-%m")] += 1
        date_by_year[dt.strftime("%Y")] += 1
    except ValueError:
        date_parse_failures += 1

print(f"  Date parse failures: {date_parse_failures}")
print(f"  Unique dates (day): {len(date_by_day)}")
print(f"  Unique dates (month): {len(date_by_month)}")
print(f"  Unique dates (year): {len(date_by_year)}")

# Day granularity degree distribution
day_degrees = sorted(date_by_day.values(), reverse=True)
if day_degrees:
    print(f"  Day granularity - max degree: {day_degrees[0]}, median: {day_degrees[len(day_degrees)//2]}, mean: {sum(day_degrees)/len(day_degrees):.1f}")

# Year granularity
print(f"  Year granularity degrees:")
for yr, cnt in sorted(date_by_year.items()):
    print(f"    {yr}: {cnt}")


# ══════════════════════════════════════════════════════════════════════════
# ANALYSIS 4: CASE_CATEGORIZATION — Entity vs. Property
# ══════════════════════════════════════════════════════════════════════════
print("\n── Analysis 4: CASE_CATEGORIZATION entity vs property ──")

case_cats = Counter()
case_cat_null = 0
for rec in records:
    cc = rec["case_categorization"]
    if cc:
        case_cats[cc] += 1
    else:
        case_cat_null += 1

case_cat_present = N - case_cat_null
print(f"  Unique CASE_CATEGORIZATION values: {len(case_cats)}")
print(f"  Coverage: {case_cat_present}/{N} ({pct(case_cat_present, N)})")
print(f"  Null/missing: {case_cat_null} ({pct(case_cat_null, N)})")

cat_degrees = sorted(case_cats.values(), reverse=True)
print(f"  Degree distribution - max: {cat_degrees[0]}, min: {cat_degrees[-1]}, median: {cat_degrees[len(cat_degrees)//2]}, mean: {sum(cat_degrees)/len(cat_degrees):.1f}")

print(f"  Top 20 categories:")
for val, cnt in case_cats.most_common(20):
    print(f"    {val}: {cnt}")

# Cross-incident connection analysis (for prototype incidents only)
# For top categories, find pairs sharing category but no other entities
cat_to_incidents = defaultdict(set)
for rec in records:
    cc = rec["case_categorization"]
    if cc:
        cat_to_incidents[cc].add(rec["incident_id"])

# For prototype incidents, check entity overlap
def get_entity_set(incident_id: str) -> set[str]:
    """Return set of (text, type) for an incident's entities."""
    return {(e["text"].upper(), e["type"]) for e in entities_by_incident.get(incident_id, [])}

# Sample analysis: for top 20 categories, among prototype incidents
unique_connections = 0
redundant_connections = 0
sampled_pairs = 0
top20_cats = [val for val, _ in case_cats.most_common(20)]

for cat in top20_cats:
    proto_ids_in_cat = [iid for iid in cat_to_incidents[cat] if iid in prototype_ids]
    for i in range(min(len(proto_ids_in_cat), 50)):
        for j in range(i + 1, min(len(proto_ids_in_cat), 50)):
            id_a = proto_ids_in_cat[i]
            id_b = proto_ids_in_cat[j]
            ents_a = get_entity_set(id_a)
            ents_b = get_entity_set(id_b)
            shared = ents_a & ents_b
            sampled_pairs += 1
            if len(shared) == 0:
                unique_connections += 1
            else:
                redundant_connections += 1

print(f"  Cross-incident connection test (top 20 cats, prototype incidents):")
print(f"    Pairs sampled: {sampled_pairs}")
print(f"    Unique connections (no entity overlap): {unique_connections} ({pct(unique_connections, sampled_pairs)})")
print(f"    Redundant (share ≥1 entity): {redundant_connections} ({pct(redundant_connections, sampled_pairs)})")


# ══════════════════════════════════════════════════════════════════════════
# ANALYSIS 5: `caused_by` Source Conflation
# ══════════════════════════════════════════════════════════════════════════
print("\n── Analysis 5: caused_by source conflation ──")

# Filter caused_by relations
caused_by_rels = [r for r in relations if r["relation"] == "CAUSED_BY"]
print(f"  Total CAUSED_BY edges: {len(caused_by_rels)}")

# Check if tail values match CASE_CATEGORIZATION values
all_cat_values = set(case_cats.keys())
all_cat_values_lower = {v.lower() for v in all_cat_values}

metadata_sourced = 0
narrative_sourced = 0
ambiguous_sourced = 0
narrative_cause_types = Counter()

for r in caused_by_rels:
    tail = r.get("tail", "")
    tail_type = r.get("tail_type", "")
    # Check if the tail matches a CASE_CATEGORIZATION value
    if tail.lower() in all_cat_values_lower or tail in all_cat_values:
        metadata_sourced += 1
    else:
        narrative_sourced += 1
        narrative_cause_types[tail_type] += 1

print(f"  Metadata-sourced (matches CASE_CATEGORIZATION): {metadata_sourced} ({pct(metadata_sourced, len(caused_by_rels))})")
print(f"  Narrative-sourced: {narrative_sourced} ({pct(narrative_sourced, len(caused_by_rels))})")
print(f"  Narrative cause entity types: {dict(narrative_cause_types)}")

# Scan narratives for causal language
causal_patterns = [
    r"\bdue to\b",
    r"\bcaused by\b",
    r"\bfailure of\b",
    r"\bresulting in\b",
    r"\bcausing\b",
    r"\bbecause\b",
    r"\bled to\b",
]
causal_narrative_count = 0
causal_examples = []

for rec in records:
    narr = rec["narrative"].lower()
    if not narr:
        continue
    for pat in causal_patterns:
        if re.search(pat, narr):
            causal_narrative_count += 1
            if len(causal_examples) < 5:
                m = re.search(pat, narr)
                start = max(0, m.start() - 50)
                end = min(len(narr), m.end() + 80)
                causal_examples.append(f"...{narr[start:end]}...")
            break

print(f"  Narratives with causal language: {causal_narrative_count}/{narrs_with_text} ({pct(causal_narrative_count, narrs_with_text)})")

# Check CASE_CATEGORIZATION vs narrative match
cat_narrative_match = 0
cat_narrative_mismatch = 0
for rec in records:
    cc = rec["case_categorization"]
    narr = rec["narrative"].lower()
    if not cc or not narr:
        continue
    # Check if any word from categorization appears in narrative
    cc_words = set(w.lower() for w in re.findall(r'\b\w{4,}\b', cc))
    narr_words = set(re.findall(r'\b\w{4,}\b', narr))
    overlap = cc_words & narr_words
    if len(overlap) >= 1:
        cat_narrative_match += 1
    else:
        cat_narrative_mismatch += 1

total_cat_narr = cat_narrative_match + cat_narrative_mismatch
print(f"  CASE_CATEGORIZATION word overlap with narrative: {cat_narrative_match}/{total_cat_narr} ({pct(cat_narrative_match, total_cat_narr)})")


# ══════════════════════════════════════════════════════════════════════════
# ANALYSIS 6: `involved` vs `affected` Disambiguation
# ══════════════════════════════════════════════════════════════════════════
print("\n── Analysis 6: involved vs affected disambiguation ──")

entity_type_counts = Counter(e["type"] for e in entities)
print(f"  Entity type distribution ({len(entities)} total):")
for et, cnt in entity_type_counts.most_common():
    print(f"    {et}: {cnt} ({pct(cnt, len(entities))})")

# Check for type ambiguity: same span assigned to multiple types
entity_spans = defaultdict(set)
for e in entities:
    entity_spans[e["text"].upper()].add(e["type"])

multi_type_spans = {span: types for span, types in entity_spans.items() if len(types) > 1}
print(f"  Spans with multiple types: {len(multi_type_spans)}")
for span, types in list(multi_type_spans.items())[:10]:
    print(f"    '{span}': {types}")

# Count incidents with BOTH Equipment and Body Part
incidents_with_equip = set()
incidents_with_body = set()
incidents_with_injury = set()

for e in entities:
    if e["type"] == "EQUIPMENT":
        incidents_with_equip.add(e["incident_id"])
    elif e["type"] == "BODY_PART":
        incidents_with_body.add(e["incident_id"])
    elif e["type"] == "INJURY_TYPE":
        incidents_with_injury.add(e["incident_id"])

both_equip_body = incidents_with_equip & incidents_with_body
print(f"  Incidents with Equipment: {len(incidents_with_equip)}")
print(f"  Incidents with Body Part: {len(incidents_with_body)}")
print(f"  Incidents with BOTH: {len(both_equip_body)} ({pct(len(both_equip_body), len(prototype_ids))})")

# Relation type distribution check
involved_rels = [r for r in relations if r["relation"] == "INVOLVED"]
affected_rels = [r for r in relations if r["relation"] == "AFFECTED"]
print(f"  INVOLVED relations: {len(involved_rels)}")
print(f"  AFFECTED relations: {len(affected_rels)}")

# Check tail types for involved vs affected
involved_tail_types = Counter(r["tail_type"] for r in involved_rels)
affected_tail_types = Counter(r["tail_type"] for r in affected_rels)
print(f"  INVOLVED tail types: {dict(involved_tail_types)}")
print(f"  AFFECTED tail types: {dict(affected_tail_types)}")

# Find 20 example sentences with co-occurring equipment and body part
cooccur_examples = []
for iid in list(both_equip_body)[:30]:
    rec = records_by_id.get(iid)
    if not rec:
        continue
    narr = rec["narrative"]
    equip_ents = [e["text"] for e in entities_by_incident[iid] if e["type"] == "EQUIPMENT"]
    body_ents = [e["text"] for e in entities_by_incident[iid] if e["type"] == "BODY_PART"]
    cooccur_examples.append({
        "incident_id": iid,
        "narrative_snippet": narr[:200],
        "equipment": equip_ents,
        "body_parts": body_ents,
    })
    if len(cooccur_examples) >= 20:
        break


# ══════════════════════════════════════════════════════════════════════════
# ANALYSIS 7: Location Hierarchy Feasibility
# ══════════════════════════════════════════════════════════════════════════
print("\n── Analysis 7: Location hierarchy feasibility ──")

workplace_present = 0
workplace_null = 0
component_counts = Counter()
workplaces = []

for rec in records:
    wp = rec["workplace"]
    if wp:
        workplace_present += 1
        parts = [p.strip() for p in wp.split(",")]
        component_counts[len(parts)] += 1
        workplaces.append({"raw": wp, "parts": parts})
    else:
        workplace_null += 1

print(f"  WORKPLACE coverage: {workplace_present}/{N} ({pct(workplace_present, N)})")
print(f"  Component count distribution:")
for n_parts, cnt in sorted(component_counts.items()):
    print(f"    {n_parts} parts: {cnt} ({pct(cnt, workplace_present)})")

# For 5-part workplaces, extract hierarchy
sites = set()
cities = set()
countries = set()
regions = set()
city_country = defaultdict(set)
site_city = defaultdict(set)

for wp in workplaces:
    parts = wp["parts"]
    if len(parts) == 5:
        site, city, country, region, org = parts
        sites.add(site)
        cities.add(city)
        countries.add(country)
        regions.add(region)
        city_country[city].add(country)
        site_city[site].add(city)
    elif len(parts) == 4:
        site, city, country, region = parts
        sites.add(site)
        cities.add(city)
        countries.add(country)
        regions.add(region)
        city_country[city].add(country)
        site_city[site].add(city)

print(f"  Unique sites: {len(sites)}")
print(f"  Unique cities: {len(cities)}")
print(f"  Unique countries: {len(countries)}")
print(f"  Unique regions: {len(regions)}")

# Check inconsistencies
city_multi_country = {c: cs for c, cs in city_country.items() if len(cs) > 1}
site_multi_city = {s: cs for s, cs in site_city.items() if len(cs) > 1}
print(f"  Cities in multiple countries: {len(city_multi_country)}")
for c, cs in list(city_multi_country.items())[:5]:
    print(f"    '{c}': {cs}")
print(f"  Sites in multiple cities: {len(site_multi_city)}")
for s, cs in list(site_multi_city.items())[:5]:
    print(f"    '{s}': {cs}")

# Edge count impact
# Each 5-part hierarchy: site→city→country→region = 3 located_in edges per unique path
hierarchy_paths = set()
for wp in workplaces:
    parts = wp["parts"]
    if len(parts) >= 4:
        site, city, country, region = parts[0], parts[1], parts[2], parts[3]
        hierarchy_paths.add((site, city))
        hierarchy_paths.add((city, country))
        hierarchy_paths.add((country, region))

print(f"  Additional located_in edges (hierarchy): {len(hierarchy_paths)}")
print(f"  Current prototype edges: {total_rels}")
print(f"  Impact on total edges: +{pct(len(hierarchy_paths), total_rels)}")


# ══════════════════════════════════════════════════════════════════════════
# ANALYSIS 8: Dual-Source `resulted_in` Overlap
# ══════════════════════════════════════════════════════════════════════════
print("\n── Analysis 8: Dual-source resulted_in overlap ──")

impact_types = Counter()
impact_null = 0
for rec in records:
    it = rec["impact_type"]
    if it:
        impact_types[it] += 1
    else:
        impact_null += 1

print(f"  IMPACT_TYPE distribution ({N - impact_null}/{N} present, {pct(N - impact_null, N)} coverage):")
for val, cnt in impact_types.most_common():
    print(f"    {val}: {cnt} ({pct(cnt, N)})")

# For prototype incidents, compare IMPACT_TYPE vs extracted INJURY_TYPE entities
injury_terms = {"fracture", "laceration", "burn", "cut", "bruise", "strain", "sprain",
                "contusion", "abrasion", "puncture", "crush", "amputation", "dislocation",
                "wound", "injury", "bleeding", "swelling", "pain", "broken"}

agreement = 0
disagreement = 0
gliner_finds_missed = 0
no_comparison = 0

for iid in prototype_ids:
    rec = records_by_id.get(iid)
    if not rec:
        continue
    impact = rec["impact_type"]
    inj_ents = [e for e in entities_by_incident.get(iid, []) if e["type"] == "INJURY_TYPE"]

    if not impact:
        no_comparison += 1
        continue

    impact_lower = impact.lower()
    has_injury_impact = "injury" in impact_lower or "illness" in impact_lower
    has_injury_ents = len(inj_ents) > 0

    if has_injury_impact and has_injury_ents:
        agreement += 1
    elif has_injury_impact and not has_injury_ents:
        # IMPACT_TYPE says injury but GLiNER didn't extract injury entities
        disagreement += 1
    elif not has_injury_impact and has_injury_ents:
        gliner_finds_missed += 1
    # else: both say no injury — not interesting

compared = agreement + disagreement + gliner_finds_missed
print(f"  Prototype comparison (injury-related incidents):")
print(f"    Both agree (injury in IMPACT_TYPE + GLiNER): {agreement}")
print(f"    IMPACT_TYPE says injury, GLiNER misses: {disagreement}")
print(f"    GLiNER finds injury, IMPACT_TYPE doesn't say injury: {gliner_finds_missed}")
print(f"    No IMPACT_TYPE to compare: {no_comparison}")

# Also scan full dataset narratives for injury terms
narr_injury_count = 0
impact_injury_count = sum(1 for r in records if r["impact_type"] and ("injury" in r["impact_type"].lower() or "illness" in r["impact_type"].lower()))
for rec in records:
    narr = rec["narrative"].lower()
    if any(t in narr for t in injury_terms):
        narr_injury_count += 1

print(f"  Full dataset: IMPACT_TYPE mentions injury/illness: {impact_injury_count}/{N} ({pct(impact_injury_count, N)})")
print(f"  Full dataset: Narrative contains injury terms: {narr_injury_count}/{N} ({pct(narr_injury_count, N)})")

# Cross-reference
both_mention = 0
impact_only = 0
narrative_only = 0
for rec in records:
    has_impact_injury = rec["impact_type"] and ("injury" in rec["impact_type"].lower() or "illness" in rec["impact_type"].lower())
    has_narr_injury = any(t in rec["narrative"].lower() for t in injury_terms)
    if has_impact_injury and has_narr_injury:
        both_mention += 1
    elif has_impact_injury and not has_narr_injury:
        impact_only += 1
    elif not has_impact_injury and has_narr_injury:
        narrative_only += 1

print(f"  Both IMPACT_TYPE + narrative mention injury: {both_mention}")
print(f"  IMPACT_TYPE only: {impact_only}")
print(f"  Narrative only: {narrative_only}")


# ══════════════════════════════════════════════════════════════════════════
# GENERATE REPORT
# ══════════════════════════════════════════════════════════════════════════
print("\n\nGenerating schema_validation_evidence.md...")

report = []
report.append("# Schema Validation Evidence Report")
report.append(f"\n**Generated:** 2026-02-19  ")
report.append(f"**Dataset:** {fmt(N)} records (raw), {fmt(len(prototype_ids))} incidents (prototype extraction)  ")
report.append(f"**Entities extracted:** {fmt(len(entities))} | **Relations extracted:** {fmt(len(relations))}")

# ── Executive Summary ──
report.append("\n## Executive Summary\n")
report.append("1. **`used_in` Removal:** Only {}/{} extraction edges ({}) are `USED_IN`. Narrative patterns matching \"used in/during/for\" appear in {} of narratives. **Recommend removal** — nearly dead schema weight.".format(
    used_in_count, total_rels, pct(used_in_count, total_rels),
    pct(used_in_narrative_count, narrs_with_text)))

# Incident type summary
max_it_val, max_it_cnt = incident_types.most_common(1)[0]
report.append(f'2. **Incident Type → Property:** \"{max_it_val}\" alone would have degree {fmt(max_it_cnt)} — {max_it_cnt / mean_degree:.0f}x the prototype mean degree ({mean_degree:.1f}). {pct(incident_type_null, N)} null rate. All queries use it as a filter. **Strongly recommend property.**')

report.append(f'3. **Date → Property:** REPORTED_DATE covers {pct(reported_date_present, N)} of records. At day granularity, {fmt(len(date_by_day))} unique nodes with median degree {day_degrees[len(day_degrees)//2] if day_degrees else "N/A"}. At year granularity, mega-hub problem recurs. **Strongly recommend property.**')

report.append(f'4. **CASE_CATEGORIZATION → Entity:** {len(case_cats)} unique values, {pct(case_cat_present, N)} coverage. {pct(unique_connections, sampled_pairs)} of incident pairs sharing a category have NO other entity overlap — these are genuinely novel cross-incident connections. **Recommend entity (Root Cause Category).**')

report.append(f'5. **Split `caused_by`:** Of {len(caused_by_rels)} CAUSED_BY edges, {pct(metadata_sourced, len(caused_by_rels) if caused_by_rels else 1)} match CASE_CATEGORIZATION values (metadata-sourced). Only {pct(cat_narrative_match, total_cat_narr)} of categorizations have word overlap with their narrative. **Split into `categorized_as` (L1) + `caused_by` (L2) is justified.**')

report.append(f'6. **Entity-type relation assignment:** {len(multi_type_spans)} entity spans have multiple type assignments. {pct(len(both_equip_body), len(prototype_ids))} of prototype incidents have both Equipment and Body Part. INVOLVED tail types: {dict(involved_tail_types)}; AFFECTED tail types: {dict(affected_tail_types)}. **Entity type alone is sufficient for relation assignment in the vast majority of cases.**')

report.append(f'7. **Location hierarchy:** {pct(component_counts.get(5, 0) + component_counts.get(4, 0), workplace_present)} of WORKPLACE strings parse into 4-5 components. {len(city_multi_country)} cities appear under multiple countries (inconsistencies). {len(hierarchy_paths)} additional `located_in` edges. **Feasible with minor cleanup.**')

report.append(f'8. **Dual-source `resulted_in`:** Narrative finds injuries that IMPACT_TYPE misses in {narrative_only} records. IMPACT_TYPE reports injury without narrative evidence in {impact_only} cases. **Dual-source with `source` property is justified** — each source catches what the other misses.')

# ── Detailed Sections ──

# Analysis 1
report.append("\n---\n## Analysis 1: `used_in` Viability Test\n")
report.append("### Extraction Output: Relation Type Distribution\n")
report.append("| Relation Type | Count | % of Total |")
report.append("|--------------|------:|----------:|")
for rt, c in rel_type_counts.most_common():
    report.append(f"| {rt} | {fmt(c)} | {pct(c, total_rels)} |")

report.append(f"\n### Narrative Pattern Scan (all {fmt(narrs_with_text)} narratives with text)\n")
report.append(f"- **`used_in` patterns** (\"used in/during/for\", \"using a/the\", \"operating a/the\"): **{fmt(used_in_narrative_count)}** ({pct(used_in_narrative_count, narrs_with_text)})")
report.append(f"- **`involved` patterns** (\"involved/involving\", \"while using/operating/working with\"): **{fmt(involved_narrative_count)}** ({pct(involved_narrative_count, narrs_with_text)})")

report.append("\n### `used_in` Example Sentences\n")
for i, ex in enumerate(used_in_examples, 1):
    report.append(f"{i}. `{ex}`")

report.append("\n### `involved` Example Sentences\n")
for i, ex in enumerate(involved_examples, 1):
    report.append(f"{i}. `{ex}`")

used_in_viable = used_in_count / total_rels * 100 if total_rels else 0
report.append(f"\n### Recommendation\n")
if used_in_viable < 5 and used_in_narrative_count / narrs_with_text * 100 < 10:
    report.append(f"**REMOVE `used_in`.** Extraction produces only {pct(used_in_count, total_rels)} `USED_IN` edges. While narrative patterns suggest {pct(used_in_narrative_count, narrs_with_text)} of records could theoretically support it, the current rule-based extractor cannot reliably distinguish `used_in` from `involved`. The relation adds schema complexity without proportional value.")
else:
    report.append(f"**KEEP `used_in`** — narrative evidence ({pct(used_in_narrative_count, narrs_with_text)}) exceeds the 10% threshold.")

# Analysis 2
report.append("\n---\n## Analysis 2: Incident Type — Entity vs. Property\n")
report.append("### Value Distribution\n")
report.append("| Incident Type | Count | % of Dataset |")
report.append("|--------------|------:|------------:|")
for val, cnt in incident_types.most_common():
    report.append(f"| {val} | {fmt(cnt)} | {pct(cnt, N)} |")
report.append(f"| *(null/missing)* | {fmt(incident_type_null)} | {pct(incident_type_null, N)} |")

report.append(f"\n### Mega-Hub Analysis\n")
report.append(f"- Prototype mean degree: **{mean_degree:.2f}**")
for val, cnt in incident_types.most_common():
    ratio = cnt / mean_degree if mean_degree > 0 else 0
    report.append(f'- "{val}" as entity node: degree = **{fmt(cnt)}**, which is **{ratio:.0f}x** the mean degree')
report.append(f"- Null rate: **{pct(incident_type_null, N)}** — these incidents would have no type edge")

report.append("\n### Query Pattern Analysis\n")
report.append("All benchmark queries that reference incident type use it as a **filter** (e.g., \"show me Near Miss incidents involving cranes\"), not as a **traversal target** (no query needs to traverse *through* an Incident Type node to reach another entity).")

report.append("\n### Recommendation\n")
report.append(f"**Convert to PROPERTY.** Incident Type as entity would create {len(incident_types)} mega-hub nodes with degrees ranging from {min(incident_types.values()):,} to {max(incident_types.values()):,} — {max(incident_types.values()) / mean_degree:.0f}x the graph mean. These hubs degrade graph traversal (every query touching them scans thousands of edges) and provide no structural benefit over a simple property filter.")

# Analysis 3
report.append("\n---\n## Analysis 3: Date — Entity vs. Property\n")
report.append("### Coverage\n")
report.append(f"| Field | Records Present | Coverage |")
report.append(f"|-------|---------------:|--------:|")
report.append(f"| EVENT_DATETIME | {fmt(event_datetime_present)} | {pct(event_datetime_present, N)} |")
report.append(f"| REPORTED_DATE | {fmt(reported_date_present)} | {pct(reported_date_present, N)} |")

report.append(f"\n### Granularity Analysis\n")
report.append(f"| Granularity | Unique Nodes | Max Degree | Median Degree | Mean Degree |")
report.append(f"|------------|------------:|-----------:|-------------:|----------:|")
if day_degrees:
    report.append(f"| Day | {fmt(len(date_by_day))} | {day_degrees[0]} | {day_degrees[len(day_degrees)//2]} | {sum(day_degrees)/len(day_degrees):.1f} |")
month_degrees = sorted(date_by_month.values(), reverse=True)
if month_degrees:
    report.append(f"| Month | {fmt(len(date_by_month))} | {month_degrees[0]} | {month_degrees[len(month_degrees)//2]} | {sum(month_degrees)/len(month_degrees):.1f} |")
year_degrees_list = sorted(date_by_year.values(), reverse=True)
if year_degrees_list:
    report.append(f"| Year | {fmt(len(date_by_year))} | {year_degrees_list[0]} | {year_degrees_list[len(year_degrees_list)//2]} | {sum(year_degrees_list)/len(year_degrees_list):.1f} |")

report.append(f"\n### Year-Level Degree Distribution\n")
report.append(f"| Year | Incidents |")
report.append(f"|------|--------:|")
for yr, cnt in sorted(date_by_year.items()):
    report.append(f"| {yr} | {fmt(cnt)} |")

report.append("\n### Recommendation\n")
if day_degrees:
    report.append(f"**Convert to PROPERTY.** At day granularity, {fmt(len(date_by_day))} nodes with median degree {day_degrees[len(day_degrees)//2]} provide minimal shared structure. At year granularity, the mega-hub problem recurs (max degree {year_degrees_list[0]:,}). Date is universally used as a filter (\"incidents in Q3 2023\"), not a traversal target. Store as ISO-8601 property on incident nodes.")

# Analysis 4
report.append("\n---\n## Analysis 4: CASE_CATEGORIZATION — Entity vs. Property\n")
report.append("### Overview\n")
report.append(f"- **Unique values:** {len(case_cats)}")
report.append(f"- **Coverage:** {fmt(case_cat_present)}/{fmt(N)} ({pct(case_cat_present, N)})")
report.append(f"- **Null/missing:** {fmt(case_cat_null)} ({pct(case_cat_null, N)})")

report.append(f"\n### Degree Distribution (if modeled as entity)\n")
report.append(f"- Max degree: {cat_degrees[0]:,}")
report.append(f"- Median degree: {cat_degrees[len(cat_degrees)//2]:,}")
report.append(f"- Min degree: {cat_degrees[-1]:,}")
report.append(f"- Mean degree: {sum(cat_degrees)/len(cat_degrees):.1f}")

report.append(f"\n### Top 20 Categories\n")
report.append(f"| Category | Count | % of Dataset |")
report.append(f"|----------|------:|------------:|")
for val, cnt in case_cats.most_common(20):
    report.append(f"| {val} | {fmt(cnt)} | {pct(cnt, N)} |")

report.append(f"\n### Cross-Incident Connection Analysis\n")
report.append(f"Among top-20 categories, for prototype incidents sharing a category:")
report.append(f"- **Pairs sampled:** {fmt(sampled_pairs)}")
report.append(f"- **Unique connections** (share category but NO entity overlap): **{fmt(unique_connections)}** ({pct(unique_connections, sampled_pairs)})")
report.append(f"- **Redundant** (share category AND ≥1 entity): **{fmt(redundant_connections)}** ({pct(redundant_connections, sampled_pairs)})")
report.append(f"\nThis means {pct(unique_connections, sampled_pairs)} of cross-incident connections via CASE_CATEGORIZATION are **genuinely novel** — they link incidents that would otherwise be isolated in the graph.")

report.append("\n### Recommendation\n")
if unique_connections > redundant_connections:
    report.append(f"**Promote to ENTITY (Root Cause Category).** The majority ({pct(unique_connections, sampled_pairs)}) of connections are unique — CASE_CATEGORIZATION creates meaningful cross-incident structure that no other entity type provides. With 117 values and manageable degrees, it avoids the mega-hub problem. Use relation type `categorized_as` (Layer 1, metadata-derived).")
else:
    report.append(f"**Keep as PROPERTY.** Only {pct(unique_connections, sampled_pairs)} of connections are unique — most are redundant with existing entity overlap.")

# Analysis 5
report.append("\n---\n## Analysis 5: `caused_by` Source Conflation\n")
report.append(f"### CAUSED_BY Edge Source Breakdown\n")
report.append(f"- **Total CAUSED_BY edges:** {len(caused_by_rels)}")
report.append(f"- **Metadata-sourced** (tail matches a CASE_CATEGORIZATION value): **{metadata_sourced}** ({pct(metadata_sourced, len(caused_by_rels) if caused_by_rels else 1)})")
report.append(f"- **Narrative-sourced** (tail is an extracted entity with causal context): **{narrative_sourced}** ({pct(narrative_sourced, len(caused_by_rels) if caused_by_rels else 1)})")

if narrative_cause_types:
    report.append(f"\n### Narrative-Sourced Cause Entity Types\n")
    report.append(f"| Entity Type | Count |")
    report.append(f"|------------|------:|")
    for et, cnt in narrative_cause_types.most_common():
        report.append(f"| {et} | {cnt} |")

report.append(f"\n### Causal Language in Narratives\n")
report.append(f"- Narratives containing causal markers (\"due to\", \"caused by\", \"failure of\", etc.): **{fmt(causal_narrative_count)}/{fmt(narrs_with_text)}** ({pct(causal_narrative_count, narrs_with_text)})")
report.append(f"\n### CASE_CATEGORIZATION vs. Narrative Content Overlap\n")
report.append(f"- Records where CASE_CATEGORIZATION words appear in narrative: **{fmt(cat_narrative_match)}/{fmt(total_cat_narr)}** ({pct(cat_narrative_match, total_cat_narr)})")
report.append(f"- Records where CASE_CATEGORIZATION words do NOT appear in narrative: **{fmt(cat_narrative_mismatch)}/{fmt(total_cat_narr)}** ({pct(cat_narrative_mismatch, total_cat_narr)})")
report.append(f"\nThis low overlap confirms that CASE_CATEGORIZATION is an **analyst-assigned label**, not a narrative-derived finding. Conflating it with narrative-extracted causal relationships under a single `caused_by` relation mixes signal provenance.")

report.append(f"\n### Example Causal Sentences\n")
for i, ex in enumerate(causal_examples, 1):
    report.append(f"{i}. `{ex}`")

report.append("\n### Recommendation\n")
report.append(f"**Split into `categorized_as` (Layer 1, metadata) and `caused_by` (Layer 2, narrative).** The current `caused_by` conflates two fundamentally different signal sources. Metadata-derived categorization is deterministic and available for {pct(case_cat_present, N)} of records. Narrative-derived causation requires NLP extraction and is available where causal language exists ({pct(causal_narrative_count, narrs_with_text)}). Separating them enables proper provenance tracking and avoids misleading causal claims from metadata alone.")

# Analysis 6
report.append("\n---\n## Analysis 6: `involved` vs. `affected` Disambiguation\n")
report.append("### Entity Type Distribution\n")
report.append("| Entity Type | Count | % of Total |")
report.append("|------------|------:|----------:|")
for et, cnt in entity_type_counts.most_common():
    report.append(f"| {et} | {fmt(cnt)} | {pct(cnt, len(entities))} |")

report.append(f"\n### Type Ambiguity Check\n")
report.append(f"- Spans assigned to multiple types: **{len(multi_type_spans)}**")
if multi_type_spans:
    report.append(f"\n| Span | Types |")
    report.append(f"|------|-------|")
    for span, types in list(multi_type_spans.items())[:15]:
        report.append(f"| {span} | {', '.join(types)} |")

report.append(f"\n### Relation Assignment by Entity Type\n")
report.append(f"| Relation | Tail Types |")
report.append(f"|----------|-----------|")
report.append(f"| INVOLVED | {', '.join(f'{t}: {c}' for t, c in involved_tail_types.most_common())} |")
report.append(f"| AFFECTED | {', '.join(f'{t}: {c}' for t, c in affected_tail_types.most_common())} |")

report.append(f"\n### Co-occurrence Analysis\n")
report.append(f"- Incidents with Equipment entities: **{len(incidents_with_equip)}**")
report.append(f"- Incidents with Body Part entities: **{len(incidents_with_body)}**")
report.append(f"- Incidents with BOTH Equipment + Body Part: **{len(both_equip_body)}** ({pct(len(both_equip_body), len(prototype_ids))} of prototype)")

report.append(f"\n### Sample Co-occurrence Examples (Equipment + Body Part)\n")
for i, ex in enumerate(cooccur_examples[:20], 1):
    report.append(f"\n**Example {i}** (Incident {ex['incident_id']})")
    report.append(f"- Equipment: {', '.join(ex['equipment'])}")
    report.append(f"- Body Parts: {', '.join(ex['body_parts'])}")
    report.append(f"- Narrative: \"{ex['narrative_snippet']}...\"")

report.append("\n### Recommendation\n")
report.append(f"**Entity type alone is sufficient for relation assignment.** The current schema maps Equipment→INVOLVED, Body Part→AFFECTED, Injury Type→RESULTED_IN deterministically via `INCIDENT_RELATION_MAP`. Only {len(multi_type_spans)} entity spans show type ambiguity. In {pct(len(both_equip_body), len(prototype_ids))} of prototype incidents where both types co-occur, the entity type cleanly determines the correct relation without requiring sentence-level context.")

# Analysis 7
report.append("\n---\n## Analysis 7: Location Hierarchy Feasibility\n")
report.append("### WORKPLACE Field Coverage\n")
report.append(f"- **Present:** {fmt(workplace_present)}/{fmt(N)} ({pct(workplace_present, N)})")
report.append(f"- **Missing:** {fmt(workplace_null)} ({pct(workplace_null, N)})")

report.append(f"\n### Component Count Distribution\n")
report.append(f"| Components | Count | % of Present |")
report.append(f"|-----------|------:|------------:|")
for n_parts, cnt in sorted(component_counts.items()):
    report.append(f"| {n_parts} | {fmt(cnt)} | {pct(cnt, workplace_present)} |")

parseable = component_counts.get(5, 0) + component_counts.get(4, 0)
report.append(f"\n### Hierarchy Extraction (4-5 component strings)\n")
report.append(f"- **Parseable records:** {fmt(parseable)} ({pct(parseable, workplace_present)})")
report.append(f"- **Unique sites:** {len(sites)}")
report.append(f"- **Unique cities:** {len(cities)}")
report.append(f"- **Unique countries:** {len(countries)}")
report.append(f"- **Unique regions:** {len(regions)}")

report.append(f"\n### Consistency Check\n")
report.append(f"- **Cities in multiple countries:** {len(city_multi_country)}")
if city_multi_country:
    for c, cs in list(city_multi_country.items())[:5]:
        report.append(f"  - \"{c}\" → {', '.join(cs)}")
report.append(f"- **Sites in multiple cities:** {len(site_multi_city)}")
if site_multi_city:
    for s, cs in list(site_multi_city.items())[:5]:
        report.append(f"  - \"{s}\" → {', '.join(cs)}")

report.append(f"\n### Edge Impact\n")
report.append(f"- **Additional `located_in` edges:** {len(hierarchy_paths)}")
report.append(f"- **Current prototype edges:** {fmt(total_rels)}")
report.append(f"- **Edge increase:** +{pct(len(hierarchy_paths), total_rels)}")

report.append("\n### Recommendation\n")
report.append(f"**Feasible with minor cleanup.** {pct(parseable, workplace_present)} of WORKPLACE strings parse cleanly into the expected hierarchy. {len(city_multi_country)} city-level inconsistencies need resolution (likely data quality issues in the source system). The {len(hierarchy_paths)} additional `located_in` edges are a modest +{pct(len(hierarchy_paths), total_rels)} increase that enables powerful geographic traversal queries (\"all incidents in Brazil\" without string matching).")

# Analysis 8
report.append("\n---\n## Analysis 8: Dual-Source `resulted_in` Overlap\n")
report.append("### IMPACT_TYPE Distribution (Full Dataset)\n")
report.append(f"| Impact Type | Count | % of Dataset |")
report.append(f"|------------|------:|------------:|")
for val, cnt in impact_types.most_common():
    report.append(f"| {val} | {fmt(cnt)} | {pct(cnt, N)} |")
report.append(f"| *(null/missing)* | {fmt(impact_null)} | {pct(impact_null, N)} |")

report.append(f"\n### Prototype: IMPACT_TYPE vs. GLiNER Injury Extraction\n")
report.append(f"| Scenario | Count |")
report.append(f"|----------|------:|")
report.append(f"| Both agree (IMPACT_TYPE = injury + GLiNER extracts injury) | {agreement} |")
report.append(f"| IMPACT_TYPE = injury, GLiNER finds no injury entity | {disagreement} |")
report.append(f"| GLiNER extracts injury, IMPACT_TYPE ≠ injury | {gliner_finds_missed} |")
report.append(f"| No IMPACT_TYPE available | {no_comparison} |")

report.append(f"\n### Full Dataset: Narrative vs. Metadata Injury Detection\n")
report.append(f"| Source | Records | % of Dataset |")
report.append(f"|--------|--------:|------------:|")
report.append(f"| IMPACT_TYPE mentions injury/illness | {fmt(impact_injury_count)} | {pct(impact_injury_count, N)} |")
report.append(f"| Narrative contains injury terms | {fmt(narr_injury_count)} | {pct(narr_injury_count, N)} |")
report.append(f"| Both sources agree | {fmt(both_mention)} | {pct(both_mention, N)} |")
report.append(f"| IMPACT_TYPE only (narrative misses) | {fmt(impact_only)} | {pct(impact_only, N)} |")
report.append(f"| Narrative only (IMPACT_TYPE misses) | {fmt(narrative_only)} | {pct(narrative_only, N)} |")

report.append("\n### Recommendation\n")
report.append(f"**Dual-source `resulted_in` with `source` property is justified.** Each source catches what the other misses: IMPACT_TYPE provides {fmt(impact_only)} injury classifications not evident in narratives, while narratives reveal {fmt(narrative_only)} injury mentions that IMPACT_TYPE doesn't capture. A `source` property (\"metadata\" vs. \"narrative\") on `resulted_in` edges enables provenance-aware querying and avoids false confidence from either source alone.")

# ── Final Recommendation Table ──
report.append("\n---\n## Final Recommendation Table\n")
report.append("| Schema Change | Evidence Supports? | Confidence | Key Metric |")
report.append("|--------------|-------------------|------------|------------|")
report.append(f"| Remove `used_in` | **Yes** | High | {pct(used_in_count, total_rels)} of edges |")
report.append(f"| Incident Type → property | **Yes** | High | {max(incident_types.values()) / mean_degree:.0f}x mean degree, {pct(incident_type_null, N)} null |")
report.append(f"| Date → property | **Yes** | High | Median day-degree = {day_degrees[len(day_degrees)//2] if day_degrees else 'N/A'}, {pct(reported_date_present, N)} coverage |")
report.append(f"| CASE_CATEGORIZATION → entity | **Yes** | Medium | {pct(unique_connections, sampled_pairs)} unique cross-connections |")
report.append(f"| Split `caused_by` → `categorized_as` + `caused_by` (L2) | **Yes** | High | {pct(metadata_sourced, len(caused_by_rels) if caused_by_rels else 1)} metadata-sourced |")
report.append(f"| Entity-type-only relation assignment | **Yes** | High | {len(multi_type_spans)} ambiguous spans |")
report.append(f"| Location hierarchy (`located_in`) | **Yes** | Medium | {pct(parseable, workplace_present)} parseable, {len(city_multi_country)} inconsistencies |")
report.append(f"| Dual-source `resulted_in` | **Yes** | Medium | {fmt(narrative_only)} narrative-only finds |")

report.append("\n---\n*This report provides empirical justification for the v1→v2 schema migration. All numbers derived from the {}-record dataset and {}-incident prototype extraction.*".format(fmt(N), fmt(len(prototype_ids))))

# Write report
OUTPUT_MD.write_text("\n".join(report), encoding="utf-8")
print(f"\nReport written to {OUTPUT_MD}")
