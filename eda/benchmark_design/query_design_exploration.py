#!/usr/bin/env python3
"""
Data profiling of 23,311 safety incident records to ground benchmark query design.

Runs six analyses on the incidents CSV and writes a markdown report to
query_design_exploration.md: (1) entity landscape profiling — term frequency
for equipment, injury/body part, and causal action terms across narratives;
(2) CASE_CATEGORIZATION taxonomy — distribution and clustering of all incident
categories cross-tabulated against IMPACT_TYPE and severity; (3) causal language
frequency — 15 causal phrase patterns measured per narrative; (4) metadata field
coverage and cross-tabulations (INCIDENT_TYPE x IMPACT_TYPE, country x severity);
(5) queryable combinations matrix — equipment x injury co-occurrence with causal
coverage and severity breakdown; (6) surface form variation audit — fragmentation
scores per entity to identify ER stress-test candidates.

Key findings: equipment dominated by vessel/crane/pipe (highest narrative
frequency); injuries dominated by back/hand/cut; top causal actions fell/hit/
injured; strong query candidates include crane-hand, pipe-back, vessel-injury
combinations with >= 50 co-occurrences; pipe/pipeline/piping and
forklift/fork-lift/FLT show the highest surface form fragmentation.

Decision: directly informed the 30 benchmark queries in pipeline/benchmark/,
providing the data-grounded entity/relation combinations, co-occurrence counts,
and causal language coverage that determine query difficulty and expected recall.
"""
from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent.parent  # repo root
CSV_PATH = ROOT / "input" / "incidents.csv"
OUTPUT_PATH = Path(__file__).resolve().parent / "query_design_exploration.md"


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def parse_records(csv_path: Path) -> List[Dict[str, str]]:
    """Parse the CSV into a list of dicts with narrative, entity_facts, meta_facts."""
    records = []
    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row.get("text", "")
            text = text.replace("\\n", "\n").replace("\\t", "\t")
            rec = {"id": row.get("RECORD_NO_LOSS_POTENTIAL", ""), "raw": text}

            # Extract sections
            rec["narrative"] = extract_section(text, "NARRATIVE")
            rec["entity_facts"] = extract_section(text, "ENTITY_FACTS")
            rec["meta_facts"] = extract_section(text, "META_FACTS")
            rec["incident_label"] = extract_line(text, "INCIDENT_LABEL")

            # Parse structured fields
            rec["ef"] = parse_kv_block(rec["entity_facts"])
            rec["mf"] = parse_meta_block(rec["meta_facts"])

            records.append(rec)
    return records


def extract_section(text: str, section: str) -> str:
    pattern = rf"{section}:\n(.*?)(?:\n\n[A-Z_]+:|$)"
    m = re.search(pattern, text, re.DOTALL)
    return m.group(1).strip() if m else ""


def extract_line(text: str, key: str) -> str:
    m = re.search(rf"{key}:\s*(.*)", text)
    return m.group(1).strip() if m else ""


def parse_kv_block(block: str) -> Dict[str, str]:
    facts = {}
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("-"):
            continue
        part = line[1:].strip()
        if ":" not in part:
            continue
        key, val = part.split(":", 1)
        facts[key.strip().upper()] = val.strip()
    return facts


def parse_meta_block(block: str) -> Dict[str, str]:
    facts = {}
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("-"):
            continue
        # format: - META[KEY]: VALUE
        m = re.match(r"-\s*META\[([^\]]+)\]:\s*(.*)", line)
        if m:
            facts[m.group(1).strip().upper()] = m.group(2).strip()
    return facts


# ---------------------------------------------------------------------------
# Analysis helpers
# ---------------------------------------------------------------------------

def count_term_in_records(records: List[Dict], field: str, terms: List[str]) -> List[Tuple[str, int, float]]:
    """Count how many records contain each term (case-insensitive, word boundary)."""
    total = len(records)
    results = []
    for term in terms:
        pattern = re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)
        count = sum(1 for r in records if pattern.search(r.get(field, "")))
        pct = count / total * 100 if total else 0
        results.append((term, count, pct))
    results.sort(key=lambda x: -x[1])
    return results


def density_flag(pct: float) -> str:
    if pct > 5:
        return "HIGH"
    elif pct >= 1:
        return "MEDIUM"
    return "LOW"


def parse_workplace(wp: str) -> Dict[str, str]:
    """Parse 'Site, City, Country, Region, TechnipFMC' format."""
    parts = [p.strip() for p in wp.split(",")]
    result = {"site": "", "city": "", "country": "", "region": ""}
    keys = ["site", "city", "country", "region"]
    for i, key in enumerate(keys):
        if i < len(parts):
            result[key] = parts[i]
    return result


def severity_bin(sev: str) -> str:
    """Bin severity string into 1-5 category."""
    if not sev:
        return "Unknown"
    m = re.match(r"(\d)", sev)
    if m:
        digit = int(m.group(1))
        labels = {1: "1-Negligible", 2: "2-Minor", 3: "3-Moderate", 4: "4-Major", 5: "5-Catastrophic"}
        return labels.get(digit, f"{digit}-Unknown")
    sev_lower = sev.lower()
    if "negligible" in sev_lower or "first aid" in sev_lower or "no impact" in sev_lower:
        return "1-Negligible"
    if "minor" in sev_lower:
        return "2-Minor"
    if "moderate" in sev_lower or "lost time" in sev_lower:
        return "3-Moderate"
    if "major" in sev_lower:
        return "4-Major"
    if "catastrophic" in sev_lower or "fatal" in sev_lower:
        return "5-Catastrophic"
    return "Unknown"


# ---------------------------------------------------------------------------
# Main analyses
# ---------------------------------------------------------------------------

