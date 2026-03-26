"""GNN-based incident similarity — method (c) in the sponsor objectives.

Implements unsupervised GraphSAGE (Hamilton et al., 2017) on the post-ER
knowledge graph to produce incident-level embeddings that capture multi-hop
relational context.

GraphSAGE overview
──────────────────
At each layer, a node aggregates representations from its sampled neighbours:

    h^(l+1)_v = σ( W^(l) · CONCAT(h^(l)_v, AGG({h^(l)_u : u ∈ N(v)})) )

Training objective: unsupervised link-prediction (positive edges vs. random
negative edges) so that incident nodes sharing many entity neighbours are
pulled together in embedding space.

After training, the incident node embeddings are L2-normalised and used as
drop-in replacements for text or structural similarity scores.

Activation threshold (Section 4.3.2 of the project report):
    giant_component_ratio ≥ 0.85  AND  mean_degree ≥ 3.0
If the post-ER graph does not meet these thresholds this module logs a
diagnostic and returns an empty dict rather than raising.

Dependencies:
    torch, torch_geometric   (pip install torch torch_geometric)
"""
from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
import pandas as pd

from .config import ENTITIES_PATH, OUTPUT_DIR, RELATIONS_PATH


# ── Graph quality check ───────────────────────────────────────────────────

_GCR_THRESHOLD = 0.85   # giant component ratio
_DEG_THRESHOLD = 3.0    # mean degree


def _check_graph_quality(
    relations_path: Path,
    gcr_threshold: float = _GCR_THRESHOLD,
    deg_threshold: float = _DEG_THRESHOLD,
) -> tuple[bool, dict]:
    """Return (passes, metrics_dict) for the GraphSAGE activation gate."""
    try:
        import networkx as nx
    except ImportError:
        # networkx is already a project dependency; skip check if unavailable
        return True, {"note": "networkx unavailable; skipping quality check"}

    edges = pd.read_parquet(relations_path)
    sources = edges["source"].astype(str).tolist()
    targets = edges["target"].astype(str).tolist()

    G = nx.Graph()
    G.add_edges_from(zip(sources, targets))

    n_nodes = G.number_of_nodes()
    giant_size = len(max(nx.connected_components(G), key=len))
    gcr  = giant_size / n_nodes if n_nodes else 0.0
    mean_deg = (2 * G.number_of_edges()) / n_nodes if n_nodes else 0.0

    metrics = {
        "n_nodes": n_nodes,
        "giant_component_ratio": round(gcr, 4),
        "mean_degree": round(mean_deg, 4),
        "gcr_threshold": gcr_threshold,
        "deg_threshold": deg_threshold,
    }
    passes = gcr >= gcr_threshold and mean_deg >= deg_threshold
    return passes, metrics


# ── PyG model definition ──────────────────────────────────────────────────


def _build_graphsage_model(
    in_channels: int,
    hidden_channels: int,
    out_channels: int,
    num_layers: int,
):
    """Construct a two/three-layer GraphSAGE encoder."""
    try:
        import torch
        import torch.nn as nn
        import torch.nn.functional as F
        from torch_geometric.nn import SAGEConv
    except ImportError as exc:
        raise ImportError(
            "GraphSAGE requires torch and torch_geometric.\n"
            "Install with:  pip install torch torch_geometric"
        ) from exc

    class GraphSAGEEncoder(nn.Module):
        def __init__(self):
            """Build SAGEConv layer stack from the enclosing factory parameters."""
            super().__init__()
            self.convs = nn.ModuleList()
            dims = [in_channels] + [hidden_channels] * (num_layers - 1) + [out_channels]
            for i in range(num_layers):
                self.convs.append(SAGEConv(dims[i], dims[i + 1]))

        def forward(self, x, edge_index):
            """Run the multi-layer GraphSAGE forward pass with ReLU and dropout."""
            for i, conv in enumerate(self.convs):
                x = conv(x, edge_index)
                if i < len(self.convs) - 1:
                    x = F.relu(x)
                    x = F.dropout(x, p=0.3, training=self.training)
            return x

    return GraphSAGEEncoder()


# ── Main training function ─────────────────────────────────────────────────


