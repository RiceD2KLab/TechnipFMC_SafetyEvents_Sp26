"""Similarity method comparison — cluster & neighbourhood visualisation.

Compares three similarity categories side-by-side for the gold-standard
safety incidents using pre-computed pkl embeddings:

  • Text similarity    — sentence-transformer cosine  (text_embeddings.pkl)
  • Structural         — weighted Jaccard over entity types (parquet → computed)
  • KG similarity      — Node2Vec / TransE / RDF2Vec  (*_embeddings.pkl)

Output files (saved to event_similarity/outputs/):
  similarity_clusters.png       — 2-D cluster landscape with theme labels
  similarity_neighborhoods.png  — 3-query × 5-method neighbourhood grid
  similarity_method_heatmap.png — pairwise Pearson r / Spearman ρ heatmap

Usage (from project root):
    python -m event_similarity.visualize_similarity_comparison
    python event_similarity/visualize_similarity_comparison.py
"""
from __future__ import annotations

import json
import pickle
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.cm as mcm
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.manifold import MDS, TSNE
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import pearsonr, spearmanr
import seaborn as sns

# ── Optional UMAP (falls back to t-SNE if not installed) ──────────────────
try:
    import umap as umap_lib
    _USE_UMAP = True
except ImportError:
    _USE_UMAP = False

# ── Path bootstrap — supports both -m and direct execution ────────────────
_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# ── Project imports after path setup ──────────────────────────────────────
try:
    from event_similarity.structural_similarity import (
        load_entity_sets,
        structural_similarity_matrix,
    )
    from event_similarity.config import (
        ENTITIES_PATH,
        OUTPUT_DIR,
        RELATIONS_PATH,
        SCHEMA_WEIGHTS,
    )
    _STRUCT_AVAILABLE = True
except Exception as _e:
    print(f"[viz] Structural similarity unavailable ({_e}); skipping.")
    _STRUCT_AVAILABLE = False
    OUTPUT_DIR = _HERE / "outputs"
    SCHEMA_WEIGHTS = {}
    RELATIONS_PATH = None
    ENTITIES_PATH = None

# ── Config ─────────────────────────────────────────────────────────────────
N_CLUSTERS   = 6
RANDOM_STATE = 42
TOP_K        = 10

# Three diverse queries spanning different cluster themes
QUERY_IDS = [
    "29857",   # Offshore / ROV operations
    "570187",  # Fluid & pressure release
    "609327",  # Falls & rigging
]

# Cluster themes for text similarity (KMeans seed=42, N=258)
# Keys are 0-based cluster labels produced by KMeans.fit_predict
CLUSTER_THEMES: dict[int, str] = {
    0: "Hand/finger\ninjuries",
    1: "Fluid & pressure\nrelease",
    2: "Falls &\nmusculoskeletal",
    3: "Offshore / ROV\noperations",
    4: "Heavy lift\nnear-misses",
    5: "Yard vehicle\ncollisions",
}

_PALETTE   = plt.cm.tab10.colors
_NBR_CMAP  = mcm.YlOrRd   # low→high similarity: yellow → orange → red


# ══════════════════════════════════════════════════════════════════════════
# Data loading
# ══════════════════════════════════════════════════════════════════════════

def _load_pkl(path: Path) -> dict[str, np.ndarray]:
    with open(path, "rb") as fh:
        return pickle.load(fh)


def _load_gold_ids() -> list[str]:
    with open(OUTPUT_DIR / "gold_standard_ids.json") as fh:
        return json.load(fh)


def _load_tier1_eval() -> dict:
    with open(OUTPUT_DIR / "tier1_eval_domain_informed.json") as fh:
        return json.load(fh)


def _build_structural_matrix(ids: list[str]) -> np.ndarray | None:
    if not _STRUCT_AVAILABLE:
        return None
    try:
        print("  Building structural similarity matrix (~30 s for 258 incidents)…")
        entity_sets = load_entity_sets(
            relations_path=RELATIONS_PATH,
            entities_path=ENTITIES_PATH,
        )
        mat = structural_similarity_matrix(entity_sets, ids, SCHEMA_WEIGHTS)
        print(f"  Structural matrix: {mat.shape}, mean={mat.mean():.4f}")
        return mat
    except Exception as exc:
        print(f"  [viz] Structural matrix failed: {exc}")
        return None