def analysis_1(records: List[Dict], out: list):
    """Entity Landscape Profiling."""
    out.append("## Analysis 1: Entity Landscape Profiling\n")
    total = len(records)
    out.append(f"Total records scanned: {total}\n")

    # Equipment terms
    equipment_terms = [
        "valve", "pump", "crane", "forklift", "scaffold", "pipe", "hose", "winch",
        "drill", "compressor", "turbine", "generator", "conveyor", "ladder", "harness",
        "sling", "chain", "cable", "motor", "engine", "tank", "vessel", "boiler",
        "wrench", "grinder", "welder", "saw", "hammer", "jack", "lift", "elevator",
        "hoist", "trolley", "clamp", "gauge", "meter", "sensor", "bolt", "nut",
        "flange", "gasket", "bearing", "gear", "pulley", "belt", "nozzle", "fitting",
        "coupling", "sprocket", "piston", "cylinder", "actuator", "regulator",
        "transformer", "breaker", "switch", "wire", "rope", "rig", "derrick",
        "mast", "boom", "jib", "hook", "shackle", "pin", "cleat", "winch",
        "capstan", "reel", "spool", "drum", "choke", "manifold", "header",
        "separator", "exchanger", "reactor", "furnace", "oven", "kiln",
        "container", "pallet", "basket", "tool", "equipment", "machine",
        "vehicle", "truck", "car", "trailer", "forklift", "loader", "excavator",
        "bulldozer", "backhoe", "grader", "roller", "scraper", "cutter",
        "torch", "electrode", "weld", "grinding", "cutting", "lifting",
        "rigging", "scaffolding", "platform", "walkway", "stairway", "railing",
        "guard", "barrier", "fence", "door", "gate", "panel", "board",
        "monitor", "display", "camera", "alarm", "detector", "extinguisher",
        "hydrant", "sprinkler", "PPE", "gloves", "helmet", "goggles",
        "respirator", "boots", "coverall",
    ]
    # Deduplicate
    equipment_terms = list(dict.fromkeys(equipment_terms))

    eq_results = count_term_in_records(records, "narrative", equipment_terms)[:50]

    out.append("### Equipment Mentions (Top 50)\n")
    out.append("| Rank | Term | Count | % Records | Density |")
    out.append("|------|------|-------|-----------|---------|")
    for i, (term, count, pct) in enumerate(eq_results, 1):
        out.append(f"| {i} | {term} | {count} | {pct:.1f}% | {density_flag(pct)} |")
    out.append("")

    # Injury/body part terms
    injury_terms = [
        "hand", "finger", "eye", "back", "head", "knee", "foot", "arm", "leg",
        "shoulder", "neck", "wrist", "ankle", "toe", "face", "chest", "elbow",
        "hip", "shin", "rib", "fracture", "laceration", "burn", "cut", "bruise",
        "sprain", "strain", "crush", "puncture", "abrasion", "contusion",
        "amputation", "dislocation", "concussion", "exposure", "inhalation",
        "swelling", "pain", "injury", "wound", "bleeding", "scratch",
    ]
    injury_terms = list(dict.fromkeys(injury_terms))
    inj_results = count_term_in_records(records, "narrative", injury_terms)[:40]

    out.append("### Injury/Body Part Mentions (Top 40)\n")
    out.append("| Rank | Term | Count | % Records | Density |")
    out.append("|------|------|-------|-----------|---------|")
    for i, (term, count, pct) in enumerate(inj_results, 1):
        out.append(f"| {i} | {term} | {count} | {pct:.1f}% | {density_flag(pct)} |")
    out.append("")

    # Causal/action terms
    causal_action_terms = [
        "fell", "dropped", "struck", "hit", "caught", "trapped", "slipped",
        "tripped", "collapsed", "leaked", "spilled", "exploded", "failed",
        "broke", "malfunctioned", "overloaded", "corroded", "dislodged",
        "ejected", "released", "injured", "damaged", "impacted", "contacted",
        "pinched", "crushed", "cut", "burned", "fractured",
    ]
    causal_action_terms = list(dict.fromkeys(causal_action_terms))
    ca_results = count_term_in_records(records, "narrative", causal_action_terms)[:30]

    out.append("### Causal/Action Terms (Top 30)\n")
    out.append("| Rank | Term | Count | % Records | Density |")
    out.append("|------|------|-------|-----------|---------|")
    for i, (term, count, pct) in enumerate(ca_results, 1):
        out.append(f"| {i} | {term} | {count} | {pct:.1f}% | {density_flag(pct)} |")
    out.append("")

    return eq_results, inj_results


