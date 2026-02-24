#!/usr/bin/env python3
"""Generate report charts comparing V1 (Mistral) vs V2 (GLiNER) pipeline."""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUT = str(Path(__file__).resolve().parent) + "/"

# ── Style ──────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
})
BLUE = "#2563EB"
RED = "#DC2626"
GREEN = "#16A34A"
GRAY = "#6B7280"
ORANGE = "#F59E0B"
LIGHT_BLUE = "#93C5FD"
LIGHT_RED = "#FCA5A5"

# ═══════════════════════════════════════════════════════════════════════════
# CHART 1: Why GLiNER — The Relation Type Problem
# ═══════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={"width_ratios": [1, 1]})

# Left: V1 Mistral — 3,380 relation types
ax = axes[0]
# Show top 10 + long tail
v1_labels = ["INVOLVED", "OCCURRED_AT", "USED_IN", "AFFECTED", "CAUSED_BY",
             "RESULTED_IN", "HAS_STATUS", "REPORTED", "LOCATED_IN", "Other 3,371 types"]
v1_counts = [7239, 3478, 2249, 1714, 1237, 674, 412, 389, 301, 8200]
colors_v1 = [LIGHT_RED]*9 + [RED]
bars = ax.barh(range(len(v1_labels)), v1_counts, color=colors_v1, edgecolor="white")
ax.set_yticks(range(len(v1_labels)))
ax.set_yticklabels(v1_labels, fontsize=10)
ax.invert_yaxis()
ax.set_xlabel("Edge Count")
ax.set_title("V1: Mistral 7B Output\n3,380 unique relation types", fontsize=13, fontweight="bold", color=RED)
# Annotate the long tail bar
ax.annotate("91.8% of types have\n≤5 occurrences", xy=(8200, 9), xytext=(12000, 7),
            fontsize=9, color=RED, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=RED))

# Right: V2 GLiNER — 7 relation types
ax = axes[1]
v2_labels = ["OCCURRED_AT", "REPORTED_BY", "INVOLVED", "CATEGORIZED_AS",
             "AFFECTED", "RESULTED_IN", "LOCATED_IN"]
v2_counts = [97903, 42372, 28490, 17933, 10423, 4459, 561]
bars = ax.barh(range(len(v2_labels)), v2_counts, color=BLUE, edgecolor="white")
ax.set_yticks(range(len(v2_labels)))
ax.set_yticklabels(v2_labels, fontsize=10)
ax.invert_yaxis()
ax.set_xlabel("Edge Count")
ax.set_title("V2: GLiNER + Deterministic Rules\n7 relation types (0 violations)", fontsize=13, fontweight="bold", color=BLUE)
for bar, count in zip(bars, v2_counts):
    ax.text(bar.get_width() + 1000, bar.get_y() + bar.get_height()/2,
            f"{count:,}", va="center", fontsize=9, color=GRAY)

fig.suptitle("Relation Schema: LLM Hallucination vs Deterministic Rules", fontsize=15, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(OUT + "chart_relation_types.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ chart_relation_types.png")


# ═══════════════════════════════════════════════════════════════════════════
# CHART 2: Head-to-Head — Key Metrics Comparison
# ═══════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 4, figsize=(16, 4.5))

metrics = [
    ("Relation Types", 3380, 7, "lower is better"),
    ("Giant Component", 0.332, 1.0, "higher is better"),
    ("Mean Degree", 2.0, 7.48, "higher is better"),
    ("Extraction Speed\n(sec/incident)", 10.0, 0.265, "lower is better"),
]

for ax, (name, v1, v2, note) in zip(axes, metrics):
    bars = ax.bar(["Mistral\n(V1)", "GLiNER\n(V2)"], [v1, v2], color=[RED, BLUE], width=0.5, edgecolor="white")
    ax.set_title(name, fontsize=12, fontweight="bold")

    # Value labels
    for bar, val in zip(bars, [v1, v2]):
        label = f"{val:,.0f}" if val >= 10 else f"{val:.3f}" if val < 1 else f"{val:.1f}"
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.05,
                label, ha="center", va="bottom", fontsize=11, fontweight="bold")

    # Improvement annotation
    if v1 > v2:
        improvement = f"{v1/v2:.0f}x reduction"
    else:
        improvement = f"{v2/v1:.1f}x increase"
    ax.text(0.5, -0.18, improvement, transform=ax.transAxes,
            ha="center", fontsize=10, color=GREEN, fontweight="bold")

    ax.set_ylim(0, max(v1, v2) * 1.25)

