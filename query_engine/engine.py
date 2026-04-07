"""CSV-driven query engine for benchmark queries.

Loads query definitions from a CSV file and dispatches to the appropriate
strategy: entity_filter, meta_filter, narrative_filter, intersect, crosstab,
spot_check, or custom.
"""

import csv
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .helpers import (
    find_entities_by_value,
    get_entities_for_incident,
    get_incident_property,
    get_incidents_for_entity,
    incidents_for_entity_filter,
    incidents_for_meta_filter,
    incidents_matching_narrative,
    parse_year,
    parse_yearmonth,
    safe_get_node_value,
)


# ── Data structures ──────────────────────────────────────────────────────

@dataclass
class QuerySpec:
    query_id: str
    name: str
    query_type: str
    strategy: str
    entity_filters: list       # [(type, regex, relation), ...]
    meta_filters: list         # [(field, op, value), ...]
    narrative_keywords: list
    match_any_keyword: bool
    require_connected: tuple   # (entity_type, relation) or None
    output_mode: str
    output_target: str
    output_top_n: int
    coverage_thresholds: tuple  # (full_threshold, partial_threshold)
    diagnosis_rule: str
    custom_fn: str
    ground_truth: set
    notes: str
    expected_count: int         # ground truth count, or None if unknown


# ── CSV parsing ──────────────────────────────────────────────────────────

def _parse_entity_filters(raw):
    """Parse 'TYPE:regex:RELATION;...' into [(type, regex, relation), ...]"""
    if not raw or not raw.strip():
        return []
    filters = []
    for part in raw.split(";"):
        part = part.strip()
        if not part:
            continue
        tokens = part.split(":")
        if len(tokens) >= 3:
            etype = tokens[0]
            relation = tokens[-1]
            regex = ":".join(tokens[1:-1])
            filters.append((etype, regex, relation))
    return filters


def _parse_meta_filters(raw):
    """Parse 'field op value;...' into [(field, op, value), ...]"""
    if not raw or not raw.strip():
        return []
    filters = []
    for part in raw.split(";"):
        part = part.strip()
        if not part:
            continue
        for op in (">=", "<=", "!=", "==", ">", "<", "contains"):
            if f" {op} " in part:
                lhs, rhs = part.split(f" {op} ", 1)
                filters.append((lhs.strip(), op, rhs.strip()))
                break
    return filters


def _parse_narrative_keywords(raw):
    """Parse 'kw1,kw2' or 'ANY:kw1,kw2' into (keywords, match_any)."""
    if not raw or not raw.strip():
        return [], False
    raw = raw.strip()
    if raw.startswith("ANY:"):
        return [k.strip() for k in raw[4:].split(",") if k.strip()], True
    return [k.strip() for k in raw.split(",") if k.strip()], False


def _parse_coverage_thresholds(raw):
    """Parse 'full:partial' into (full_threshold, partial_threshold)."""
    if not raw or not raw.strip():
        return (1, 0)
    parts = raw.strip().split(":")
    return (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)


def load_queries(csv_path):
    """Load benchmark queries from a CSV file."""
    specs = []
    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            entity_filters = _parse_entity_filters(
                row.get("entity_filters", ""))
            meta_filters = _parse_meta_filters(
                row.get("meta_filters", ""))
            keywords, match_any = _parse_narrative_keywords(
                row.get("narrative_keywords", ""))
            thresholds = _parse_coverage_thresholds(
                row.get("coverage_thresholds", ""))

            req_conn = None
            rc_raw = (row.get("require_connected") or "").strip()
            if rc_raw:
                rc_parts = rc_raw.split(":")
                if len(rc_parts) == 2:
                    req_conn = (rc_parts[0], rc_parts[1])

            ground_truth = set()
            gt_raw = (row.get("ground_truth") or "").strip()
            if gt_raw:
                ground_truth = {g.strip().lower() for g in gt_raw.split("|")}

            ec_raw = (row.get("expected_count") or "").strip()
            expected_count = None
            if ec_raw:
                try:
                    expected_count = int(ec_raw)
                except ValueError:
                    print(f"Warning: invalid expected_count "
                          f"'{ec_raw}' for {row['query_id']}")

            specs.append(QuerySpec(
                query_id=row["query_id"].strip(),
                name=row["name"].strip(),
                query_type=row["query_type"].strip(),
                strategy=row["strategy"].strip(),
                entity_filters=entity_filters,
                meta_filters=meta_filters,
                narrative_keywords=keywords,
                match_any_keyword=match_any,
                require_connected=req_conn,
                output_mode=(row.get("output_mode") or "").strip(),
                output_target=(row.get("output_target") or "").strip(),
                output_top_n=int(
                    (row.get("output_top_n") or "10").strip() or "10"),
                coverage_thresholds=thresholds,
                diagnosis_rule=(
                    row.get("diagnosis_rule") or "auto").strip(),
                custom_fn=(row.get("custom_fn") or "").strip(),
                ground_truth=ground_truth,
                notes=(row.get("notes") or "").strip(),
                expected_count=expected_count,
            ))
    return specs


