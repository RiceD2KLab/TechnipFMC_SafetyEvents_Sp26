#!/usr/bin/env python3
"""
Comprehensive evaluation of five entity resolution strategies on real data.

Tests approaches from Section 12 of the Strategic Assessment: (A) incident
co-occurrence as an ER signal, (B) transitive closure on high-confidence fuzzy
pairs, candidate quality analysis identifying problematic patterns (UNKNOWN
entities, equipment number mismatches, cross-country location pairs), (D) org
suffix normalization, and (D) location structure parsing. For each approach
computes precision indicators and estimates realistic degree improvement from
conservatively safe merges only.

Critical findings: 81.3% equipment false positive rate when numbers differ;
conservative safe merges (score >= 0.95 with matching numbers) cover only 1.2%
of the merges needed to reach average degree 4.0; co-occurrence signal is weak
(few pairs share 3+ incidents); org normalization yields exact matches for a
meaningful subset of organization pairs.

Decision: ER alone is insufficient to reach connectivity targets; equipment
number-based filtering must be strict (num_jaccard >= 0.8) to avoid false
positive merges; results set the expectation that v2 must look beyond ER for
connectivity improvement.
"""

import pandas as pd
import json
from collections import defaultdict, Counter
from pathlib import Path
import re

BASE = Path(__file__).parent.parent.parent  # repo root
OUTPUT_DIR = BASE / "fall2025" / "graphRAG" / "output"
EDA_DIR = BASE / "eda"

def load_data():
    """Load all required data files"""
    print("Loading data...")

    # Load incident triples
    triples = pd.read_csv(OUTPUT_DIR / "incident_triples.csv")
    print(f"  Incident triples: {len(triples):,} rows, {triples['incident_id'].nunique():,} unique incidents")

    # Load fuzzy match candidates
    candidates = pd.read_csv(EDA_DIR / "fuzzy_match_candidates_training.csv")
    print(f"  Fuzzy candidates: {len(candidates):,} pairs")

    # Load entities
    entities = pd.read_parquet(OUTPUT_DIR / "entities_filtered.parquet")
    print(f"  Entities: {len(entities):,} total")

    # Load relationships
    rels = pd.read_parquet(OUTPUT_DIR / "relationships_filtered.parquet")
    print(f"  Relationships: {len(rels):,} edges")

    return triples, candidates, entities, rels