# ══════════════════════════════════════════════════════════════════════════
# Dimensionality reduction
# ══════════════════════════════════════════════════════════════════════════

def _reduce_vectors(X: np.ndarray, label: str = "") -> np.ndarray:
    n   = X.shape[0]
    tag = f"[{label}] " if label else ""
    if _USE_UMAP:
        print(f"  {tag}UMAP ({X.shape})…")
        return umap_lib.UMAP(
            n_components=2, n_neighbors=min(15, n - 1), min_dist=0.1,
            metric="cosine", random_state=RANDOM_STATE, verbose=False,
        ).fit_transform(X)
    print(f"  {tag}t-SNE ({X.shape})…")
    return TSNE(
        n_components=2, perplexity=min(30, n - 1), random_state=RANDOM_STATE,
        max_iter=1000, metric="cosine", init="pca", learning_rate="auto",
    ).fit_transform(X)


def _reduce_sim_matrix(sim_mat: np.ndarray, label: str = "") -> np.ndarray:
    dist = np.clip(1.0 - sim_mat, 0.0, None)
    tag  = f"[{label}] " if label else ""
    if _USE_UMAP:
        print(f"  {tag}UMAP precomputed ({sim_mat.shape})…")
        return umap_lib.UMAP(
            n_components=2, metric="precomputed", n_neighbors=min(15, sim_mat.shape[0] - 1),
            min_dist=0.1, random_state=RANDOM_STATE, verbose=False,
        ).fit_transform(dist)
    print(f"  {tag}MDS ({sim_mat.shape})…")
    return MDS(
        n_components=2, metric="precomputed", metric_mds=True,
        random_state=RANDOM_STATE, n_init=4, max_iter=400, init="random",
    ).fit_transform(dist)


# ══════════════════════════════════════════════════════════════════════════
# Clustering
# ══════════════════════════════════════════════════════════════════════════

def _cluster(X: np.ndarray) -> np.ndarray:
    return KMeans(n_clusters=N_CLUSTERS, random_state=RANDOM_STATE, n_init=10).fit_predict(X)


# ══════════════════════════════════════════════════════════════════════════
# Neighbour helpers  (return scored pairs: [(idx, score), …])
# ══════════════════════════════════════════════════════════════════════════

def _json_nbrs_scored(
    q_id: str,
    key: str,
    common_ids: list[str],
    per_query: dict,
) -> list[tuple[int, float]]:
    pairs = per_query.get(q_id, {}).get(key, [])
    return [
        (common_ids.index(nid), float(score))
        for nid, score in pairs
        if nid in common_ids
    ][:TOP_K]


def _emb_nbrs_scored(
    X: np.ndarray,
    q_idx: int,
) -> list[tuple[int, float]]:
    sims = cosine_similarity(X[q_idx : q_idx + 1], X)[0]
    sims[q_idx] = -np.inf
    order = np.argsort(sims)[::-1][:TOP_K]
    return [(int(i), float(sims[i])) for i in order]


# ══════════════════════════════════════════════════════════════════════════
# Core scatter helper
# ══════════════════════════════════════════════════════════════════════════