# ── Incident filtering ───────────────────────────────────────────────────

def _get_filtered_incidents(spec, G, entities_df, metadata_df):
    """Apply all filters (entity, meta, narrative) and return
    (incident_set, all_entity_ids).
    """
    incident_sets = []
    all_entity_ids = []

    for etype, regex, relation in spec.entity_filters:
        incidents, entity_ids = incidents_for_entity_filter(
            G, entities_df, etype, regex, relation)
        incident_sets.append(incidents)
        all_entity_ids.extend(entity_ids)

    for field_name, op, value in spec.meta_filters:
        incidents = incidents_for_meta_filter(
            metadata_df, field_name, op, value)
        incident_sets.append(incidents)

    if spec.narrative_keywords:
        match_all = not spec.match_any_keyword
        narr_records = incidents_matching_narrative(
            metadata_df, spec.narrative_keywords, match_all=match_all)
        narr_incidents = {f"INCIDENT::{r}" for r in narr_records}
        incident_sets.append(narr_incidents)

    # Intersect all sets
    if not incident_sets:
        incidents = {n for n in G.nodes if n.startswith("INCIDENT::")}
    elif len(incident_sets) == 1:
        incidents = incident_sets[0]
    else:
        incidents = incident_sets[0]
        for s in incident_sets[1:]:
            incidents = incidents & s

    # require_connected filter
    if spec.require_connected:
        req_type, req_rel = spec.require_connected
        incidents = {
            inc_id for inc_id in incidents
            if get_entities_for_incident(
                G, inc_id, entity_type=req_type, relation_type=req_rel)
        }

    return incidents, all_entity_ids


# ── Output modes ─────────────────────────────────────────────────────────

def _output_count(spec, incidents, G):
    count = len(incidents)
    lines = [f"Matching incidents: {count}"]
    if incidents:
        lines.append(f"Sample: {sorted(incidents)[:5]}")
    return {"count": count, "detail_lines": lines,
            "result_summary": f"{count} incidents"}


def _output_aggregate(spec, incidents, G):
    target = spec.output_target
    gran = None
    m = re.match(r"(\w+)\[(\w+)\]:(\w+)", target)
    if m:
        etype, gran, relation = m.groups()
    else:
        parts = target.split(":")
        etype = parts[0]
        relation = parts[1] if len(parts) > 1 else None

    counts = Counter()
    for inc_id in incidents:
        if inc_id not in G:
            continue
        entities = get_entities_for_incident(
            G, inc_id, entity_type=etype, relation_type=relation)
        for ent in entities:
            if gran and G.nodes[ent].get("granularity") != gran:
                continue
            val = safe_get_node_value(G, ent)
            if val:
                counts[val] += 1

    top_n = counts.most_common(spec.output_top_n)
    lines = [
        f"Matching incidents: {len(incidents)}",
        f"Distinct {etype} values: {len(counts)}",
        f"Top {spec.output_top_n}:",
    ] + [f"  {val}: {cnt}" for val, cnt in top_n]

    count = len(top_n)
    summary = (f"{len(incidents)} incidents, "
               f"{len(counts)} {etype.lower()} values")
    if top_n:
        summary += f", top: {top_n[0][0]}"
    return {"count": count, "detail_lines": lines,
            "result_summary": summary, "top_n": top_n, "counts": counts}