def analysis_2(records: List[Dict], out: list):
    """CASE_CATEGORIZATION Taxonomy."""
    out.append("## Analysis 2: CASE_CATEGORIZATION Taxonomy\n")

    # Extract all CASE_CATEGORIZATION values
    cc_counter = Counter()
    for r in records:
        cc = r["mf"].get("CASE_CATEGORIZATION", "").strip()
        if cc:
            cc_counter[cc] += 1

    out.append(f"Total unique CASE_CATEGORIZATION values: {len(cc_counter)}\n")
    out.append("### All Values (sorted by count)\n")
    out.append("| Rank | CASE_CATEGORIZATION | Count | % |")
    out.append("|------|---------------------|-------|---|")
    total_with_cc = sum(cc_counter.values())
    for i, (cc, count) in enumerate(cc_counter.most_common(), 1):
        pct = count / len(records) * 100
        out.append(f"| {i} | {cc} | {count} | {pct:.1f}% |")
    out.append("")

    # Group into natural clusters
    cluster_map = {
        "Mechanical": ["mechanical", "machine", "equipment", "tool", "motor vehicle", "crane", "lifting",
                        "uncontrolled moving", "struck by", "pressur", "hydraulic", "pneumatic"],
        "Falls & Slips": ["fall", "slip", "trip", "same level", "lower level", "height"],
        "Chemical & Hazmat": ["chemical", "hazardous", "substance", "spill", "leak", "release",
                               "exposure", "inhalation", "radiation"],
        "Electrical": ["electrical", "electr", "arc flash", "shock"],
        "Fire & Explosion": ["fire", "explosion", "burn", "ignition", "flammab"],
        "Procedural & Organizational": ["procedure", "supervision", "planning", "coordination",
                                         "standard operating", "permit", "management of change",
                                         "communication", "competenc", "training", "organization"],
        "Human Factors": ["human factor", "ergonomic", "fatigue", "stress", "behavior",
                           "fitness for duty", "alcohol", "drug"],
        "Environmental": ["environment", "weather", "natural", "climate", "marine life"],
        "Risk Assessment & Hazard ID": ["hazard identification", "risk assessment", "risk management"],
        "Housekeeping & Layout": ["housekeep", "layout", "congestion", "workplace layout",
                                    "storage", "access"],
        "Transportation": ["driving", "vehicle", "road", "transport", "marine", "vessel",
                            "aviation", "helicopter"],
        "PPE & Safety Controls": ["ppe", "personal protective", "safety control", "bypassing",
                                    "guard", "barrier", "isolation"],
        "Dropped Objects": ["dropped", "falling object", "dropped object"],
        "Manual Handling": ["manual handling", "lifting", "ergonomic", "body mechanics"],
    }

    cluster_counts = defaultdict(list)
    for cc, count in cc_counter.most_common():
        cc_lower = cc.lower()
        assigned = False
        for cluster_name, keywords in cluster_map.items():
            if any(kw in cc_lower for kw in keywords):
                cluster_counts[cluster_name].append((cc, count))
                assigned = True
                break
        if not assigned:
            cluster_counts["Other"].append((cc, count))

    out.append("### Clustered Groupings\n")
    for cluster_name in sorted(cluster_counts.keys(), key=lambda c: -sum(x[1] for x in cluster_counts[c])):
        items = cluster_counts[cluster_name]
        total_cluster = sum(x[1] for x in items)
        out.append(f"**{cluster_name}** (total: {total_cluster})")
        for cc, count in items:
            out.append(f"  - {cc}: {count}")
        out.append("")

    # Cross-tabulate top 15 CC vs IMPACT_TYPE
    top15_cc = [cc for cc, _ in cc_counter.most_common(15)]
    impact_counter = defaultdict(lambda: defaultdict(int))
    severity_counter = defaultdict(lambda: defaultdict(int))

    for r in records:
        cc = r["mf"].get("CASE_CATEGORIZATION", "").strip()
        if cc not in top15_cc:
            continue
        impact = r["ef"].get("IMPACT_TYPE", "Unknown") or "Unknown"
        impact_counter[cc][impact] += 1

        sev_raw = r["ef"].get("SEVERITY_DESC", "")
        sev = severity_bin(sev_raw)
        severity_counter[cc][sev] += 1

    # Get all impact types
    all_impacts = sorted(set(imp for d in impact_counter.values() for imp in d))

    out.append("### Top 15 CASE_CATEGORIZATION × IMPACT_TYPE\n")
    header = "| CASE_CATEGORIZATION | " + " | ".join(all_impacts) + " |"
    sep = "|" + "---|" * (len(all_impacts) + 1)
    out.append(header)
    out.append(sep)
    for cc in top15_cc:
        vals = " | ".join(str(impact_counter[cc].get(imp, 0)) for imp in all_impacts)
        out.append(f"| {cc[:60]} | {vals} |")
    out.append("")

    # Cross-tabulate top 15 CC vs SEVERITY
    all_sevs = sorted(set(s for d in severity_counter.values() for s in d))
    out.append("### Top 15 CASE_CATEGORIZATION × SEVERITY\n")
    header = "| CASE_CATEGORIZATION | " + " | ".join(all_sevs) + " |"
    sep = "|" + "---|" * (len(all_sevs) + 1)
    out.append(header)
    out.append(sep)
    for cc in top15_cc:
        vals = " | ".join(str(severity_counter[cc].get(s, 0)) for s in all_sevs)
        out.append(f"| {cc[:60]} | {vals} |")
    out.append("")


def analysis_3(records: List[Dict], out: list):
    """Causal Language in Narratives."""
    out.append("## Analysis 3: Causal Language in Narratives\n")

    causal_phrases = [
        "caused by", "due to", "resulted in", "led to", "because",
        "as a result", "contributing factor", "root cause", "failure of",
        "attributed to", "consequence of", "triggered by", "stemming from",
        "originating from", "linked to",
    ]

    total = len(records)
    phrase_counts = {}
    records_with_any = 0
    distribution = Counter()  # 0, 1, 2, 3+ causal phrases per narrative
    phrase_examples = defaultdict(list)  # phrase -> list of example sentences

    for r in records:
        narr = r.get("narrative", "")
        narr_lower = narr.lower()
        found_count = 0
        for phrase in causal_phrases:
            if phrase in narr_lower:
                phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1
                found_count += 1
                # Collect example sentences
                if len(phrase_examples[phrase]) < 10:
                    # Extract sentence containing the phrase
                    sentences = re.split(r'[.!?]+', narr)
                    for sent in sentences:
                        if phrase.lower() in sent.lower() and len(sent.strip()) > 20:
                            phrase_examples[phrase].append(sent.strip()[:200])
                            break
        if found_count > 0:
            records_with_any += 1
        bin_key = min(found_count, 3)
        distribution[bin_key] += 1

    out.append(f"Records with at least one causal phrase: {records_with_any} ({records_with_any/total*100:.1f}%)\n")

    out.append("### Causal Phrase Frequencies\n")
    out.append("| Phrase | Count | % Records |")
    out.append("|--------|-------|-----------|")
    for phrase in sorted(phrase_counts.keys(), key=lambda p: -phrase_counts[p]):
        count = phrase_counts[phrase]
        pct = count / total * 100
        out.append(f"| {phrase} | {count} | {pct:.1f}% |")
    out.append("")

    out.append("### Causal Phrase Distribution per Narrative\n")
    out.append("| Phrases per narrative | Count | % |")
    out.append("|----------------------|-------|---|")
    for k in sorted(distribution.keys()):
        label = f"{k}+" if k == 3 else str(k)
        out.append(f"| {label} | {distribution[k]} | {distribution[k]/total*100:.1f}% |")
    out.append("")

    # Top 5 phrase examples
    top5_phrases = sorted(phrase_counts.keys(), key=lambda p: -phrase_counts[p])[:5]
    out.append("### Example Sentences for Top 5 Causal Phrases\n")
    for phrase in top5_phrases:
        out.append(f"#### \"{phrase}\" ({phrase_counts[phrase]} occurrences)\n")
        for i, ex in enumerate(phrase_examples[phrase][:10], 1):
            out.append(f"{i}. {ex}")
        out.append("")


