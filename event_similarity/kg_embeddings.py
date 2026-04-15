"""Knowledge graph embeddings — method (b) in the sponsor objectives.

Implements two KG embedding strategies on the post-ER graph:

  Node2Vec (Grover & Leskovec, 2016)
  ─────────────────────────────────
  Biased random walks over the incident–entity graph learn structural node
  embeddings that capture neighbourhood topology.  Incident nodes are the
  source nodes (INCIDENT::X); their embeddings serve as incident
  representations for similarity computation.

  TransE (Bordes et al., 2013)
  ────────────────────────────
  Treats each (incident, relation_type, entity) triple as a fact and optimises
  zh + zr ≈ zt via margin-based loss.  Incident entity embeddings encode the
  relational context of each incident.

Both methods produce {record_no: np.ndarray} dicts compatible with the
text_similarity and structural_similarity APIs.

Dependencies:
    torch, torch_geometric   (Node2Vec)
    pykeen                   (TransE)
    pandas, numpy

These are heavy dependencies not in requirements.txt; install with:
    pip install torch torch_geometric pykeen
"""
from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
import pandas as pd

from .config import ENTITIES_PATH, OUTPUT_DIR, RELATIONS_PATH


# ── Graph construction from post-ER parquets ─────────────────────────────


def _build_edge_lists(
    relations_path: Path = RELATIONS_PATH,
) -> tuple[list[str], list[str], list[str], dict[str, int]]:
    """Parse the post-ER relations parquet into edge lists.

    Returns:
        sources      : list of source node IDs (may include INCIDENT:: nodes)
        targets      : list of target node IDs
        relations    : list of relation type labels
        node2idx     : {node_id: integer_index} for all unique nodes
    """
    edges = pd.read_parquet(relations_path)

    sources   = edges["source"].astype(str).tolist()
    targets   = edges["target"].astype(str).tolist()
    rel_types = edges["relation"].astype(str).tolist()

    all_nodes = list(dict.fromkeys(sources + targets))   # ordered dedup
    node2idx  = {n: i for i, n in enumerate(all_nodes)}

    return sources, targets, rel_types, node2idx


def _incident_nodes(node2idx: dict[str, int]) -> dict[str, int]:
    """Filter node2idx to INCIDENT:: nodes only."""
    return {
        node_id: idx
        for node_id, idx in node2idx.items()
        if node_id.startswith("INCIDENT::")
    }


# ── Node2Vec ──────────────────────────────────────────────────────────────