def _output_count_by_year(spec, incidents, G):
    monthly = Counter()
    for inc_id in incidents:
        date = get_incident_property(G, inc_id, "reported_date")
        ym = parse_yearmonth(date)
        if ym:
            monthly[ym] += 1

    yearly = Counter()
    for ym, cnt in monthly.items():
        yearly[ym[:4]] += cnt

    lines = [
        f"Total incidents: {len(incidents)}",
        f"Months with data: {len(monthly)}",
        f"Yearly breakdown:",
    ] + [f"  {y}: {yearly[y]}" for y in sorted(yearly)]

    return {"count": len(monthly), "detail_lines": lines,
            "result_summary": (f"{len(incidents)} incidents "
                               f"across {len(monthly)} months")}


def _output_pairs(spec, incidents, G):
    targets = spec.output_target.split(",")
    if len(targets) != 2:
        return {"count": 0, "detail_lines": ["Invalid pairs target"],
                "result_summary": "error"}

    t1_parts = targets[0].strip().split(":")
    t2_parts = targets[1].strip().split(":")
    type1, rel1 = t1_parts[0], t1_parts[1]
    type2, rel2 = t2_parts[0], t2_parts[1]

    pair_counts = Counter()
    for inc_id in incidents:
        if inc_id not in G:
            continue
        ents1 = get_entities_for_incident(
            G, inc_id, entity_type=type1, relation_type=rel1)
        ents2 = get_entities_for_incident(
            G, inc_id, entity_type=type2, relation_type=rel2)
        for e1 in ents1:
            for e2 in ents2:
                v1 = safe_get_node_value(G, e1)
                v2 = safe_get_node_value(G, e2)
                if v1 and v2:
                    pair_counts[(v1, v2)] += 1

    top_n = pair_counts.most_common(spec.output_top_n)
    lines = [
        f"Matching incidents: {len(incidents)}",
        f"{type1}->{type2} pairs (top {spec.output_top_n}):",
    ] + [f"  {v1} -> {v2}: {cnt}" for (v1, v2), cnt in top_n]

    return {"count": len(top_n), "detail_lines": lines,
            "result_summary": (f"{len(incidents)} incidents, "
                               f"{len(pair_counts)} pairs")}


def _output_crosstab(spec, metadata_df):
    target = spec.output_target
    parts = target.split(":")
    if len(parts) != 2:
        return {"count": 0, "detail_lines": ["Invalid crosstab target"],
                "result_summary": "error"}

    field1, field2 = parts[0].strip(), parts[1].strip()

    if field1 == "year":
        col1 = metadata_df["reported_date"].apply(parse_year).astype(str)
        col1_name = "year"
    else:
        col1 = metadata_df[field1].astype(str)
        col1_name = field1

    if field2 == "year":
        col2 = metadata_df["reported_date"].apply(parse_year).astype(str)
    else:
        col2 = metadata_df[field2].astype(str)

    crosstab = defaultdict(Counter)
    null_count = 0
    for i in range(len(metadata_df)):
        v1 = str(col1.iloc[i])
        v2 = str(col2.iloc[i])
        if v1 in ("nan", "None", ""):
            null_count += 1
            v1 = "Unknown"
        if v2 in ("nan", "None", ""):
            v2 = "Unknown"
        crosstab[str(v1)][str(v2)] += 1

    all_v2 = sorted(set(v2 for c in crosstab.values() for v2 in c))
    lines = []
    if null_count:
        lines.append(
            f"{col1_name} null rate: {null_count}/{len(metadata_df)} "
            f"({100 * null_count / len(metadata_df):.1f}%)")
        lines.append("")

    header = f"| {col1_name} | " + " | ".join(all_v2) + " | Total |"
    sep = "|" + "|".join(["---"] * (len(all_v2) + 2)) + "|"
    lines.extend([header, sep])

    for v1 in sorted(crosstab,
                     key=lambda x: -sum(crosstab[x].values()))[:15]:
        row_vals = [str(crosstab[v1].get(v2, 0)) for v2 in all_v2]
        total = sum(crosstab[v1].values())
        lines.append(
            f"| {str(v1)[:40]} | " + " | ".join(row_vals) + f" | {total} |")

    return {"count": len(crosstab), "detail_lines": lines,
            "result_summary": (f"Crosstab: {len(crosstab)} {col1_name} "
                               f"values x {len(all_v2)} {field2} values")}