def analysis_4(records: List[Dict], out: list):
    """Metadata Field Coverage & Cross-tabulation."""
    out.append("## Analysis 4: Metadata Field Coverage & Cross-tabulation\n")

    total = len(records)

    # ENTITY_FACTS fields
    ef_fields = ["INCIDENT_TYPE", "IMPACT_TYPE", "SEVERITY_DESC", "LIKELIHOOD_RANGE",
                 "EVENT_DATETIME", "WORKPLACE", "CLIENT", "WORK_PROCESS"]
    # META_FACTS fields
    mf_fields = ["RISK_COLOR", "CASE_CATEGORIZATION", "GENERAL_BUSINESS_UNIT",
                 "SPECIFIC_BUSINESS_UNIT", "LIFE_SAVING_RULES", "LOSS_POTENTIAL"]

    out.append("### Field Coverage\n")
    out.append("| Field | Source | Non-null | % Coverage | Unique Values | Top 5 |")
    out.append("|-------|--------|----------|------------|---------------|-------|")

    for field in ef_fields:
        vals = [r["ef"].get(field, "") for r in records]
        non_null = sum(1 for v in vals if v)
        unique = len(set(v for v in vals if v))
        counter = Counter(v for v in vals if v)
        top5 = "; ".join(f"{k}({c})" for k, c in counter.most_common(5))
        out.append(f"| {field} | ENTITY_FACTS | {non_null} | {non_null/total*100:.1f}% | {unique} | {top5[:100]} |")

    for field in mf_fields:
        vals = [r["mf"].get(field, "") for r in records]
        non_null = sum(1 for v in vals if v)
        unique = len(set(v for v in vals if v))
        counter = Counter(v for v in vals if v)
        top5 = "; ".join(f"{k}({c})" for k, c in counter.most_common(5))
        out.append(f"| {field} | META_FACTS | {non_null} | {non_null/total*100:.1f}% | {unique} | {top5[:100]} |")
    out.append("")

    # WORKPLACE parsing
    out.append("### WORKPLACE Parsing\n")
    countries = Counter()
    cities = Counter()
    regions = Counter()
    for r in records:
        wp = r["ef"].get("WORKPLACE", "")
        if not wp:
            continue
        parsed = parse_workplace(wp)
        if parsed.get("country"):
            countries[parsed["country"]] += 1
        if parsed.get("city"):
            cities[parsed["city"]] += 1
        if parsed.get("region"):
            regions[parsed["region"]] += 1

    out.append("#### Top 20 Countries\n")
    out.append("| Rank | Country | Count | % |")
    out.append("|------|---------|-------|---|")
    for i, (c, count) in enumerate(countries.most_common(20), 1):
        out.append(f"| {i} | {c} | {count} | {count/total*100:.1f}% |")
    out.append("")

    out.append("#### Top 20 Cities\n")
    out.append("| Rank | City | Count | % |")
    out.append("|------|------|-------|---|")
    for i, (c, count) in enumerate(cities.most_common(20), 1):
        out.append(f"| {i} | {c} | {count} | {count/total*100:.1f}% |")
    out.append("")

    out.append("#### Top 10 Regions\n")
    out.append("| Rank | Region | Count | % |")
    out.append("|------|--------|-------|---|")
    for i, (c, count) in enumerate(regions.most_common(10), 1):
        out.append(f"| {i} | {c} | {count} | {count/total*100:.1f}% |")
    out.append("")

    # Cross-tabulations
    # INCIDENT_TYPE x IMPACT_TYPE
    it_ip = defaultdict(lambda: defaultdict(int))
    for r in records:
        it = r["ef"].get("INCIDENT_TYPE", "Unknown") or "Unknown"
        ip = r["ef"].get("IMPACT_TYPE", "Unknown") or "Unknown"
        it_ip[it][ip] += 1

    all_its = sorted(it_ip.keys())
    all_ips = sorted(set(ip for d in it_ip.values() for ip in d))

    out.append("### INCIDENT_TYPE × IMPACT_TYPE\n")
    header = "| INCIDENT_TYPE | " + " | ".join(all_ips) + " | Total |"
    sep = "|" + "---|" * (len(all_ips) + 2)
    out.append(header)
    out.append(sep)
    for it in all_its:
        vals = [str(it_ip[it].get(ip, 0)) for ip in all_ips]
        row_total = sum(it_ip[it].values())
        out.append(f"| {it} | " + " | ".join(vals) + f" | {row_total} |")
    out.append("")

    # Top 10 countries x IMPACT_TYPE
    top10_countries = [c for c, _ in countries.most_common(10)]
    ct_ip = defaultdict(lambda: defaultdict(int))
    for r in records:
        wp = r["ef"].get("WORKPLACE", "")
        if not wp:
            continue
        parsed = parse_workplace(wp)
        country = parsed.get("country", "")
        if not country or country not in top10_countries:
            continue
        ip = r["ef"].get("IMPACT_TYPE", "Unknown") or "Unknown"
        ct_ip[country][ip] += 1

    out.append("### Top 10 Countries × IMPACT_TYPE\n")
    header = "| Country | " + " | ".join(all_ips) + " | Total |"
    sep = "|" + "---|" * (len(all_ips) + 2)
    out.append(header)
    out.append(sep)
    for country in top10_countries:
        vals = [str(ct_ip[country].get(ip, 0)) for ip in all_ips]
        row_total = sum(ct_ip[country].values())
        out.append(f"| {country} | " + " | ".join(vals) + f" | {row_total} |")
    out.append("")

    # SEVERITY (binned) × INCIDENT_TYPE
    sev_it = defaultdict(lambda: defaultdict(int))
    for r in records:
        sev_raw = r["ef"].get("SEVERITY_DESC", "")
        sev = severity_bin(sev_raw)
        it = r["ef"].get("INCIDENT_TYPE", "Unknown") or "Unknown"
        sev_it[sev][it] += 1

    all_sevs = sorted(sev_it.keys())
    out.append("### SEVERITY (binned) × INCIDENT_TYPE\n")
    header = "| Severity | " + " | ".join(all_its) + " | Total |"
    sep = "|" + "---|" * (len(all_its) + 2)
    out.append(header)
    out.append(sep)
    for sev in all_sevs:
        vals = [str(sev_it[sev].get(it, 0)) for it in all_its]
        row_total = sum(sev_it[sev].values())
        out.append(f"| {sev} | " + " | ".join(vals) + f" | {row_total} |")
    out.append("")

    return countries, cities, regions