fig.suptitle("GLiNER vs Mistral: Head-to-Head Comparison", fontsize=15, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(OUT + "chart_head_to_head.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ chart_head_to_head.png")


# ═══════════════════════════════════════════════════════════════════════════
# CHART 3: Benchmark Query Coverage
# ═══════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5))

categories = ["Single-hop", "Aggregation", "Multi-hop", "Global", "Conjunctive"]
full_pass = [5, 5, 5, 4, 2]
partial = [1, 1, 2, 0, 3]
fail = [0, 0, 1, 0, 1]

x = np.arange(len(categories))
w = 0.6

p1 = ax.bar(x, full_pass, w, label="Full Pass", color=GREEN, edgecolor="white")
p2 = ax.bar(x, partial, w, bottom=full_pass, label="Partial Pass", color=ORANGE, edgecolor="white")
p3 = ax.bar(x, fail, w, bottom=[f+p for f,p in zip(full_pass, partial)], label="Fail", color=RED, edgecolor="white")

ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=11)
ax.set_ylabel("Number of Queries")
ax.set_title("L1 Benchmark: 30 Queries — 21 PASS / 7 PARTIAL / 2 FAIL", fontsize=13, fontweight="bold")
ax.legend(loc="upper right", frameon=False)
ax.set_ylim(0, 10)

# Totals on each bar
for i in range(len(categories)):
    total = full_pass[i] + partial[i] + fail[i]
    ax.text(i, total + 0.15, f"{full_pass[i]}/{total}", ha="center", fontsize=10, fontweight="bold")

plt.tight_layout()
plt.savefig(OUT + "chart_benchmark_coverage.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ chart_benchmark_coverage.png")


# ═══════════════════════════════════════════════════════════════════════════
# CHART 4: Entity Type Distribution (Donut)
# ═══════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 8))

labels = ["INCIDENT", "EQUIPMENT", "LOCATION",
          "ORGANIZATION", "BODY_PART", "INJURY_TYPE",
          "ROOT_CAUSE"]
sizes = [19820, 15158, 12810, 9310, 2630, 1700, 117]
colors = ["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EF4444", "#EC4899", "#6B7280"]
explode = (0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03)

wedges, texts, autotexts = ax.pie(
    sizes, colors=colors, explode=explode,
    autopct="", startangle=90, textprops={"fontsize": 10}
)

# Custom legend instead of overlapping labels
legend_labels = [f"{l} ({s:,})" for l, s in zip(labels, sizes)]
ax.legend(wedges, legend_labels, title="Entity Types", loc="center left",
          bbox_to_anchor=(0.85, 0, 0.5, 1), fontsize=10, title_fontsize=11)

# Donut hole
centre = plt.Circle((0, 0), 0.55, fc="white")
ax.add_artist(centre)
ax.text(0, 0.05, "61,545", fontsize=22, fontweight="bold", ha="center", va="center")
ax.text(0, -0.12, "total nodes", fontsize=12, ha="center", va="center", color=GRAY)