def _compute_output(spec, incidents, G, entities_df, metadata_df):
    dispatch = {
        "count_incidents": _output_count,
        "aggregate": _output_aggregate,
        "count_by_year": _output_count_by_year,
        "pairs": _output_pairs,
    }
    if spec.output_mode == "crosstab":
        return _output_crosstab(spec, metadata_df)
    fn = dispatch.get(spec.output_mode)
    if fn:
        return fn(spec, incidents, G)
    return {"count": 0,
            "detail_lines": [f"Unknown output_mode: {spec.output_mode}"]}


# ── Scoring ──────────────────────────────────────────────────────────────

def _score_coverage(spec, output):
    count = output.get("count", 0)
    full_thresh, partial_thresh = spec.coverage_thresholds
    if count >= full_thresh:
        return "\u2705"
    if count >= partial_thresh:
        return "\u26a0\ufe0f"
    return "\u274c"


def _determine_diagnosis(spec, entity_ids, output):
    rule = spec.diagnosis_rule
    if rule != "auto":
        return rule
    # auto: DATA_SPARSE when no results, CLEAN otherwise.
    # Queries needing ER_NEEDED have it set explicitly in CSV.
    if output.get("count", 0) == 0:
        return "DATA_SPARSE"
    return "CLEAN"


def _score_validation(spec, output):
    """Compare graph count vs expected ground truth count.

    Returns:
        str: VALIDATED (within 10%), CLOSE (within 25%), DRIFT (>25%),
             or "—" if no expected_count.
    """
    if spec.expected_count is None:
        return "—"
    expected = spec.expected_count
    # For count_incidents: use count directly
    # For aggregate/count_by_year: use incident count from detail
    actual = output.get("count", 0)
    # Try to extract incident count from detail for aggregate modes
    for line in output.get("detail_lines", []):
        if line.startswith("Matching incidents:"):
            try:
                actual = int(line.split(":")[1].strip())
            except (ValueError, IndexError):
                pass
            break
        if line.startswith("Total incidents:"):
            try:
                actual = int(line.split(":")[1].strip())
            except (ValueError, IndexError):
                pass
            break
    if expected == 0:
        return "VALIDATED" if actual == 0 else "DRIFT"
    pct_diff = abs(actual - expected) / expected
    if pct_diff <= 0.10:
        return "VALIDATED"
    if pct_diff <= 0.25:
        return "CLOSE"
    return "DRIFT"


# ── Spot-check strategy ─────────────────────────────────────────────────

def _execute_spot_check(spec, G, entities_df):
    target = spec.output_target
    # Format: INCIDENT::ID:ENTITY_TYPE:RELATION
    # After split(":"): ["INCIDENT","","ID","TYPE","REL"]
    parts = target.split(":")
    inc_id = f"INCIDENT::{parts[2]}"
    etype = parts[3]
    relation = parts[4]

    entities = get_entities_for_incident(
        G, inc_id, entity_type=etype, relation_type=relation)
    found_vals = sorted(
        v for e in entities if e in G
        for v in [safe_get_node_value(G, e)] if v is not None)
    found_lower = {v.lower() for v in found_vals}

    # Bidirectional substring match: a GT term is satisfied if any extracted
    # value contains it OR is contained within it.  This handles morphological
    # variants ("lip"/"lips"/"lower lip") and qualified spans
    # ("fracture"/"confirmed fracture") that exact matching would reject.
    def _gt_matched(gt_term: str) -> bool:
        gt = gt_term.lower()
        return any(gt in fv or fv in gt for fv in found_lower)

    matched_gt = {gt for gt in spec.ground_truth if _gt_matched(gt)}
    missing = spec.ground_truth - matched_gt
    matched_found = {fv for fv in found_lower
                     if any(gt.lower() in fv or fv in gt.lower()
                            for gt in spec.ground_truth)}
    extra = found_lower - matched_found

    lines = [
        f"{etype} found for {inc_id}: {found_vals}",
        f"Ground truth: {sorted(spec.ground_truth)}",
        f"Missing: {sorted(missing) if missing else 'none'}",
        f"Extra (unexpected): {sorted(extra) if extra else 'none'}",
    ]

    count = len(matched_gt) if spec.ground_truth else len(found_vals)
    coverage = _score_coverage(spec, {"count": count})
    diag = "EXTRACTION_GAP" if missing else "CLEAN"

    return {
        "coverage": coverage,
        "diagnosis": diag,
        "result_summary": f"{len(found_vals)} items: {found_vals}",
        "detail": "\n".join(lines),
    }