def _scatter(
    ax: plt.Axes,
    coords: np.ndarray,
    labels: np.ndarray,
    title: str,
    *,
    query_idx: int | None = None,
    neighbour_scored: list[tuple[int, float]] | None = None,
    bg_alpha: float = 0.65,
    cluster_themes: dict[int, str] | None = None,
) -> None:
    """2-D scatter plot with optional cluster annotations and scored neighbours."""
    unique = np.unique(labels)

    # Background incidents coloured by cluster
    for c in unique:
        mask = labels == c
        ax.scatter(
            coords[mask, 0], coords[mask, 1],
            s=16, alpha=bg_alpha,
            color=_PALETTE[int(c) % len(_PALETTE)],
            linewidths=0, zorder=2,
        )

    # Cluster centroid annotations (theme + count)
    if cluster_themes is not None:
        for c in unique:
            mask = labels == c
            cx   = coords[mask, 0].mean()
            cy   = coords[mask, 1].mean()
            n    = int(mask.sum())
            theme = cluster_themes.get(int(c), f"C{int(c)+1}")
            ax.text(
                cx, cy,
                f"{theme}\n(n={n})",
                ha="center", va="center",
                fontsize=6.5, fontweight="bold", color="black",
                bbox=dict(
                    boxstyle="round,pad=0.25",
                    facecolor="white", alpha=0.75,
                    edgecolor=_PALETTE[int(c) % len(_PALETTE)], linewidth=0.8,
                ),
                zorder=6,
            )

    # Neighbours coloured by similarity score (yellow → orange → red)
    if neighbour_scored:
        idxs   = np.array([i for i, _ in neighbour_scored])
        scores = np.array([s for _, s in neighbour_scored], dtype=float)

        lo, hi = scores.min(), scores.max()
        norm   = mcolors.Normalize(vmin=lo - (hi - lo) * 0.1, vmax=hi)
        colors = _NBR_CMAP(norm(scores))

        ax.scatter(
            coords[idxs, 0], coords[idxs, 1],
            s=70, c=colors,
            edgecolors="black", linewidths=0.7,
            zorder=4,
        )

        # Annotate top-3 scores to show the similarity range
        for rank, (i, score) in enumerate(neighbour_scored[:3]):
            ax.annotate(
                f"{score:.2f}",
                xy=(coords[i, 0], coords[i, 1]),
                xytext=(5, 3), textcoords="offset points",
                fontsize=5.5, color="darkred", fontweight="bold",
            )

    # Query star
    if query_idx is not None:
        ax.scatter(
            coords[query_idx, 0], coords[query_idx, 1],
            s=180, marker="*", color="crimson",
            edgecolors="black", linewidths=0.9,
            zorder=7,
        )

    if title:
        ax.set_title(title, fontsize=9.5, fontweight="bold", pad=4)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


# ══════════════════════════════════════════════════════════════════════════
# Figure 1 — Cluster landscape  (theme labels on text panel)
# ══════════════════════════════════════════════════════════════════════════

def _fig_clusters(
    method_data: list[tuple[np.ndarray, np.ndarray, str, dict[int, str] | None]],
    n_incidents: int,
) -> plt.Figure:
    """Grid of scatter plots coloured by KMeans cluster, with theme annotations."""
    n     = len(method_data)
    ncols = 3
    nrows = (n + ncols - 1) // ncols

    reducer_tag = "UMAP" if _USE_UMAP else "t-SNE"
    fig, axes = plt.subplots(
        nrows, ncols,
        figsize=(ncols * 5.0, nrows * 4.4),
        dpi=130,
    )
    axes_flat = np.array(axes).flatten()

    for ax, (coords, labels, title, themes) in zip(axes_flat, method_data):
        _scatter(ax, coords, labels, title, cluster_themes=themes)

    for ax in axes_flat[n:]:
        ax.set_visible(False)

    # Legend: cluster colours + theme names (from text panel)
    legend_handles = [
        mpatches.Patch(
            color=_PALETTE[c],
            label=f"C{c+1}: {CLUSTER_THEMES[c].replace(chr(10), ' ')}",
        )
        for c in range(N_CLUSTERS)
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        ncol=3,
        frameon=False,
        fontsize=8.5,
        bbox_to_anchor=(0.5, -0.04),
    )
    fig.suptitle(
        f"Event Similarity — Cluster Landscape  "
        f"({reducer_tag} · N={n_incidents} incidents · k={N_CLUSTERS} clusters)\n"
        f"Theme labels derived from text similarity clusters (seed=42)",
        fontsize=11, fontweight="bold", y=1.02,
    )
    fig.tight_layout()
    return fig


