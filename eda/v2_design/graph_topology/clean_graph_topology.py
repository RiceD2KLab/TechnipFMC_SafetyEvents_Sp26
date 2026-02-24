"""
Canonical relation mapping and entity deduplication on raw GraphRAG Mistral output.

Applies a keyword-based relation canonicalization map (e.g. CAUSE/LED_TO/DUE_TO
all collapse to CAUSED_BY) and deduplicates entities by normalizing titles to
uppercase alphanumeric form, keeping the highest-degree representative for each
normalized key. Reads from graphRAG/output and writes cleaned parquet files to
graphRAG/output_cleaned.

Key findings: 1,073 entity merges achieved via text normalization alone;
relation types reduced from thousands of free-text strings to a small canonical
set; average degree increased after edge remapping to clean endpoints.

Decision: established the relation canonicalization strategy and title
normalization logic that became the foundation of the v2 pipeline guardrail.
"""

import pandas as pd
import re
from pathlib import Path

# --- Configuration ---
INPUT_DIR = Path("graphRAG/output")
OUTPUT_DIR = Path("graphRAG/output_cleaned")
OUTPUT_DIR.mkdir(exist_ok=True)

# Canonical Relations Mapping (The "Schema")
# We map keywords found in garbage relations to a clean standard set.
RELATION_MAP = {
    "CAUSE": "CAUSED_BY",
    "LED_TO": "CAUSED_BY",
    "RESULT": "RESULTED_IN",
    "DUE_TO": "CAUSED_BY",
    "CONTRIB": "CAUSED_BY",
    "INVOLV": "INVOLVED",
    "OCCUR": "OCCURRED_AT",
    "LOCAT": "OCCURRED_AT",
    "PLACE": "OCCURRED_AT",
    "DURING": "OCCURRED_AT",
    "WHEN": "OCCURRED_AT",
    "TIME": "OCCURRED_AT",
    "DAMAGE": "RESULTED_IN",
    "INJUR": "RESULTED_IN",
    "HURT": "RESULTED_IN",
    "AFFECT": "AFFECTED",
    "IMPACT": "AFFECTED",
    "USE": "USED_IN",
    "UTIL": "USED_IN",
    "OPERAT": "INVOLVED",
    "OWN": "INVOLVED",
}

def normalize_text(text):
    if not isinstance(text, str): return ""
    # Uppercase, remove special chars, normalize whitespace
    text = text.upper()
    text = re.sub(r'[^A-Z0-9\s]', ' ', text) # Replace punctuation with space
    text = re.sub(r'\s+', ' ', text).strip() # Collapse whitespace
    return text

def clean_topology():
    print(">>> Starting Graph Topology Cleanup...")
    
    # 1. Load Data
    print("Loading Parquet files...")
    rels = pd.read_parquet(INPUT_DIR / "relationships_filtered.parquet")
    ents = pd.read_parquet(INPUT_DIR / "entities_filtered.parquet")
    
    print(f"Original Nodes: {len(ents)}")
    print(f"Original Edges: {len(rels)}")
    print(f"Original Relation Types: {rels['description'].nunique()}")

    # 2. Clean Relations (The "Garbage Collection")
    print("\n--- Cleaning Relations ---")
    
    def map_relation(desc):
        norm = normalize_text(desc)
        for keyword, canonical in RELATION_MAP.items():
            if keyword in norm:
                return canonical
        return "INVOLVED"

    rels['clean_description'] = rels['description'].apply(map_relation)
    
    # Show improvement
    print("Top 10 New Relations:")
    print(rels['clean_description'].value_counts().head(10))
    print(f"New Relation Types count: {rels['clean_description'].nunique()}")

    # 3. Clean Entities (The "Entity Resolution" Lite)
    print("\n--- Cleaning Entities ---")
    
    # Normalize titles
    ents['clean_title'] = ents['title'].apply(normalize_text)
    
    # Create a mapping from Old ID -> New Clean Title
    # Note: Real ER needs a unique ID per 'concept', here we use the clean title as the ID
    # This effectively merges "Pump A" and "Pump-A" into "PUMP A"
    
    # We need to preserve the metadata of the 'best' candidate for each clean title
    # For simplicity, we take the one with the highest degree
    ents = ents.sort_values('degree', ascending=False)
    deduped_ents = ents.drop_duplicates(subset='clean_title', keep='first').copy()
    
    print(f"Nodes after Deduplication: {len(deduped_ents)}")
    print(f"Nodes Merged: {len(ents) - len(deduped_ents)}")

    # Create mapping: Original Title -> Clean Title
    # Note: We need to map the SOURCE and TARGET in relationships
    # The relationships file uses 'title' strings in 'source' and 'target' cols (based on previous file inspection)
    
    # Map raw text in relationships to the clean text
    rels['clean_source'] = rels['source'].apply(normalize_text)
    rels['clean_target'] = rels['target'].apply(normalize_text)
    
    # Filter edges where source or target effectively disappeared (shouldn't happen with string norm)
    valid_nodes = set(deduped_ents['clean_title'])
    mask = rels['clean_source'].isin(valid_nodes) & rels['clean_target'].isin(valid_nodes)
    clean_rels = rels[mask].copy()
    
    # 4. Connectivity Check
    print("\n--- Final Metrics ---")
    
    node_count = len(deduped_ents)
    edge_count = len(clean_rels)
    avg_degree = edge_count / node_count if node_count > 0 else 0
    
    print(f"Final Nodes: {node_count}")
    print(f"Final Edges: {edge_count}")
    print(f"Final Avg Degree: {avg_degree:.2f}")
    
    # 5. Save
    print("\nSaving to 'graphRAG/output_cleaned/'...")
    deduped_ents.to_parquet(OUTPUT_DIR / "entities.parquet")
    clean_rels.to_parquet(OUTPUT_DIR / "relationships.parquet")
    print("Done.")

if __name__ == "__main__":
    clean_topology()