def test_transitive_closure(candidates):
    """
    Approach B: Test transitive closure on high-confidence pairs
    """
    print("\n" + "="*60)
    print("APPROACH B: TRANSITIVE CLOSURE")
    print("="*60)

    # Filter to high-confidence pairs (score >= 0.95, num_jaccard >= 0.8)
    high_conf = candidates[
        (candidates['score'] >= 0.95) &
        (candidates['num_jaccard'] >= 0.8)
    ]
    print(f"High-confidence pairs (score>=0.95, num_jaccard>=0.8): {len(high_conf):,}")

    # Union-Find implementation
    parent = {}
    rank = {}

    def find(x):
        if x not in parent:
            parent[x] = x
            rank[x] = 0
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1
            return True
        return False

    # Apply unions
    merges = 0
    for _, row in high_conf.iterrows():
        if union(row['id_l'], row['id_r']):
            merges += 1

    # Count clusters
    clusters = defaultdict(set)
    for node in parent:
        clusters[find(node)].add(node)

    cluster_sizes = [len(c) for c in clusters.values()]
    multi_clusters = [s for s in cluster_sizes if s > 1]

    print(f"Direct pairs used: {len(high_conf):,}")
    print(f"Actual merges (unions): {merges:,}")
    print(f"Total clusters: {len(clusters):,}")
    print(f"Multi-node clusters (size > 1): {len(multi_clusters):,}")
    print(f"Max cluster size: {max(cluster_sizes) if cluster_sizes else 0}")
    print(f"Entities absorbed into clusters: {sum(multi_clusters):,}")

    # Calculate transitive pairs generated
    transitive_pairs = sum(s * (s-1) // 2 for s in multi_clusters)
    print(f"Transitive pairs generated: {transitive_pairs:,}")

    return {
        "direct_pairs": len(high_conf),
        "merges": merges,
        "clusters": len(clusters),
        "multi_clusters": len(multi_clusters),
        "max_cluster": max(cluster_sizes) if cluster_sizes else 0,
        "transitive_pairs": transitive_pairs
    }


def test_candidate_quality(candidates):
    """
    Evaluate quality of fuzzy match candidates - are they real matches?
    """
    print("\n" + "="*60)
    print("CANDIDATE QUALITY ANALYSIS")
    print("="*60)

    # Analyze by type
    type_stats = candidates.groupby('type').agg({
        'score': ['count', 'mean'],
        'num_jaccard': 'mean'
    }).round(3)
    type_stats.columns = ['count', 'avg_score', 'avg_num_jaccard']
    print("\nBy entity type:")
    print(type_stats.sort_values('count', ascending=False))

    # Check for problematic patterns
    print("\n--- Problematic Pattern Detection ---")

    # 1. "UNKNOWN" matches (likely false positives)
    unknown_matches = candidates[
        candidates['title_l'].str.contains('UNKNOWN', case=False, na=False) |
        candidates['title_r'].str.contains('UNKNOWN', case=False, na=False)
    ]
    print(f"Pairs containing 'UNKNOWN': {len(unknown_matches):,} ({100*len(unknown_matches)/len(candidates):.1f}%)")

    # 2. Different specific locations matched to generic
    location_pairs = candidates[candidates['type'] == 'LOCATION']
    generic_location = location_pairs[
        (location_pairs['title_l'].str.count(',') != location_pairs['title_r'].str.count(',')) |
        (location_pairs['title_l'].str.contains('UNKNOWN.*UNKNOWN.*UNKNOWN', case=False, na=False))
    ]
    print(f"Location pairs with generic/specific mismatch: {len(generic_location):,}")

    # 3. Organization suffix differences
    org_pairs = candidates[candidates['type'] == 'ORGANIZATION']
    suffix_pattern = r'\b(INC|LTD|CORP|PLC|LLC|CO)\b'
    org_suffix_diff = org_pairs[
        (org_pairs['title_l'].str.contains(suffix_pattern, case=False, na=False)) !=
        (org_pairs['title_r'].str.contains(suffix_pattern, case=False, na=False))
    ]
    print(f"Org pairs with suffix mismatch: {len(org_suffix_diff):,} (potentially valid merges)")

    # 4. Equipment with different numbers
    equip_pairs = candidates[candidates['type'] == 'EQUIPMENT']
    equip_diff_nums = equip_pairs[
        (equip_pairs['nums_l'].notna()) &
        (equip_pairs['nums_r'].notna()) &
        (equip_pairs['nums_l'] != equip_pairs['nums_r'])
    ]
    print(f"Equipment pairs with different numbers: {len(equip_diff_nums):,} (likely FALSE positives)")

    # Calculate "clean" candidates
    problematic = set(unknown_matches.index) | set(equip_diff_nums.index)
    clean_candidates = candidates[~candidates.index.isin(problematic)]
    print(f"\nClean candidates (excluding problematic): {len(clean_candidates):,}")

    return {
        "total": len(candidates),
        "unknown_matches": len(unknown_matches),
        "location_generic_specific": len(generic_location),
        "org_suffix_diff": len(org_suffix_diff),
        "equip_diff_nums": len(equip_diff_nums),
        "clean_candidates": len(clean_candidates)
    }


def test_cooccurrence(triples, candidates):
    """
    Approach A: Test incident co-occurrence patterns
    """
    print("\n" + "="*60)
    print("APPROACH A: INCIDENT CO-OCCURRENCE")
    print("="*60)

    # Build entity -> incidents mapping
    entity_incidents = defaultdict(set)
    for _, row in triples.iterrows():
        inc_id = row['incident_id']
        entity_incidents[row['source']].add(inc_id)
        entity_incidents[row['target']].add(inc_id)

    print(f"Entities with incident links: {len(entity_incidents):,}")

    # For each candidate pair, check co-occurrence
    cooccur_counts = []
    for _, row in candidates.iterrows():
        # Try to match by title (candidates have titles, triples have entity names)
        title_l = row['title_l']
        title_r = row['title_r']

        inc_l = entity_incidents.get(title_l, set())
        inc_r = entity_incidents.get(title_r, set())

        cooccur = len(inc_l & inc_r)
        cooccur_counts.append(cooccur)

    candidates_copy = candidates.copy()
    candidates_copy['cooccur'] = cooccur_counts

    # Analyze co-occurrence
    print(f"\nCo-occurrence distribution:")
    print(f"  0 incidents shared: {sum(1 for c in cooccur_counts if c == 0):,}")
    print(f"  1+ incidents shared: {sum(1 for c in cooccur_counts if c >= 1):,}")
    print(f"  3+ incidents shared: {sum(1 for c in cooccur_counts if c >= 3):,}")
    print(f"  5+ incidents shared: {sum(1 for c in cooccur_counts if c >= 5):,}")

    # High co-occurrence pairs
    high_cooccur = candidates_copy[candidates_copy['cooccur'] >= 3]
    print(f"\nHigh co-occurrence pairs (>=3 shared incidents): {len(high_cooccur):,}")
    if len(high_cooccur) > 0:
        print("Sample high co-occurrence pairs:")
        for _, row in high_cooccur.head(5).iterrows():
            print(f"  [{row['type']}] '{row['title_l'][:40]}' <-> '{row['title_r'][:40]}' (cooccur={row['cooccur']})")

    return {
        "pairs_checked": len(candidates),
        "zero_cooccur": sum(1 for c in cooccur_counts if c == 0),
        "one_plus_cooccur": sum(1 for c in cooccur_counts if c >= 1),
        "three_plus_cooccur": sum(1 for c in cooccur_counts if c >= 3),
        "five_plus_cooccur": sum(1 for c in cooccur_counts if c >= 5)
    }


def test_org_normalization(candidates):
    """
    Approach D: Test organization normalization rules
    """
    print("\n" + "="*60)
    print("APPROACH D: ORGANIZATION NORMALIZATION")
    print("="*60)

    org_pairs = candidates[candidates['type'] == 'ORGANIZATION'].copy()
    print(f"Organization pairs: {len(org_pairs):,}")

    def normalize_org(name):
        if pd.isna(name):
            return ""
        # Remove legal suffixes
        name = re.sub(r'\b(INC|LTD|CORP|PLC|LLC|CO|COMPANY|CORPORATION|LIMITED)\.?\b', '', str(name), flags=re.IGNORECASE)
        # Remove punctuation and extra spaces
        name = re.sub(r'[^\w\s]', '', name)
        name = ' '.join(name.upper().split())
        return name

    org_pairs['norm_l'] = org_pairs['title_l'].apply(normalize_org)
    org_pairs['norm_r'] = org_pairs['title_r'].apply(normalize_org)

    # Check how many become exact matches after normalization
    exact_after_norm = org_pairs[org_pairs['norm_l'] == org_pairs['norm_r']]
    print(f"Exact matches after normalization: {len(exact_after_norm):,}")

    if len(exact_after_norm) > 0:
        print("Sample normalized matches:")
        for _, row in exact_after_norm.head(5).iterrows():
            tl, tr, nl = row['title_l'], row['title_r'], row['norm_l']
            print(f"  '{tl}' <-> '{tr}' -> '{nl}'")

    return {
        "org_pairs": len(org_pairs),
        "exact_after_norm": len(exact_after_norm)
    }


def test_location_structure(candidates):
    """
    Approach D: Analyze location structure for code extraction
    """
    print("\n" + "="*60)
    print("APPROACH D: LOCATION STRUCTURE ANALYSIS")
    print("="*60)

    loc_pairs = candidates[candidates['type'] == 'LOCATION'].copy()
    print(f"Location pairs: {len(loc_pairs):,}")

    # Check for structured location patterns
    all_locs = set(loc_pairs['title_l'].tolist() + loc_pairs['title_r'].tolist())

    # Pattern: "CITY, REGION, COUNTRY, CONTINENT"
    structured = [l for l in all_locs if ',' in str(l)]
    unstructured = [l for l in all_locs if ',' not in str(l)]

    print(f"Unique locations: {len(all_locs):,}")
    print(f"  Structured (with commas): {len(structured):,}")
    print(f"  Unstructured: {len(unstructured):,}")

    # Check for UNKNOWN dominance
    unknown_locs = [l for l in all_locs if 'UNKNOWN' in str(l).upper()]
    print(f"  Containing 'UNKNOWN': {len(unknown_locs):,} ({100*len(unknown_locs)/len(all_locs):.1f}%)")

    # Look for location codes (TFMC###)
    code_pattern = r'TFMC\d+'
    coded_locs = [l for l in all_locs if re.search(code_pattern, str(l))]
    print(f"  With TFMC codes: {len(coded_locs):,}")

    # Check same-country pairs
    def extract_country(loc):
        if pd.isna(loc):
            return None
        parts = str(loc).split(',')
        if len(parts) >= 3:
            return parts[-2].strip().upper()
        return None

    loc_pairs['country_l'] = loc_pairs['title_l'].apply(extract_country)
    loc_pairs['country_r'] = loc_pairs['title_r'].apply(extract_country)

    same_country = loc_pairs[
        (loc_pairs['country_l'].notna()) &
        (loc_pairs['country_l'] == loc_pairs['country_r'])
    ]
    diff_country = loc_pairs[
        (loc_pairs['country_l'].notna()) &
        (loc_pairs['country_r'].notna()) &
        (loc_pairs['country_l'] != loc_pairs['country_r'])
    ]

    print(f"\nSame-country pairs: {len(same_country):,}")
    print(f"Different-country pairs: {len(diff_country):,} (likely FALSE positives)")

    return {
        "loc_pairs": len(loc_pairs),
        "unique_locs": len(all_locs),
        "structured": len(structured),
        "unknown_locs": len(unknown_locs),
        "coded_locs": len(coded_locs),
        "same_country": len(same_country),
        "diff_country": len(diff_country)
    }


def calculate_realistic_impact(candidates, rels):
    """
    Calculate realistic degree improvement based on clean merges
    """
    print("\n" + "="*60)
    print("REALISTIC IMPACT CALCULATION")
    print("="*60)

    # Current state
    nodes = set(rels['source'].tolist() + rels['target'].tolist())
    edges = len(rels)
    current_degree = edges / len(nodes)

    print(f"Current state:")
    print(f"  Nodes: {len(nodes):,}")
    print(f"  Edges: {edges:,}")
    print(f"  Avg Degree: {current_degree:.4f}")

    # Conservative estimate: only count truly safe merges
    # 1. Org normalization (suffix removal)
    org_pairs = candidates[candidates['type'] == 'ORGANIZATION']
    safe_org_merges = len(org_pairs[org_pairs['score'] >= 0.98])

    # 2. High-confidence non-location, non-equipment
    other_pairs = candidates[~candidates['type'].isin(['LOCATION', 'EQUIPMENT', 'ORGANIZATION'])]
    safe_other_merges = len(other_pairs[(other_pairs['score'] >= 0.98) & (other_pairs['num_jaccard'] >= 0.9)])

    # 3. Equipment same-number (not different numbers)
    equip_pairs = candidates[candidates['type'] == 'EQUIPMENT']
    safe_equip = equip_pairs[
        (equip_pairs['score'] >= 0.95) &
        ((equip_pairs['num_jaccard'] >= 0.9) | (equip_pairs['nums_l'].isna() & equip_pairs['nums_r'].isna()))
    ]
    safe_equip_merges = len(safe_equip)

    total_safe_merges = safe_org_merges + safe_other_merges + safe_equip_merges

    print(f"\nConservative safe merges:")
    print(f"  Org (suffix norm, score>=0.98): {safe_org_merges:,}")
    print(f"  Other (score>=0.98, num_jaccard>=0.9): {safe_other_merges:,}")
    print(f"  Equipment (score>=0.95, same/no nums): {safe_equip_merges:,}")
    print(f"  TOTAL: {total_safe_merges:,}")

    # Calculate impact
    # Each merge reduces nodes by 1 but keeps edges (redirected)
    new_nodes = len(nodes) - total_safe_merges
    new_degree = edges / new_nodes if new_nodes > 0 else 0

    print(f"\nProjected state (conservative):")
    print(f"  Nodes: {new_nodes:,}")
    print(f"  Avg Degree: {new_degree:.4f}")
    print(f"  Improvement: {100*(new_degree - current_degree)/current_degree:.2f}%")

    # Target check
    target_degree = 4.0
    merges_needed = len(nodes) - (edges / target_degree)
    print(f"\nTo reach avg degree 4.0:")
    print(f"  Merges needed: {merges_needed:,.0f}")
    print(f"  Current safe merges cover: {100*total_safe_merges/merges_needed:.1f}% of needed")

    return {
        "current_nodes": len(nodes),
        "current_edges": edges,
        "current_degree": current_degree,
        "safe_merges": total_safe_merges,
        "projected_nodes": new_nodes,
        "projected_degree": new_degree,
        "improvement_pct": 100*(new_degree - current_degree)/current_degree,
        "merges_needed_for_4": merges_needed
    }


def main():
    print("="*60)
    print("ENTITY RESOLUTION APPROACHES - REAL DATA TEST")
    print("="*60)

    triples, candidates, entities, rels = load_data()

    results = {}

    # Test each approach
    results['transitive_closure'] = test_transitive_closure(candidates)
    results['candidate_quality'] = test_candidate_quality(candidates)
    results['cooccurrence'] = test_cooccurrence(triples, candidates)
    results['org_normalization'] = test_org_normalization(candidates)
    results['location_structure'] = test_location_structure(candidates)
    results['realistic_impact'] = calculate_realistic_impact(candidates, rels)

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    print(f"""
KEY FINDINGS:
- Transitive closure generates {results['transitive_closure']['transitive_pairs']:,} pairs from {results['transitive_closure']['direct_pairs']:,} direct pairs
- {results['candidate_quality']['unknown_matches']:,} candidates contain 'UNKNOWN' (likely false positives)
- {results['candidate_quality']['equip_diff_nums']:,} equipment pairs have different numbers (false positives)
- Only {results['cooccurrence']['three_plus_cooccur']:,} pairs share 3+ incidents (co-occurrence signal weak)
- {results['org_normalization']['exact_after_norm']:,} org pairs become exact matches after normalization
- {results['location_structure']['diff_country']:,} location pairs cross countries (false positives)

REALISTIC IMPACT:
- Safe merges available: {results['realistic_impact']['safe_merges']:,}
- Projected degree: {results['realistic_impact']['current_degree']:.4f} -> {results['realistic_impact']['projected_degree']:.4f}
- Improvement: {results['realistic_impact']['improvement_pct']:.2f}%
- To reach degree 4.0: need {results['realistic_impact']['merges_needed_for_4']:,.0f} merges
- Current approach covers: {100*results['realistic_impact']['safe_merges']/results['realistic_impact']['merges_needed_for_4']:.1f}% of needed
""")

    # Save results
    output_path = EDA_DIR / "er_approaches_test_results.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to: {output_path}")

    return results


if __name__ == "__main__":
    main()