# ══════════════════════════════════════════════════════════════════════════
# Figure 2 — Neighbourhood comparison  (3 queries × N methods grid)
# ══════════════════════════════════════════════════════════════════════════

def _fig_neighborhoods(
    queries: list[dict],
    method_names: list[str],
) -> plt.Figure:
    """3-row × N-method grid.  Each row is a query; each column is a method.

    Each query dict:
        id          str
        idx         int
        theme       str            (cluster theme of this query)
        methods     list of (coords, labels, scored_neighbours)
    """
    n_queries = len(queries)
    n_methods = len(method_names)

    fig, axes = plt.subplots(
        n_queries, n_methods,
        figsize=(n_methods * 3.8, n_queries * 3.6),
        dpi=130,
        constrained_layout=True,
    )
    # Ensure 2-D array even for single row/col
    if n_queries == 1:
        axes = axes[np.newaxis, :]
    if n_methods == 1:
        axes = axes[:, np.newaxis]

    # Column headers (method names) — only on top row
    for col, name in enumerate(method_names):
        axes[0, col].set_title(name, fontsize=10, fontweight="bold", pad=6)

    for row, q in enumerate(queries):
        q_idx   = q["idx"]
        q_id    = q["id"]
        q_theme = q["theme"]

        for col, (coords, labels, nbrs_scored) in enumerate(q["methods"]):
            ax    = axes[row, col]
            title = name if row > 0 else ""   # title only on row 0 (already set above)
            _scatter(
                ax, coords, labels, title,
                query_idx=q_idx,
                neighbour_scored=nbrs_scored,
                bg_alpha=0.15,
            )
            # Remove the per-cell title added by _scatter on row > 0
            if row > 0:
                ax.set_title("")

        # Row label on the left-most panel
        axes[row, 0].set_ylabel(
            f"#{q_id}\n{q_theme}",
            fontsize=8, fontweight="bold",
            rotation=90, va="center", labelpad=8,
        )

    # Shared colour-bar for similarity scores
    sm = mcm.ScalarMappable(cmap=_NBR_CMAP, norm=mcolors.Normalize(vmin=0, vmax=1))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=axes, orientation="vertical", fraction=0.015, pad=0.02)
    cbar.set_label("Score (within-method norm.)", fontsize=8)
    cbar.ax.tick_params(labelsize=7)

    # Figure-level legend
    legend_handles = [
        plt.scatter([], [], s=130, marker="*", color="crimson",
                    edgecolors="black", linewidths=0.8, label="Query incident"),
        plt.scatter([], [], s=60, color=_NBR_CMAP(0.9),
                    edgecolors="black", linewidths=0.7, label=f"Top-{TOP_K} neighbours\n(darker = more similar)"),
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        ncol=2,
        frameon=False,
        fontsize=8.5,
        bbox_to_anchor=(0.45, -0.04),
    )
    fig.suptitle(
        "Neighbourhood Comparison — Three Query Incidents × Five Similarity Methods\n"
        "Scores annotated on top-3 neighbours per panel",
        fontsize=11, fontweight="bold", y=1.01,
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════
# Figure 3 — Method agreement heatmap
# ══════════════════════════════════════════════════════════════════════════

def _fig_heatmap(
    flats: list[np.ndarray],
    method_names: list[str],
) -> plt.Figure:
    n_m   = len(method_names)
    p_mat = np.eye(n_m)
    s_mat = np.eye(n_m)
    for i in range(n_m):
        for j in range(i + 1, n_m):
            r_p, _ = pearsonr(flats[i], flats[j])
            r_s, _ = spearmanr(flats[i], flats[j])
            p_mat[i, j] = p_mat[j, i] = r_p
            s_mat[i, j] = s_mat[j, i] = r_s

    fig, (ax_p, ax_s) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=130)
    _hm_kw = dict(
        annot=True, fmt=".3f", cmap="RdYlGn", vmin=-0.2, vmax=1.0,
        xticklabels=method_names, yticklabels=method_names,
        linewidths=0.5, square=True, annot_kws={"size": 9},
    )
    sns.heatmap(p_mat, ax=ax_p, **_hm_kw)
    ax_p.set_title("Pearson r",  fontsize=11, fontweight="bold", pad=8)
    sns.heatmap(s_mat, ax=ax_s, **_hm_kw)
    ax_s.set_title("Spearman ρ", fontsize=11, fontweight="bold", pad=8)
    for ax in (ax_p, ax_s):
        ax.tick_params(axis="x", rotation=30, labelsize=9)
        ax.tick_params(axis="y", rotation=0,  labelsize=9)
    fig.suptitle(
        "Pairwise Similarity Matrix Correlation  "
        "(upper-triangle pairs, N(N−1)/2 values per cell)",
        fontsize=11, fontweight="bold", y=1.01,
    )
    fig.tight_layout()
    return fig


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════

