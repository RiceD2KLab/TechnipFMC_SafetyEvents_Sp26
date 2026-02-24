"""Report generation for benchmark results."""

from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


def generate_report(results, G, entities_df, metadata_df, output_path):
    """Generate benchmark_results.md from query results."""
    lines = []
    lines.append("# L1 Benchmark Query Results")
    lines.append("")
    lines.append(f"**Generated:** {date.today().isoformat()}")
    lines.append(
        f"**Graph:** {G.number_of_nodes():,} nodes, "
        f"{G.number_of_edges():,} edges")
    inc_count = len(
        entities_df[entities_df.entity_type == "INCIDENT"])
    lines.append(
        f"**Records:** {len(metadata_df):,} metadata rows, "
        f"{inc_count:,} incident nodes")
    lines.append(
        "**Layer:** L1 only (pre-ER, pre-Layer 2 causal enrichment)")
    lines.append("")

    # ── Summary Table ────────────────────────────────────────────────
    lines.append("## 1. Summary Table")
    lines.append("")
    lines.append(
        "| ID | Query | Type | Coverage | Result | Diagnosis |")
    lines.append(
        "|------|-------|------|:--------:|--------|-----------|")

    for qid in sorted(results.keys()):
        r = results[qid]
        lines.append(
            f"| {qid} | {r['name']} | {r['type']} | "
            f"{r['coverage']} | {r['result_summary']} | "
            f"{r['diagnosis']} |")
    lines.append("")

    # ── Coverage summary ─────────────────────────────────────────────
    full = sum(1 for r in results.values()
               if r["coverage"] == "\u2705")
    partial = sum(1 for r in results.values()
                  if r["coverage"] == "\u26a0\ufe0f")
    fail = sum(1 for r in results.values()
               if r["coverage"] == "\u274c")
    lines.append(
        f"**Overall:** {full} \u2705 FULL / {partial} \u26a0\ufe0f "
        f"PARTIAL / {fail} \u274c FAIL out of {len(results)} queries")
    lines.append("")

    # ── Diagnosis summary ────────────────────────────────────────────
    diag_counts = Counter(r["diagnosis"] for r in results.values())
    lines.append("**Diagnosis breakdown:**")
    for diag, cnt in diag_counts.most_common():
        lines.append(f"- {diag}: {cnt}")
    lines.append("")

    # ── Per-Query Detail ─────────────────────────────────────────────
    lines.append("## 2. Per-Query Details")
    lines.append("")

    for qid in sorted(results.keys()):
        r = results[qid]
        lines.append(f"### {qid}: {r['name']}")
        lines.append(
            f"**Type:** {r['type']} | **Coverage:** {r['coverage']} | "
            f"**Diagnosis:** {r['diagnosis']} | "
            f"**Time:** {r.get('elapsed', '?')}")
        lines.append("")
        lines.append("```")
        lines.append(r["detail"])
        lines.append("```")
        lines.append("")

    # ── Ablation Prediction ──────────────────────────────────────────
    lines.append("## 3. Ablation Prediction Table")
    lines.append("")

    type_results = defaultdict(lambda: {"total": 0, "full": 0})
    for r in results.values():
        t = r["type"]
        type_results[t]["total"] += 1
        if r["coverage"] == "\u2705":
            type_results[t]["full"] += 1

    lines.append(
        "| Query Type | Count | L1 Baseline | "
        "After ER (predicted) | After L2 (predicted) |")
    lines.append(
        "|-----------|:-----:|:-----------:|"
        ":-------------------:|:-------------------:|")

    er_boost = {"Single-hop": 1, "Aggregation": 0, "Multi-hop": 1,
                "Global": 0, "Conjunctive": 0}
    l2_boost = {"Single-hop": 0, "Aggregation": 0, "Multi-hop": 0,
                "Global": 0, "Conjunctive": 2}

    for qtype in ["Single-hop", "Aggregation", "Multi-hop",
                   "Global", "Conjunctive"]:
        tr = type_results[qtype]
        l1 = tr["full"]
        total = tr["total"]
        er_needed = sum(
            1 for r in results.values()
            if r["type"] == qtype
            and r["diagnosis"] == "ER_NEEDED"
            and r["coverage"] != "\u2705")
        after_er = min(
            l1 + er_needed + er_boost.get(qtype, 0), total)
        l2_needed = sum(
            1 for r in results.values()
            if r["type"] == qtype
            and r["diagnosis"] == "L2_REQUIRED")
        after_l2 = min(after_er + l2_needed, total)
        lines.append(
            f"| {qtype} ({total}) | {total} | {l1}/{total} pass | "
            f"{after_er}/{total} pass | {after_l2}/{total} pass |")
    lines.append("")

    # ── Key Findings ─────────────────────────────────────────────────
    lines.append("## 4. Key Findings")
    lines.append("")
    lines.append("### What works well at L1")
    lines.append("")
    for qid, r in sorted(results.items()):
        if r["coverage"] == "\u2705":
            lines.append(f"- **{qid}**: {r['name']}")
    lines.append("")

    lines.append("### ER merges that would improve results most")
    lines.append("")
    for qid, r in sorted(results.items()):
        if r["diagnosis"] == "ER_NEEDED":
            lines.append(
                f"- **{qid}** ({r['name']}): "
                "surface form fragmentation reduces accuracy")
    lines.append("")

    lines.append("### Queries blocked until Layer 2")
    lines.append("")
    for qid, r in sorted(results.items()):
        if r["diagnosis"] == "L2_REQUIRED":
            lines.append(
                f"- **{qid}** ({r['name']}): "
                "requires CAUSED_BY/CONTRIBUTED_TO edges")
    lines.append("")

    lines.append("### Data sparsity issues")
    lines.append("")
    for qid, r in sorted(results.items()):
        if r["diagnosis"] == "DATA_SPARSE":
            lines.append(
                f"- **{qid}** ({r['name']}): "
                "metadata coverage too low for reliable results")
    lines.append("")

    lines.append("---")
    lines.append(
        "*Generated by pipeline_v2/benchmark/run_benchmark.py*")

    output_path = Path(output_path)
    output_path.write_text("\n".join(lines))
    print(f"\nReport written to {output_path}")
