"""
Quick feasibility check for graph connectivity and relation cleanliness.

Loads the filtered relationships parquet and computes two binary signals:
(1) graph connectivity — average degree below 2.0 signals a sparse graph where
GNN and reasoning workloads will struggle and entity resolution becomes the
priority; (2) relation cleanliness — more than 50 unique relation type strings
signals a messy schema requiring enforcement before query templates can be built.
Prints a VERDICT for each check.

Key findings: average degree < 2.0 (sparse) and unique relation types > 50
(messy) — both verdicts triggered on the raw Mistral output, confirming that
schema enforcement and ER were the two prerequisite work items before any
downstream task.

Decision: provided the go/no-go signal that gated all other v2 design work;
the two thresholds (avg_degree < 2.0, unique_rels > 50) became informal pass
criteria for the preflight gate in docs/preflight_gate.md.
"""

import pandas as pd

def litmus_test():
    print(">>> Running Feasibility Litmus Test...")
    
    try:
        # Load Relationships
        df = pd.read_parquet("fall2025/graphRAG/output/relationships_filtered.parquet")
        
        # 1. Check Connectivity (Is the graph dead?)
        node_count = len(set(df['source'].unique()) | set(df['target'].unique()))
        edge_count = len(df)
        avg_degree = edge_count / node_count
        
        print(f"\n[1] Graph Connectivity:")
        print(f"    - Nodes: {node_count}")
        print(f"    - Edges: {edge_count}")
        print(f"    - Avg Degree: {avg_degree:.2f}")
        
        if avg_degree < 2.0:
            print("    -> VERDICT: Graph is SPARSE. GNNs/Reasoning will struggle. Priority: Entity Resolution.")
        else:
            print("    -> VERDICT: Graph is CONNECTED. Reasoning is feasible.")

        # 2. Check Relation Chaos (Can we use templates?)
        rel_counts = df['description'].value_counts()
        top_rels = rel_counts.head(10)
        unique_rels = len(rel_counts)
        
        print(f"\n[2] Relationship Cleanliness:")
        print(f"    - Unique Relation Types: {unique_rels}")
        print("    - Top 5 Relations:")
        print(top_rels.head(5).to_string())
        
        if unique_rels > 50:
            print("    -> VERDICT: Relations are MESSY (Too many types). Priority: Schema Enforcement (Objective 1).")
        else:
            print("    -> VERDICT: Relations are CLEAN. You can build Query Templates immediately.")

    except Exception as e:
        print(f"Error reading files: {e}")

if __name__ == "__main__":
    litmus_test()