def train_node2vec(
    relations_path: Path = RELATIONS_PATH,
    embedding_dim: int = 128,
    walk_length: int = 20,
    context_size: int = 10,
    walks_per_node: int = 10,
    num_neg_samples: int = 1,
    p: float = 1.0,
    q: float = 1.0,
    epochs: int = 20,
    batch_size: int = 128,
    lr: float = 0.01,
    cache_path: Path | None = OUTPUT_DIR / "node2vec_embeddings.pkl",
) -> dict[str, np.ndarray]:
    """Train Node2Vec on the post-ER incident–entity graph.

    Returns {record_no: embedding} for all INCIDENT nodes.
    record_no is the bare ID (no "INCIDENT::" prefix) to match other methods.

    Args:
        relations_path: Path to relations_post_er.parquet.
        embedding_dim: Embedding dimension.
        walk_length: Random walk length.
        context_size: Skip-gram context window.
        walks_per_node: Number of walks per node per epoch.
        num_neg_samples: Negative samples per positive pair.
        p: Return parameter (BFS bias; p < 1 → stay close).
        q: In-out parameter (DFS bias; q < 1 → explore further).
        epochs: Training epochs.
        batch_size: Walk loader batch size.
        lr: Learning rate.
        cache_path: Pickle cache path; set None to always retrain.

    Returns:
        Dict[record_no, np.ndarray] of shape (embedding_dim,).
    """
    if cache_path is not None and Path(cache_path).exists():
        with open(cache_path, "rb") as f:
            return pickle.load(f)

    # Lazy import — keep torch / torch_geometric optional
    try:
        import torch
        from torch_geometric.nn import Node2Vec as PyGNode2Vec
    except ImportError as exc:
        raise ImportError(
            "Node2Vec requires torch and torch_geometric.\n"
            "Install with:  pip install torch torch_geometric"
        ) from exc

    # Reproducibility
    np.random.seed(42)
    torch.manual_seed(42)

    sources, targets, _, node2idx = _build_edge_lists(relations_path)

    src_idx = [node2idx[s] for s in sources]
    dst_idx = [node2idx[t] for t in targets]

    # Undirected: add reverse edges
    edge_index = torch.tensor(
        [src_idx + dst_idx, dst_idx + src_idx], dtype=torch.long
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = PyGNode2Vec(
        edge_index=edge_index,
        embedding_dim=embedding_dim,
        walk_length=walk_length,
        context_size=context_size,
        walks_per_node=walks_per_node,
        num_negative_samples=num_neg_samples,
        p=p, q=q,
        sparse=True,
    ).to(device)

    loader    = model.loader(batch_size=batch_size, shuffle=True)
    optimizer = torch.optim.SparseAdam(model.parameters(), lr=lr)

    for epoch in range(1, epochs + 1):
        model.train()
        total_loss = 0.0
        for pos_rw, neg_rw in loader:
            optimizer.zero_grad()
            loss = model.loss(pos_rw.to(device), neg_rw.to(device))
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"  Node2Vec epoch {epoch}/{epochs}  loss={total_loss / len(loader):.4f}")

    all_embs = model.embedding.weight.data.cpu().numpy()   # (num_nodes, dim)

    # Project to incident-level embeddings using L2 normalisation
    from sklearn.preprocessing import normalize
    all_embs = normalize(all_embs)

    inc_nodes = _incident_nodes(node2idx)
    emb_map: dict[str, np.ndarray] = {
        node_id.split("::", 1)[1]: all_embs[idx]
        for node_id, idx in inc_nodes.items()
    }

    if cache_path is not None:
        Path(cache_path).parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, "wb") as f:
            pickle.dump(emb_map, f)
        print(f"  Node2Vec embeddings cached → {cache_path}")

    return emb_map


# ── TransE ────────────────────────────────────────────────────────────────


def train_transe(
    relations_path: Path = RELATIONS_PATH,
    embedding_dim: int = 128,
    batch_size: int = 256,
    lr: float = 1e-3,
    num_epochs: int = 100,
    device: str = "cpu",
    cache_path: Path | None = OUTPUT_DIR / "transe_embeddings.pkl",
) -> dict[str, np.ndarray]:
    """Train TransE on (INCIDENT, relation_type, entity) triples.

    Returns {record_no: embedding} for all INCIDENT nodes.

    Args:
        relations_path: Path to relations_post_er.parquet.
        embedding_dim: Embedding dimension.
        batch_size: Training batch size.
        lr: Learning rate.
        num_epochs: Training epochs.
        device: "cpu" or "cuda".
        cache_path: Pickle cache path; set None to always retrain.

    Returns:
        Dict[record_no, np.ndarray] of shape (embedding_dim,) unit-normalised.
    """
    if cache_path is not None and Path(cache_path).exists():
        with open(cache_path, "rb") as f:
            return pickle.load(f)

    try:
        from pykeen.pipeline import pipeline as pykeen_pipeline
        from pykeen.triples import TriplesFactory
    except ImportError as exc:
        raise ImportError(
            "TransE requires pykeen.\n"
            "Install with:  pip install pykeen"
        ) from exc

    # Reproducibility
    np.random.seed(42)

    sources, targets, rel_types, _ = _build_edge_lists(relations_path)

    # Build (head, relation, tail) triple array — keep only INCIDENT sources
    triples = np.array(
        [
            (s, r, t)
            for s, r, t in zip(sources, rel_types, targets)
            if s.startswith("INCIDENT::")
        ],
        dtype=str,
    )

    if len(triples) == 0:
        raise ValueError("No INCIDENT-sourced triples found in relations parquet.")

    tf = TriplesFactory.from_labeled_triples(triples)
    tf_train, tf_test = tf.split([0.9999, 0.0001])

    result = pykeen_pipeline(
        training=tf_train,
        testing=tf_test,
        model="TransE",
        model_kwargs=dict(embedding_dim=embedding_dim, scoring_fct_norm=1),
        training_loop="sLCWA",
        training_kwargs=dict(num_epochs=num_epochs, batch_size=batch_size),
        negative_sampler="basic",
        negative_sampler_kwargs=dict(num_negs_per_pos=1),
        optimizer="adam",
        optimizer_kwargs=dict(lr=lr),
        device=device,
    )

    entity_embs = (
        result.model.entity_representations[0](indices=None)
        .detach()
        .cpu()
        .numpy()
    )
    entity_to_id = {k: int(v) for k, v in tf.entity_to_id.items()}

    from sklearn.preprocessing import normalize
    entity_embs = normalize(entity_embs)

    # Map incident entity IDs → record_no
    emb_map: dict[str, np.ndarray] = {}
    for entity_id, idx in entity_to_id.items():
        if entity_id.startswith("INCIDENT::"):
            record_no = entity_id.split("::", 1)[1]
            emb_map[record_no] = entity_embs[idx]

    if cache_path is not None:
        Path(cache_path).parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, "wb") as f:
            pickle.dump(emb_map, f)
        print(f"  TransE embeddings cached → {cache_path}")

    return emb_map