# ── Graph traversal strategy ─────────────────────────────────────────────

def _execute_traverse(spec, G, entities_df, relations_df):
    """Walk the graph following a path pattern and collect endpoints.

    output_target format for traverse:
        START_TYPE:start_pattern>REL1>REL2>...>COLLECT_TYPE

    Examples:
        EQUIPMENT:crane>INVOLVED>INCIDENT>RESULTED_IN>INJURY_TYPE
        INJURY_TYPE:fracture>RESULTED_IN>INCIDENT>INVOLVED>EQUIPMENT
        EVENT:corrosion>CAUSAL>EVENT>CAUSAL>INJURY

    The traversal starts from entities matching START_TYPE:start_pattern,
    follows edges by relation type at each hop, and collects entity values
    at the final COLLECT_TYPE.  Direction is followed as the graph stores it
    (source→target for most relations; reversed via predecessors when needed).
    """
    target = spec.output_target
    hops = target.split(">")
    if len(hops) < 3:
        return {"count": 0,
                "detail_lines": [f"Invalid traverse path: {target}"],
                "result_summary": "error: need at least START>REL>END"}

    # Parse start: TYPE:pattern
    start_parts = hops[0].split(":")
    start_type = start_parts[0]
    start_pattern = ":".join(start_parts[1:]) if len(start_parts) > 1 else ".*"

    # Remaining hops alternate: RELATION, NODE_TYPE, RELATION, NODE_TYPE, ...
    # The last element is the collection type
    path_steps = hops[1:]  # [REL1, TYPE1, REL2, TYPE2, ..., COLLECT_TYPE]

    # Find start nodes
    start_nodes = find_entities_by_value(entities_df, start_type, start_pattern)
    if not start_nodes:
        return {"count": 0,
                "detail_lines": [f"No {start_type} matching '{start_pattern}'"],
                "result_summary": f"0 start nodes for {start_type}:{start_pattern}"}

    # Walk the graph
    current_nodes = set(n for n in start_nodes if n in G)
    walk_log = [f"Start: {len(current_nodes)} {start_type} nodes "
                f"matching '{start_pattern}'"]

    i = 0
    while i < len(path_steps) - 1:  # -1 because last is collect type
        relation = path_steps[i]
        next_type = path_steps[i + 1] if i + 1 < len(path_steps) else None

        next_nodes = set()
        for node in current_nodes:
            # Try forward edges (node → neighbor)
            for nbr in G.successors(node):
                edge_rel = G.edges[node, nbr].get("relation", "")
                if edge_rel == relation:
                    if next_type is None or G.nodes[nbr].get(
                            "entity_type", "") == next_type:
                        next_nodes.add(nbr)
            # Try reverse edges (neighbor → node) for relations like
            # RESULTED_IN where we want to go from INJURY_TYPE back to INCIDENT
            for nbr in G.predecessors(node):
                edge_rel = G.edges[nbr, node].get("relation", "")
                if edge_rel == relation:
                    if next_type is None or G.nodes[nbr].get(
                            "entity_type", "") == next_type:
                        next_nodes.add(nbr)

        walk_log.append(
            f"  --{relation}--> {next_type or '?'}: {len(next_nodes)} nodes")
        current_nodes = next_nodes
        i += 2  # skip relation + type

    # If odd number of remaining steps, last is just the collect type filter
    collect_type = path_steps[-1]
    if collect_type != "?" and collect_type != "*":
        current_nodes = {n for n in current_nodes
                         if G.nodes[n].get("entity_type", "") == collect_type}

    # Collect and count values
    value_counts = Counter()
    for node in current_nodes:
        val = safe_get_node_value(G, node)
        if val:
            value_counts[val] += 1

    top_n = value_counts.most_common(spec.output_top_n)
    walk_log.extend([
        f"  Final: {len(current_nodes)} {collect_type} nodes, "
        f"{len(value_counts)} distinct values",
        "",
        f"Top {spec.output_top_n}:",
    ] + [f"  {val}: {cnt}" for val, cnt in top_n])

    count = len(value_counts)
    coverage = _score_coverage(spec, {"count": count})
    diag = spec.diagnosis_rule if spec.diagnosis_rule != "auto" else (
        "CLEAN" if count > 0 else "DATA_SPARSE")

    return {
        "coverage": coverage,
        "diagnosis": diag,
        "result_summary": (f"{len(current_nodes)} endpoints, "
                           f"{len(value_counts)} distinct {collect_type}"),
        "detail": "\n".join(walk_log),
    }