def analysis_5(records: List[Dict], eq_results: list, inj_results: list,
               countries_counter: Counter, out: list):
    """Queryable Combinations Matrix."""
    out.append("## Analysis 5: Queryable Combinations Matrix\n")

    # Top 15 equipment, top 10 injury/body part
    top15_eq = [t for t, _, _ in eq_results[:15]]
    top10_inj = [t for t, _, _ in inj_results[:10]]
    top10_countries = [c for c, _ in countries_counter.most_common(10)]

    # Pre-compile patterns
    eq_patterns = {t: re.compile(r"\b" + re.escape(t) + r"\b", re.IGNORECASE) for t in top15_eq}
    inj_patterns = {t: re.compile(r"\b" + re.escape(t) + r"\b", re.IGNORECASE) for t in top10_inj}

    # Causal patterns for step 4
    causal_re = re.compile(
        r"caused by|due to|resulted in|led to|because|as a result|contributing factor|root cause|failure of|attributed to",
        re.IGNORECASE,
    )

    # Step 2: Equipment × Injury matrix
    eq_inj_matrix = defaultdict(lambda: defaultdict(int))
    eq_inj_records = defaultdict(lambda: defaultdict(list))  # store record refs for step 4

    for r in records:
        narr = r.get("narrative", "")
        matched_eq = [t for t, pat in eq_patterns.items() if pat.search(narr)]
        matched_inj = [t for t, pat in inj_patterns.items() if pat.search(narr)]
        for eq in matched_eq:
            for inj in matched_inj:
                eq_inj_matrix[eq][inj] += 1
                eq_inj_records[eq][inj].append(r)

    out.append("### Step 2: Equipment × Injury/Body Part Co-occurrence Matrix\n")
    header = "| Equipment | " + " | ".join(top10_inj) + " |"
    sep = "|" + "---|" * (len(top10_inj) + 1)
    out.append(header)
    out.append(sep)
    for eq in top15_eq:
        vals = [str(eq_inj_matrix[eq].get(inj, 0)) for inj in top10_inj]
        out.append(f"| {eq} | " + " | ".join(vals) + " |")
    out.append("")

    # Step 3: Equipment × Country
    eq_country_matrix = defaultdict(lambda: defaultdict(int))
    for r in records:
        narr = r.get("narrative", "")
        wp = r["ef"].get("WORKPLACE", "")
        parsed = parse_workplace(wp)
        country = parsed.get("country", "")
        if not country or country not in top10_countries:
            continue
        matched_eq = [t for t, pat in eq_patterns.items() if pat.search(narr)]
        for eq in matched_eq:
            eq_country_matrix[eq][country] += 1

    out.append("### Step 3: Equipment × Top 10 Countries\n")
    header = "| Equipment | " + " | ".join(top10_countries) + " |"
    sep = "|" + "---|" * (len(top10_countries) + 1)
    out.append(header)
    out.append(sep)
    for eq in top15_eq:
        vals = [str(eq_country_matrix[eq].get(c, 0)) for c in top10_countries]
        out.append(f"| {eq} | " + " | ".join(vals) + " |")
    out.append("")

    # Step 4: Deep dive on pairs with >=20 co-occurrences
    out.append("### Step 4: Deep Dive on Viable Query Candidates (≥20 co-occurrences)\n")
    strong_candidates = []
    viable_candidates = []

    for eq in top15_eq:
        for inj in top10_inj:
            count = eq_inj_matrix[eq][inj]
            if count < 20:
                continue
            recs = eq_inj_records[eq][inj]

            # Causal language count
            causal_count = sum(1 for r in recs if causal_re.search(r.get("narrative", "")))

            # CASE_CATEGORIZATION distribution
            cc_dist = Counter(r["mf"].get("CASE_CATEGORIZATION", "Unknown") for r in recs)
            top3_cc = "; ".join(f"{k}({v})" for k, v in cc_dist.most_common(3))

            # Severity distribution
            sev_dist = Counter(severity_bin(r["ef"].get("SEVERITY_DESC", "")) for r in recs)
            sev_str = "; ".join(f"{k}({v})" for k, v in sorted(sev_dist.items()))

            label = "STRONG" if count >= 50 else "VIABLE"
            if count >= 50:
                strong_candidates.append((eq, inj, count, causal_count, top3_cc, sev_str))
            else:
                viable_candidates.append((eq, inj, count, causal_count, top3_cc, sev_str))

    out.append("| Status | Equipment | Injury/Body Part | Co-occurrences | With Causal Language | Top CASE_CATEGORIZATION | Severity Distribution |")
    out.append("|--------|-----------|------------------|----------------|---------------------|------------------------|----------------------|")
    for eq, inj, count, causal, cc, sev in sorted(strong_candidates + viable_candidates, key=lambda x: -x[2]):
        label = "**STRONG**" if count >= 50 else "VIABLE"
        out.append(f"| {label} | {eq} | {inj} | {count} | {causal} ({causal/count*100:.0f}%) | {cc[:80]} | {sev[:60]} |")
    out.append("")

    return strong_candidates, viable_candidates