# ── Shared similarity helpers (re-use text_similarity functions) ──────────


def top_k_kg(
    emb_map: dict[str, np.ndarray],
    query_id: str,
    corpus_ids: list[str],
    k: int = 10,
) -> list[tuple[str, float]]:
    """Top-k most similar incidents using cosine similarity on KG embeddings.

    Delegates to text_similarity.top_k_similar since the interface is
    identical (unit-normalised {record_no: np.ndarray} dicts).
    """
    from .text_similarity import top_k_similar
    return top_k_similar(emb_map, query_id, corpus_ids, k=k)


def kg_similarity_matrix(
    emb_map: dict[str, np.ndarray],
    incident_ids: list[str],
) -> np.ndarray:
    """(N × N) cosine similarity matrix for KG embeddings."""
    from .text_similarity import text_similarity_matrix
    return text_similarity_matrix(emb_map, incident_ids)


# ── RDF2Vec ───────────────────────────────────────────────────────────────


def _build_adjacency(
    relations_path: Path = RELATIONS_PATH,
) -> tuple[dict[str, list[tuple[str, str]]], dict[str, int]]:
    """Build adjacency list {node: [(relation, target), ...]} from parquet.

    Returns:
        adj      : {source_node: [(relation_label, target_node), ...]}
        node2idx : ordering for all unique nodes (used only for sizing)
    """
    edges = pd.read_parquet(relations_path)
    adj: dict[str, list[tuple[str, str]]] = {}
    for src, rel, tgt in zip(
        edges["source"].astype(str),
        edges["relation"].astype(str),
        edges["target"].astype(str),
    ):
        adj.setdefault(src, []).append((rel, tgt))
        # undirected: add reverse edge with inverted relation label
        adj.setdefault(tgt, []).append((f"INV_{rel}", src))

    all_nodes = list(adj.keys())
    node2idx = {n: i for i, n in enumerate(all_nodes)}
    return adj, node2idx


def _generate_walks(
    adj: dict[str, list[tuple[str, str]]],
    root_nodes: list[str],
    walks_per_node: int,
    walk_depth: int,
    seed: int = 42,
) -> list[list[str]]:
    """Generate classic RDF2vec walks (alternating nodes and predicates).

    Each walk has the form:
        [node0, pred1, node1, pred2, node2, ..., nodeD]
    where D = walk_depth.  The walk is represented as a list of strings
    so that gensim can treat each token as a "word".

    Args:
        adj           : adjacency list from _build_adjacency
        root_nodes    : nodes to start walks from
        walks_per_node: number of walks initiated from each root node
        walk_depth    : number of hops per walk (tokens = 2*depth + 1)
        seed          : random seed

    Returns:
        List of walks, each walk is a list of string tokens.
    """
    rng = np.random.default_rng(seed)
    walks: list[list[str]] = []

    for root in root_nodes:
        for _ in range(walks_per_node):
            walk: list[str] = [root]
            current = root
            for _ in range(walk_depth):
                neighbours = adj.get(current)
                if not neighbours:
                    break
                idx = int(rng.integers(len(neighbours)))
                rel, nxt = neighbours[idx]
                walk.append(rel)
                walk.append(nxt)
                current = nxt
            walks.append(walk)

    return walks