# ── Main dispatch ────────────────────────────────────────────────────────

def execute_query(spec, G, entities_df, relations_df, metadata_df,
                  custom_registry=None, results=None):
    """Execute a single QuerySpec and return a result dict."""
    t0 = time.time()

    if spec.strategy == "custom":
        if custom_registry and spec.custom_fn in custom_registry:
            result = custom_registry[spec.custom_fn](
                spec, G, entities_df, relations_df, metadata_df,
                results=results)
        else:
            available = list(custom_registry.keys()) \
                if custom_registry else []
            result = {
                "coverage": "\u274c",
                "diagnosis": "MISSING_FN",
                "result_summary":
                    f"custom_fn '{spec.custom_fn}' not found",
                "detail": f"Available: {available}",
            }
        result["validation"] = "—"
        result["elapsed"] = f"{time.time() - t0:.1f}s"
        return result

    if spec.strategy == "spot_check":
        result = _execute_spot_check(spec, G, entities_df)
        result["validation"] = "—"
        result["elapsed"] = f"{time.time() - t0:.1f}s"
        return result

    if spec.strategy == "traverse":
        result = _execute_traverse(spec, G, entities_df, relations_df)
        result["validation"] = _score_validation(spec, result)
        result["elapsed"] = f"{time.time() - t0:.1f}s"
        return result

    # Crosstab uses metadata directly (no incident filtering)
    if spec.output_mode == "crosstab":
        output = _output_crosstab(spec, metadata_df)
        coverage = _score_coverage(spec, output)
        diag = spec.diagnosis_rule if spec.diagnosis_rule != "auto" \
            else "CLEAN"
        result = {
            "coverage": coverage,
            "diagnosis": diag,
            "result_summary": output["result_summary"],
            "detail": "\n".join(output["detail_lines"]),
            "validation": _score_validation(spec, output),
        }
        result["elapsed"] = f"{time.time() - t0:.1f}s"
        return result

    # Standard strategies: entity_filter, meta_filter, narrative_filter,
    # intersect — all use the same flow
    incidents, entity_ids = _get_filtered_incidents(
        spec, G, entities_df, metadata_df)
    output = _compute_output(spec, incidents, G, entities_df, metadata_df)
    coverage = _score_coverage(spec, output)
    diagnosis = _determine_diagnosis(spec, entity_ids, output)

    result = {
        "coverage": coverage,
        "diagnosis": diagnosis,
        "result_summary": output.get(
            "result_summary", f"{output.get('count', 0)} results"),
        "detail": "\n".join(output.get("detail_lines", [])),
        "validation": _score_validation(spec, output),
    }
    result["elapsed"] = f"{time.time() - t0:.1f}s"
    return result


def run_all_queries(specs, G, entities_df, relations_df, metadata_df,
                    custom_registry=None):
    """Execute all query specs in order and return results dict."""
    results = {}
    for spec in specs:
        print(f"  Running {spec.query_id}: {spec.name}...")
        try:
            result = execute_query(
                spec, G, entities_df, relations_df, metadata_df,
                custom_registry=custom_registry, results=results)
        except Exception as exc:
            result = {
                "coverage": "❌",
                "diagnosis": "ERROR",
                "result_summary": f"Crashed: {exc}",
                "detail": "",
                "elapsed": "0.0s",
            }
        result["name"] = spec.name
        result["type"] = spec.query_type
        results[spec.query_id] = result
        validation = result.get('validation', '—')
        print(f"    -> {result.get('coverage', '?')} | "
              f"{result.get('diagnosis', '?')} | {validation} "
              f"({result.get('elapsed', '?')})")
    return results