def analysis_6(records: List[Dict], eq_results: list, inj_results: list,
               countries_counter: Counter, out: list):
    """Surface Form Variation Audit."""
    out.append("## Analysis 6: Surface Form Variation Audit\n")

    top20_eq = [t for t, _, _ in eq_results[:20]]
    top10_inj = [t for t, _, _ in inj_results[:10]]
    top10_cities = [c for c, _ in countries_counter.most_common(10)]

    # Equipment surface form variants
    equipment_variants = {
        "forklift": [r"forklift", r"fork lift", r"fork-lift", r"FLT", r"FORKLIFT", r"\d+[Tt]\s*forklift",
                     r"\d+\s*[Tt]on\s*forklift"],
        "crane": [r"crane", r"CRANE", r"overhead crane", r"gantry crane", r"mobile crane",
                  r"tower crane", r"crawler crane", r"pedestal crane"],
        "valve": [r"valve", r"VALVE", r"gate valve", r"ball valve", r"check valve",
                  r"relief valve", r"safety valve", r"control valve", r"choke valve"],
        "pump": [r"pump", r"PUMP", r"hydraulic pump", r"centrifugal pump", r"mud pump"],
        "pipe": [r"pipe", r"PIPE", r"pipeline", r"piping", r"pipe-line", r"pipework"],
        "hose": [r"hose", r"HOSE", r"hydraulic hose", r"hoses", r"hosepipe"],
        "scaffold": [r"scaffold", r"scaffolding", r"SCAFFOLD", r"scaffolds"],
        "ladder": [r"ladder", r"LADDER", r"ladders", r"step ladder", r"step-ladder", r"stepladder"],
        "harness": [r"harness", r"HARNESS", r"safety harness", r"body harness", r"fall harness"],
        "winch": [r"winch", r"WINCH", r"winches"],
        "drill": [r"drill", r"DRILL", r"drilling", r"drill bit", r"drill press"],
        "grinder": [r"grinder", r"GRINDER", r"grinding wheel", r"angle grinder", r"bench grinder"],
        "welder": [r"welder", r"WELDER", r"welding", r"weld", r"welding machine"],
        "vehicle": [r"vehicle", r"VEHICLE", r"vehicles", r"motor vehicle", r"company vehicle"],
        "container": [r"container", r"CONTAINER", r"containers", r"shipping container", r"ISO container"],
        "truck": [r"truck", r"TRUCK", r"trucks", r"lorry", r"HGV"],
        "cable": [r"cable", r"CABLE", r"cables", r"wire rope", r"steel cable"],
        "chain": [r"chain", r"CHAIN", r"chains", r"chain sling", r"chain hoist"],
        "bolt": [r"bolt", r"BOLT", r"bolts", r"bolting"],
        "tool": [r"tool", r"TOOL", r"tools", r"hand tool", r"power tool"],
    }

    # Injury surface form variants
    injury_variants = {
        "laceration": [r"laceration", r"lacerations", r"cut", r"cuts", r"gash"],
        "burn": [r"burn", r"burns", r"burned", r"burnt", r"scald", r"scalded"],
        "fracture": [r"fracture", r"fractured", r"fractures", r"broken bone", r"break"],
        "bruise": [r"bruise", r"bruised", r"bruises", r"bruising", r"contusion"],
        "sprain": [r"sprain", r"sprained", r"sprains", r"strain", r"strained"],
        "crush": [r"crush", r"crushed", r"crushing", r"crush injury"],
        "puncture": [r"puncture", r"punctured", r"punctures", r"pierced"],
        "abrasion": [r"abrasion", r"abrasions", r"graze", r"grazed", r"scrape", r"scraped", r"scratch"],
        "swelling": [r"swelling", r"swollen", r"swelled"],
        "pain": [r"pain", r"painful", r"ache", r"aching", r"sore", r"soreness"],
    }

    out.append("### Equipment Surface Form Variants\n")
    out.append("| Base Term | Variant | Count |")
    out.append("|-----------|---------|-------|")
    eq_frag_scores = []
    for base in top20_eq:
        variants = equipment_variants.get(base, [re.escape(base)])
        variant_counts = []
        for v in variants:
            pat = re.compile(r"\b" + v + r"\b", re.IGNORECASE)
            count = sum(1 for r in records if pat.search(r.get("narrative", "")))
            if count > 0:
                variant_counts.append((v, count))
        total_mentions = sum(c for _, c in variant_counts)
        n_forms = len(variant_counts)
        frag_score = n_forms / total_mentions if total_mentions > 0 else 0
        eq_frag_scores.append((base, n_forms, total_mentions, frag_score))
        for v, c in sorted(variant_counts, key=lambda x: -x[1]):
            out.append(f"| {base} | {v} | {c} |")
    out.append("")

    out.append("### Injury Surface Form Variants\n")
    out.append("| Base Term | Variant | Count |")
    out.append("|-----------|---------|-------|")
    inj_frag_scores = []
    for base in top10_inj[:10]:
        variants = injury_variants.get(base, [re.escape(base)])
        variant_counts = []
        for v in variants:
            pat = re.compile(r"\b" + v + r"\b", re.IGNORECASE)
            count = sum(1 for r in records if pat.search(r.get("narrative", "")))
            if count > 0:
                variant_counts.append((v, count))
        total_mentions = sum(c for _, c in variant_counts)
        n_forms = len(variant_counts)
        frag_score = n_forms / total_mentions if total_mentions > 0 else 0
        inj_frag_scores.append((base, n_forms, total_mentions, frag_score))
        for v, c in sorted(variant_counts, key=lambda x: -x[1]):
            out.append(f"| {base} | {v} | {c} |")
    out.append("")

    # Fragmentation scores
    out.append("### Fragmentation Scores\n")
    out.append("Higher = more surface form variation = better ER stress-test candidate\n")
    out.append("| Entity | Type | Distinct Forms | Total Mentions | Fragmentation Score |")
    out.append("|--------|------|---------------|----------------|---------------------|")
    all_frag = [(b, "Equipment", n, t, f) for b, n, t, f in eq_frag_scores] + \
               [(b, "Injury", n, t, f) for b, n, t, f in inj_frag_scores]
    all_frag.sort(key=lambda x: -x[4])
    for base, typ, n, t, f in all_frag:
        out.append(f"| {base} | {typ} | {n} | {t} | {f:.4f} |")
    out.append("")

    return all_frag