def train_graphsage(
    relations_path: Path = RELATIONS_PATH,
    entities_path: Path = ENTITIES_PATH,
    embedding_dim: int = 128,
    hidden_dim: int = 256,
    num_layers: int = 2,
    epochs: int = 50,
    lr: float = 1e-3,
    batch_size: int = 512,
    neg_ratio: int = 1,
    check_quality: bool = True,
    cache_path: Path | None = OUTPUT_DIR / "graphsage_embeddings.pkl",
) -> dict[str, np.ndarray]:
    """Train unsupervised GraphSAGE and return {record_no: embedding}.

    Training uses an unsupervised link-prediction objective:
      - Positive pairs: actual edges from the post-ER graph
      - Negative pairs: randomly sampled non-edges
      - Loss: binary cross-entropy on dot-product scores

    Args:
        relations_path: Path to relations_post_er.parquet.
        entities_path:  Path to entities_post_er.parquet (used for node count).
        embedding_dim:  Output embedding dimension.
        hidden_dim:     Hidden layer width.
        num_layers:     Number of SAGEConv layers.
        epochs:         Training epochs.
        lr:             Adam learning rate.
        batch_size:     Mini-batch size for edge sampling.
        neg_ratio:      Negative edges per positive edge.
        check_quality:  If True, enforce giant_component_ratio and degree
                        thresholds before training (Section 4.3.2).
        cache_path:     Pickle cache; set None to retrain each time.

    Returns:
        Dict[record_no, np.ndarray] of shape (embedding_dim,) unit-normalised,
        or an empty dict if quality thresholds are not met (logged to stdout).
    """
    if cache_path is not None and Path(cache_path).exists():
        with open(cache_path, "rb") as f:
            return pickle.load(f)

    # ── Quality gate ───────────────────────────────────────────────────────
    if check_quality:
        passes, metrics = _check_graph_quality(relations_path)
        gcr = metrics.get("giant_component_ratio", 0.0)
        deg = metrics.get("mean_degree", 0.0)
        print(f"  Graph quality: GCR={gcr:.4f} (≥{_GCR_THRESHOLD}), "
              f"mean_degree={deg:.4f} (≥{_DEG_THRESHOLD})")
        if not passes:
            print(
                "  GraphSAGE activation threshold NOT met — "
                "returning empty embedding map.\n"
                "  This result will be reported as a pipeline finding "
                "(Section 4.3.2)."
            )
            return {}

    try:
        import torch
        import torch.nn.functional as F
        from sklearn.preprocessing import normalize
    except ImportError as exc:
        raise ImportError(
            "GraphSAGE requires torch.\n"
            "Install with:  pip install torch torch_geometric"
        ) from exc

    # ── Build graph data ───────────────────────────────────────────────────
    edges = pd.read_parquet(relations_path)
    sources = edges["source"].astype(str).tolist()
    targets = edges["target"].astype(str).tolist()

    all_nodes = list(dict.fromkeys(sources + targets))
    node2idx  = {n: i for i, n in enumerate(all_nodes)}
    n_nodes   = len(all_nodes)

    src_idx = torch.tensor([node2idx[s] for s in sources], dtype=torch.long)
    dst_idx = torch.tensor([node2idx[t] for t in targets], dtype=torch.long)
    # Undirected
    edge_index = torch.stack(
        [torch.cat([src_idx, dst_idx]), torch.cat([dst_idx, src_idx])], dim=0
    )

    # Node features: one-hot entity type (7 types + INCIDENT)
    # Use a simple degree-based feature since we have no node attributes
    degree = torch.zeros(n_nodes, dtype=torch.float)
    for idx in src_idx.tolist() + dst_idx.tolist():
        degree[idx] += 1.0
    # Normalise
    degree = (degree - degree.mean()) / (degree.std() + 1e-8)
    x = degree.unsqueeze(1)   # (n_nodes, 1)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    x          = x.to(device)
    edge_index = edge_index.to(device)

    # ── Model ──────────────────────────────────────────────────────────────
    model = _build_graphsage_model(
        in_channels=1,
        hidden_channels=hidden_dim,
        out_channels=embedding_dim,
        num_layers=num_layers,
    ).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    n_edges = src_idx.shape[0]

    # ── Training loop ──────────────────────────────────────────────────────
    for epoch in range(1, epochs + 1):
        model.train()
        optimizer.zero_grad()

        z = model(x, edge_index)   # (n_nodes, embedding_dim)

        # Mini-batch of positive edges
        perm = torch.randperm(n_edges)[:batch_size]
        pos_src = src_idx[perm].to(device)
        pos_dst = dst_idx[perm].to(device)

        # Random negative edges
        neg_dst = torch.randint(0, n_nodes, (batch_size * neg_ratio,), device=device)
        neg_src = pos_src.repeat(neg_ratio)

        pos_score = (z[pos_src] * z[pos_dst]).sum(dim=-1)
        neg_score = (z[neg_src] * z[neg_dst]).sum(dim=-1)

        pos_loss = F.binary_cross_entropy_with_logits(
            pos_score, torch.ones_like(pos_score)
        )
        neg_loss = F.binary_cross_entropy_with_logits(
            neg_score, torch.zeros_like(neg_score)
        )
        loss = pos_loss + neg_loss
        loss.backward()
        optimizer.step()

        if epoch % 10 == 0 or epoch == epochs:
            print(f"  GraphSAGE epoch {epoch}/{epochs}  loss={loss.item():.4f}")

    # ── Extract incident embeddings ────────────────────────────────────────
    model.eval()
    with torch.no_grad():
        all_embs = model(x, edge_index).cpu().numpy()   # (n_nodes, embedding_dim)

    all_embs = normalize(all_embs)

    emb_map: dict[str, np.ndarray] = {}
    for node_id, idx in node2idx.items():
        if node_id.startswith("INCIDENT::"):
            record_no = node_id.split("::", 1)[1]
            emb_map[record_no] = all_embs[idx]

    if cache_path is not None:
        Path(cache_path).parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, "wb") as f:
            pickle.dump(emb_map, f)
        print(f"  GraphSAGE embeddings cached → {cache_path}")

    return emb_map


# ── Shared similarity helpers ─────────────────────────────────────────────


def top_k_gnn(
    emb_map: dict[str, np.ndarray],
    query_id: str,
    corpus_ids: list[str],
    k: int = 10,
) -> list[tuple[str, float]]:
    """Top-k most similar incidents using cosine similarity on GNN embeddings."""
    from .text_similarity import top_k_similar
    return top_k_similar(emb_map, query_id, corpus_ids, k=k)


def gnn_similarity_matrix(
    emb_map: dict[str, np.ndarray],
    incident_ids: list[str],
) -> np.ndarray:
    """(N × N) cosine similarity matrix for GNN embeddings."""
    from .text_similarity import text_similarity_matrix
    return text_similarity_matrix(emb_map, incident_ids)