def train_rdf2vec(
    relations_path: Path = RELATIONS_PATH,
    embedding_dim: int = 128,
    walks_per_node: int = 200,
    walk_depth: int = 5,
    window_size: int = 5,
    epochs: int = 20,
    sg: int = 1,
    workers: int = 4,
    seed: int = 42,
    cache_path: Path | None = None,
) -> dict[str, np.ndarray]:
    """Train RDF2Vec on the post-ER incident-entity graph.

    Implements classic RDF2vec (Ristoski & Paulheim, 2016):
      1. Generate random walks over the heterogeneous graph, interleaving
         node IDs and relation labels as tokens.
      2. Train Word2Vec skip-gram on those token sequences.
      3. Extract and L2-normalise INCIDENT node embeddings.

    Walk format (classic):
        INCIDENT::42 → HAS_EQUIPMENT → EQUIPMENT::pump → INV_HAS_EQUIPMENT → INCIDENT::17 …

    This is RDF2vec Light in spirit: walks are seeded only from INCIDENT
    nodes to avoid computing embeddings for the entire graph vocabulary.

    Args:
        relations_path : Path to relations_post_er.parquet.
        embedding_dim  : Embedding dimension.
        walks_per_node : Number of random walks per incident node.
        walk_depth     : Hops per walk (token length = 2 * walk_depth + 1). Should match window_size.
        window_size    : Word2Vec context window.
        epochs         : Word2Vec training epochs.
        sg             : 1 = skip-gram (recommended), 0 = CBOW.
        workers        : Parallel Word2Vec training threads.
        seed           : Reproducibility seed.
        cache_path     : Pickle cache; set None to always retrain.

    Returns:
        Dict[record_no, np.ndarray] of shape (embedding_dim,) unit-normalised.

    Dependencies:
        gensim  (pip install gensim)
    """
    # Resolve default cache path at call time so OUTPUT_DIR is fully
    # initialised before this function is ever called.
    from .config import OUTPUT_DIR as _OUTPUT_DIR
    if cache_path is None:
        _cache_path: Path | None = _OUTPUT_DIR / "rdf2vec_embeddings.pkl"
    else:
        _cache_path = Path(cache_path)

    if _cache_path is not None and _cache_path.exists():
        with open(_cache_path, "rb") as f:
            return pickle.load(f)

    try:
        from gensim.models import Word2Vec
    except ImportError as exc:
        raise ImportError(
            "RDF2Vec requires gensim.\n"
            "Install with:  pip install gensim"
        ) from exc

    np.random.seed(seed)

    adj, node2idx = _build_adjacency(relations_path)

    # Seed walks only from INCIDENT nodes (RDF2vec Light approach)
    incident_nodes = [n for n in node2idx if n.startswith("INCIDENT::")]
    if not incident_nodes:
        raise ValueError("No INCIDENT:: nodes found in relations parquet.")

    print(f"  RDF2Vec: generating walks for {len(incident_nodes):,} incident nodes …")
    walks = _generate_walks(
        adj,
        root_nodes=incident_nodes,
        walks_per_node=walks_per_node,
        walk_depth=walk_depth,
        seed=seed,
    )
    print(f"  RDF2Vec: {len(walks):,} walks generated  "
          f"(avg length {sum(len(w) for w in walks) / max(len(walks), 1):.1f} tokens)")

    model = Word2Vec(
        sentences=walks,
        vector_size=embedding_dim,
        window=window_size,
        min_count=1,
        sg=sg,
        epochs=epochs,
        workers=workers,
        seed=seed,
    )

    from sklearn.preprocessing import normalize

    emb_map: dict[str, np.ndarray] = {}
    for node_id in incident_nodes:
        if node_id in model.wv:
            record_no = node_id.split("::", 1)[1]
            vec = model.wv[node_id].astype(np.float32)
            emb_map[record_no] = vec

    if emb_map:
        vecs = np.stack(list(emb_map.values()))
        vecs = normalize(vecs)
        for i, key in enumerate(emb_map):
            emb_map[key] = vecs[i]

    if _cache_path is not None:
        _cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(_cache_path, "wb") as f:
            pickle.dump(emb_map, f)
        print(f"  RDF2Vec embeddings cached → {_cache_path}")

    return emb_map