def main() -> None:
    print("=" * 60)
    print("  Event Similarity — Cluster & Neighbourhood Visualiser")
    print(f"  Reducer: {'UMAP' if _USE_UMAP else 't-SNE'}")
    print("=" * 60)

    # ── Load embeddings ────────────────────────────────────────────────────
    print("\n[1/5] Loading embeddings and gold-standard IDs…")
    gold_ids    = _load_gold_ids()
    emb_text    = _load_pkl(OUTPUT_DIR / "text_embeddings.pkl")
    emb_n2v     = _load_pkl(OUTPUT_DIR / "node2vec_embeddings.pkl")
    emb_transe  = _load_pkl(OUTPUT_DIR / "transe_embeddings.pkl")
    emb_rdf2vec = _load_pkl(OUTPUT_DIR / "rdf2vec_embeddings.pkl")

    common_ids = [
        i for i in gold_ids
        if i in emb_text and i in emb_n2v and i in emb_transe and i in emb_rdf2vec
    ]
    print(f"  Incidents with all embeddings: {len(common_ids)}/{len(gold_ids)}")

    X_text    = np.vstack([emb_text[i]    for i in common_ids])
    X_n2v     = np.vstack([emb_n2v[i]     for i in common_ids])
    X_transe  = np.vstack([emb_transe[i]  for i in common_ids])
    X_rdf2vec = np.vstack([emb_rdf2vec[i] for i in common_ids])
    print(f"  Shapes — Text:{X_text.shape}  N2V:{X_n2v.shape}  "
          f"TransE:{X_transe.shape}  RDF2Vec:{X_rdf2vec.shape}")

    # ── Structural matrix ──────────────────────────────────────────────────
    print("\n[2/5] Building structural similarity matrix…")
    struct_mat = _build_structural_matrix(common_ids)

    # ── Dimensionality reduction ───────────────────────────────────────────
    print("\n[3/5] Reducing to 2-D…")
    coords_text    = _reduce_vectors(X_text,    "Text")
    coords_n2v     = _reduce_vectors(X_n2v,     "Node2Vec")
    coords_transe  = _reduce_vectors(X_transe,  "TransE")
    coords_rdf2vec = _reduce_vectors(X_rdf2vec, "RDF2Vec")
    coords_struct  = _reduce_sim_matrix(struct_mat, "Structural") \
                     if struct_mat is not None else None

    # ── KMeans clusters ────────────────────────────────────────────────────
    print("\n[4/5] Clustering…")
    labels_text    = _cluster(X_text)
    labels_n2v     = _cluster(X_n2v)
    labels_transe  = _cluster(X_transe)
    labels_rdf2vec = _cluster(X_rdf2vec)
    labels_struct  = _cluster(struct_mat) if struct_mat is not None else None

    # ── Build cluster landscape entries ───────────────────────────────────
    # Pass CLUSTER_THEMES only to the text panel (themes are text-derived)
    cluster_entries: list[tuple] = [
        (coords_text,    labels_text,    "Text Similarity\n(all-MiniLM-L6-v2)",     CLUSTER_THEMES),
        (coords_n2v,     labels_n2v,     "KG Similarity\n(Node2Vec)",               None),
        (coords_transe,  labels_transe,  "KG Similarity\n(TransE)",                 None),
        (coords_rdf2vec, labels_rdf2vec, "KG Similarity\n(RDF2Vec)",                None),
    ]
    if coords_struct is not None:
        cluster_entries.insert(
            1,
            (coords_struct, labels_struct, "Structural Similarity\n(Weighted Jaccard)", None),
        )

    # ── Build neighbourhood data for 3 queries ─────────────────────────────
    tier1     = _load_tier1_eval()
    per_query = tier1.get("per_query", {})

    # Map query IDs → cluster themes (based on text clustering)
    def _query_theme(q_id: str) -> str:
        if q_id not in common_ids:
            return "unknown"
        idx   = common_ids.index(q_id)
        label = int(labels_text[idx])
        return CLUSTER_THEMES.get(label, f"Cluster {label+1}").replace("\n", " ")

    queries: list[dict] = []
    for q_id in QUERY_IDS:
        if q_id not in common_ids:
            print(f"  [viz] Query {q_id} not in common_ids — skipping")
            continue
        q_idx = common_ids.index(q_id)

        nbrs_text    = _json_nbrs_scored(q_id, "text_top_k",   common_ids, per_query)
        nbrs_struct  = _json_nbrs_scored(q_id, "struct_top_k", common_ids, per_query) \
                       if struct_mat is not None else []
        nbrs_n2v     = _emb_nbrs_scored(X_n2v,     q_idx)
        nbrs_transe  = _emb_nbrs_scored(X_transe,  q_idx)
        nbrs_rdf2vec = _emb_nbrs_scored(X_rdf2vec, q_idx)

        method_tuples = [
            (coords_text,    labels_text,    nbrs_text),
            (coords_n2v,     labels_n2v,     nbrs_n2v),
            (coords_transe,  labels_transe,  nbrs_transe),
            (coords_rdf2vec, labels_rdf2vec, nbrs_rdf2vec),
        ]
        if coords_struct is not None:
            method_tuples.insert(1, (coords_struct, labels_struct, nbrs_struct))

        queries.append({
            "id":      q_id,
            "idx":     q_idx,
            "theme":   _query_theme(q_id),
            "methods": method_tuples,
        })

    method_names = ["Text", "Node2Vec", "TransE", "RDF2Vec"]
    if coords_struct is not None:
        method_names.insert(1, "Structural")

    # ── Pairwise flat vectors for heatmap ──────────────────────────────────
    def _triu(mat: np.ndarray) -> np.ndarray:
        idx = np.triu_indices(mat.shape[0], k=1)
        return mat[idx]

    flat_names = ["Text", "Node2Vec", "TransE", "RDF2Vec"]
    flat_vecs  = [
        _triu(cosine_similarity(X_text)),
        _triu(cosine_similarity(X_n2v)),
        _triu(cosine_similarity(X_transe)),
        _triu(cosine_similarity(X_rdf2vec)),
    ]
    if struct_mat is not None:
        flat_names.insert(1, "Structural")
        flat_vecs.insert(1, _triu(struct_mat))

    # ── Generate & save ────────────────────────────────────────────────────
    print("\n[5/5] Generating figures…")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    fig1 = _fig_clusters(cluster_entries, len(common_ids))
    out1 = OUTPUT_DIR / "similarity_clusters.png"
    fig1.savefig(out1, bbox_inches="tight", dpi=130)
    plt.close(fig1)
    print(f"  Saved: {out1}")

    fig2 = _fig_neighborhoods(queries, method_names)
    out2 = OUTPUT_DIR / "similarity_neighborhoods.png"
    fig2.savefig(out2, bbox_inches="tight", dpi=130)
    plt.close(fig2)
    print(f"  Saved: {out2}")

    fig3 = _fig_heatmap(flat_vecs, flat_names)
    out3 = OUTPUT_DIR / "similarity_method_heatmap.png"
    fig3.savefig(out3, bbox_inches="tight", dpi=130)
    plt.close(fig3)
    print(f"  Saved: {out3}")

    print("\nDone. All output written to:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