ax.set_title("V2 Knowledge Graph: Entity Distribution\n7 Schema-Compliant Types", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(OUT + "chart_entity_distribution.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ chart_entity_distribution.png")


# ═══════════════════════════════════════════════════════════════════════════
# CHART 5: Pipeline Architecture Flow (text-based summary)
# ═══════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(14, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")

# Pipeline stages as boxes
stages = [
    (0.5, 4.5, "23,311\nIncidents", "#E5E7EB", "black"),
    (2.3, 4.5, "Pre-Filter\n-197 non-English\n-empty narratives", "#FEF3C7", "#92400E"),
    (4.3, 4.5, "GLiNER NER\n133,805 entities\n265ms/incident", "#DBEAFE", "#1E40AF"),
    (6.3, 4.5, "Graph Assembly\n61,545 nodes\n202,141 edges", "#D1FAE5", "#065F46"),
    (8.3, 4.5, "Gate 1 PASS\nGC=1.0\nDegree=6.57", "#DCFCE7", "#14532D"),
]

for x, y, text, bg, fg in stages:
    box = mpatches.FancyBboxPatch((x, y-0.6), 1.5, 1.2, boxstyle="round,pad=0.1",
                                   facecolor=bg, edgecolor=fg, linewidth=1.5)
    ax.add_patch(box)
    ax.text(x+0.75, y, text, ha="center", va="center", fontsize=9, color=fg, fontweight="bold")

# Arrows between stages
for x in [2.0, 3.8, 5.8, 7.8]:
    ax.annotate("", xy=(x+0.3, 4.5), xytext=(x, 4.5),
                arrowprops=dict(arrowstyle="->", color=GRAY, lw=2))

# ER row
er_stages = [
    (2.3, 2.5, "Entity Resolution\n-5,137 entities\n3,936 merged", "#EDE9FE", "#5B21B6"),
    (4.3, 2.5, "Schema Fix\n2,123 edges fixed\n0 violations", "#FEE2E2", "#991B1B"),
    (6.3, 2.5, "Gate 2 PASS\n56,408 nodes\n199,902 edges", "#DCFCE7", "#14532D"),
]
for x, y, text, bg, fg in er_stages:
    box = mpatches.FancyBboxPatch((x, y-0.6), 1.5, 1.2, boxstyle="round,pad=0.1",
                                   facecolor=bg, edgecolor=fg, linewidth=1.5)
    ax.add_patch(box)
    ax.text(x+0.75, y, text, ha="center", va="center", fontsize=9, color=fg, fontweight="bold")

for x in [3.8, 5.8]:
    ax.annotate("", xy=(x+0.3, 2.5), xytext=(x, 2.5),
                arrowprops=dict(arrowstyle="->", color=GRAY, lw=2))

# Arrow from Gate 1 down to ER
ax.annotate("", xy=(3.05, 3.1), xytext=(8.3, 3.9),
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=2, connectionstyle="arc3,rad=0.2"))

# Benchmark box
box = mpatches.FancyBboxPatch((8.3, 1.9), 1.5, 1.2, boxstyle="round,pad=0.1",
                               facecolor="#FEF3C7", edgecolor="#92400E", linewidth=1.5)
ax.add_patch(box)
ax.text(9.05, 2.5, "30 Benchmark\nQueries\n21 PASS", ha="center", va="center",
        fontsize=9, color="#92400E", fontweight="bold")
ax.annotate("", xy=(8.3, 2.5), xytext=(7.8, 2.5),
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=2))

# Title
ax.text(5, 5.7, "GLiNER V2 Pipeline Architecture", fontsize=16, fontweight="bold",
        ha="center", va="center")

plt.savefig(OUT + "chart_pipeline_architecture.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ chart_pipeline_architecture.png")


# ═══════════════════════════════════════════════════════════════════════════
# CHART 6: ER Compression by Entity Type
# ═══════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5))

types = ["ROOT_CAUSE\nCATEGORY", "LOCATION", "INJURY\nTYPE", "BODY_PART", "EQUIPMENT", "ORGANIZATION"]
pre_er = [117, 12810, 1700, 2630, 15158, 9310]
post_er = [73, 10744, 1465, 2315, 13446, 8557]
compression = [37.6, 16.1, 13.8, 12.0, 11.3, 8.1]

x = np.arange(len(types))
w = 0.35

bars1 = ax.bar(x - w/2, pre_er, w, label="Pre-ER", color=LIGHT_RED, edgecolor="white")
bars2 = ax.bar(x + w/2, post_er, w, label="Post-ER", color=BLUE, edgecolor="white")

for i, comp in enumerate(compression):
    ax.text(i, max(pre_er[i], post_er[i]) * 1.05, f"-{comp}%",
            ha="center", fontsize=10, fontweight="bold", color=GREEN)

ax.set_xticks(x)
ax.set_xticklabels(types, fontsize=10)
ax.set_ylabel("Entity Count")
ax.set_title("Entity Resolution: Compression by Type\n5,137 entities merged (8.3% reduction)", fontsize=13, fontweight="bold")
ax.legend(frameon=False)
plt.tight_layout()
plt.savefig(OUT + "chart_er_compression.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ chart_er_compression.png")

print("\n✅ All 6 charts saved to pipeline_v2/outputs/")