def summary_section(records, strong_candidates, viable_candidates, all_frag, out):
    """Summary & Query Design Implications."""
    out.append("## Summary & Query Design Implications\n")

    # 1. Top 10 strong query candidates
    out.append("### 1. Top 10 Strong Query Candidate Entity Combinations\n")
    out.append("These have the highest co-occurrence counts and serve as two-hop query anchors.\n")
    out.append("| Rank | Equipment | Injury/Body Part | Co-occurrences | Causal Coverage |")
    out.append("|------|-----------|------------------|----------------|-----------------|")
    all_cands = sorted(strong_candidates + viable_candidates, key=lambda x: -x[2])
    for i, (eq, inj, count, causal, cc, sev) in enumerate(all_cands[:10], 1):
        out.append(f"| {i} | {eq} | {inj} | {count} | {causal} ({causal/count*100:.0f}%) |")
    out.append("")

    # 2. Top 5 ER stress-test candidates
    out.append("### 2. Top 5 Entity Resolution Stress-Test Candidates\n")
    out.append("Highest fragmentation scores — most surface form variation.\n")
    out.append("| Rank | Entity | Type | Forms | Total Mentions | Frag Score |")
    out.append("|------|--------|------|-------|----------------|------------|")
    for i, (base, typ, n, t, f) in enumerate(all_frag[:5], 1):
        out.append(f"| {i} | {base} | {typ} | {n} | {t} | {f:.4f} |")
    out.append("")

    # 3. Causal query feasibility
    out.append("### 3. Causal Query Feasibility Assessment\n")
    causal_re = re.compile(
        r"caused by|due to|resulted in|led to|because|as a result|contributing factor|root cause|failure of|attributed to",
        re.IGNORECASE,
    )
    total = len(records)
    with_causal = sum(1 for r in records if causal_re.search(r.get("narrative", "")))
    out.append(f"- **{with_causal/total*100:.1f}%** of records contain explicit causal language")
    out.append(f"- Total records with causal phrases: {with_causal} / {total}")
    out.append("")

    # Which CC clusters have richest causal language
    cc_causal = defaultdict(lambda: [0, 0])  # [with_causal, total]
    for r in records:
        cc = r["mf"].get("CASE_CATEGORIZATION", "")
        if not cc:
            continue
        cc_causal[cc][1] += 1
        if causal_re.search(r.get("narrative", "")):
            cc_causal[cc][0] += 1

    out.append("**CASE_CATEGORIZATION clusters with richest causal language (top 15 by causal %):**\n")
    out.append("| CASE_CATEGORIZATION | Causal Records | Total | Causal % |")
    out.append("|---------------------|----------------|-------|----------|")
    cc_sorted = sorted(cc_causal.items(), key=lambda x: -x[1][0]/max(x[1][1],1) if x[1][1] >= 20 else 0)
    for cc, (c, t) in cc_sorted[:15]:
        if t >= 20:
            out.append(f"| {cc[:70]} | {c} | {t} | {c/t*100:.1f}% |")
    out.append("")

    # 4. Metadata gaps
    out.append("### 4. Metadata Gaps\n")
    out.append("Fields with coverage issues that limit query reliability:\n")
    ef_fields = ["INCIDENT_TYPE", "IMPACT_TYPE", "SEVERITY_DESC", "LIKELIHOOD_RANGE",
                 "EVENT_DATETIME", "WORKPLACE", "CLIENT", "WORK_PROCESS"]
    mf_fields = ["RISK_COLOR", "CASE_CATEGORIZATION", "GENERAL_BUSINESS_UNIT"]

    for field in ef_fields + mf_fields:
        source = "ef" if field in ef_fields else "mf"
        vals = [r[source].get(field, "") for r in records]
        non_null = sum(1 for v in vals if v)
        pct = non_null / total * 100
        if pct < 80:
            out.append(f"- **{field}**: {pct:.1f}% coverage ({total - non_null} missing)")
    out.append("")

    # 5. Recommended query design space
    out.append("### 5. Recommended Query Design Space\n")
    out.append("A shortlist of entity/relation/metadata combinations for the 30 benchmark queries:\n")

    out.append("#### Single-hop queries (10): Entity resolution + direct lookup")
    out.append("- Use high-fragmentation entities for ER stress tests")
    out.append("- Use high-frequency equipment terms for direct entity lookup")
    out.append("- Use WORKPLACE parsing for location queries")
    out.append("- Use INCIDENT_TYPE / IMPACT_TYPE for type classification queries\n")

    out.append("#### Two-hop queries (10): Entity-to-entity traversal")
    out.append("- Equipment → Injury/Body Part (use strong candidates from matrix)")
    out.append("- Equipment → Location (country-level)")
    out.append("- CASE_CATEGORIZATION → Equipment → Location")
    out.append("- Injury → Severity → CASE_CATEGORIZATION\n")

    out.append("#### Three-hop causal queries (7): Multi-entity causal chains")
    out.append("- Equipment failure → Causal mechanism → Injury → Severity")
    out.append("- Focus on CC clusters with high causal language density")
    out.append("- Use 'due to', 'caused by', 'resulted in' as relation signals\n")

    out.append("#### Similarity queries (3): Pattern matching across incidents")
    out.append("- Similar incidents by equipment + location + severity")
    out.append("- Similar incidents by CASE_CATEGORIZATION + injury type")
    out.append("- Similar causal chains across different locations\n")

    # Specific suggested combinations
    out.append("#### Specific Suggested Combinations\n")
    out.append("| # | Query Type | Entity/Relation Combination | Expected Data Support |")
    out.append("|---|------------|---------------------------|----------------------|")
    suggestions = [
        ("1", "1-hop ER", "forklift surface forms → canonical entity", "High fragmentation"),
        ("2", "1-hop ER", "crane surface forms → canonical entity", "Multiple compound forms"),
        ("3", "1-hop ER", "pipe/pipeline/piping → canonical entity", "High fragmentation"),
        ("4", "1-hop lookup", "All incidents at [top country]", "High count"),
        ("5", "1-hop lookup", "All incidents involving [top equipment]", "High count"),
        ("6", "1-hop lookup", "Incidents by CASE_CATEGORIZATION cluster", "Well-distributed"),
        ("7", "1-hop lookup", "Incidents by severity level", "5-bin distribution"),
        ("8", "1-hop ER", "burn/burned/burnt/scald → canonical injury", "Common injury type"),
        ("9", "1-hop lookup", "Incidents by IMPACT_TYPE", "Good coverage"),
        ("10", "1-hop ER", "laceration/cut/gash → canonical injury", "High overlap"),
    ]
    for row in suggestions:
        out.append(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} |")

    # Add two-hop suggestions from strong candidates
    for i, (eq, inj, count, causal, cc, sev) in enumerate(all_cands[:10], 11):
        out.append(f"| {i} | 2-hop | {eq} → involved → {inj} | {count} co-occurrences |")

    # Three-hop suggestions
    out.append(f"| 21 | 3-hop causal | Equipment failure → caused_by → [mechanism] → resulted_in → injury | Causal language in {with_causal/total*100:.0f}% records |")
    out.append("| 22 | 3-hop causal | [Equipment] → occurred_at → [Location] → involved → [Injury] | Cross-entity chain |")
    out.append("| 23 | 3-hop causal | [CC category] → caused_by → [Equipment] → resulted_in → [Severity] | CC-anchored chain |")
    out.append("| 24 | 3-hop causal | falls/slips → caused_by → [surface condition] → affected → [body part] | Rich CC cluster |")
    out.append("| 25 | 3-hop causal | mechanical failure → caused_by → [equipment] → resulted_in → [damage type] | Mechanical cluster |")
    out.append("| 26 | 3-hop causal | dropped object → caused_by → [lifting equipment] → affected → [body part] | Dropped object cluster |")
    out.append("| 27 | 3-hop causal | vehicle incident → occurred_at → [location] → resulted_in → [injury type] | Transportation cluster |")
    out.append("| 28 | similarity | Similar incidents: same equipment + same CC + different location | Pattern matching |")
    out.append("| 29 | similarity | Similar incidents: same injury + same severity + different equipment | Injury-anchored |")
    out.append("| 30 | similarity | Similar causal chains across regions | Cross-region patterns |")
    out.append("")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Loading records from {CSV_PATH}...")
    records = parse_records(CSV_PATH)
    print(f"Loaded {len(records)} records.")

    out = []
    out.append("# Query Design Data Exploration Report\n")
    out.append(f"**Dataset:** `{CSV_PATH.name}` — {len(records)} records\n")
    out.append("**Purpose:** Ground truth data profiling to support design of 30 Gold Standard benchmark queries.\n")
    out.append("---\n")

    # Analysis 1
    print("Running Analysis 1: Entity Landscape Profiling...")
    eq_results, inj_results = analysis_1(records, out)
    out.append("---\n")

    # Analysis 2
    print("Running Analysis 2: CASE_CATEGORIZATION Taxonomy...")
    analysis_2(records, out)
    out.append("---\n")

    # Analysis 3
    print("Running Analysis 3: Causal Language in Narratives...")
    analysis_3(records, out)
    out.append("---\n")

    # Analysis 4
    print("Running Analysis 4: Metadata Field Coverage...")
    countries, cities, regions = analysis_4(records, out)
    out.append("---\n")

    # Analysis 5
    print("Running Analysis 5: Queryable Combinations Matrix...")
    strong, viable = analysis_5(records, eq_results, inj_results, countries, out)
    out.append("---\n")

    # Analysis 6
    print("Running Analysis 6: Surface Form Variation Audit...")
    all_frag = analysis_6(records, eq_results, inj_results, countries, out)
    out.append("---\n")

    # Summary
    print("Writing Summary...")
    summary_section(records, strong, viable, all_frag, out)

    # Write output
    OUTPUT_PATH.write_text("\n".join(out), encoding="utf-8")
    print(f"\nReport written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
