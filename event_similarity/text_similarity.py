"""Text embedding similarity for incident narratives.

Implements Equation 3 from Section 4.3.1 of the project report:

    S_text(i, j) = (z_i · z_j) / (||z_i|| * ||z_j||)

where z_i is the sentence-transformer embedding of incident i's narrative.

Embeddings are L2-normalised at encode time so that cosine similarity reduces
to a plain dot product, enabling efficient matrix multiplication.
"""
from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from .config import (
    EMBEDDING_BATCH_SIZE,
    METADATA_PATH,
    OUTPUT_DIR,
    SENTENCE_TRANSFORMER_MODEL,
)


# ── Data loading ──────────────────────────────────────────────────────────


def load_narratives(metadata_path: Path = METADATA_PATH) -> pd.DataFrame:
    """Return a deduplicated DataFrame with columns [record_no, narrative].

    record_no is coerced to str to match the string keys used by entity sets.
    Rows with null narratives are dropped.
    """
    df = pd.read_parquet(metadata_path, columns=["record_no", "narrative"])
    df["record_no"] = df["record_no"].astype(str)
    df = df.dropna(subset=["narrative"])
    df = df[df["narrative"].str.strip() != ""]
    df = df.drop_duplicates(subset="record_no")
    return df.reset_index(drop=True)


# ── Embedding computation ─────────────────────────────────────────────────


def compute_text_embeddings(
    narratives: pd.DataFrame,
    model_name: str = SENTENCE_TRANSFORMER_MODEL,
    batch_size: int = EMBEDDING_BATCH_SIZE,
    cache_path: Path | None = OUTPUT_DIR / "text_embeddings.pkl",
) -> dict[str, np.ndarray]:
    """Encode incident narratives and return {record_no: embedding} mapping.

    Args:
        narratives: DataFrame with columns record_no, narrative.
        model_name: Sentence-transformer model identifier.
        batch_size: Encoding batch size.
        cache_path: If provided and the file exists, load from cache instead
                    of re-encoding.  Pass None to always recompute.

    Returns:
        Dict mapping record_no (str) → unit-normalised embedding (np.ndarray).
    """
    if cache_path is not None and Path(cache_path).exists():
        with open(cache_path, "rb") as f:
            return pickle.load(f)

    # Seed for reproducibility before encoding
    np.random.seed(42)
    torch.manual_seed(42)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(42)

    model = SentenceTransformer(model_name)
    texts = narratives["narrative"].astype(str).tolist()
    ids = narratives["record_no"].tolist()

    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        normalize_embeddings=True,   # unit-normalise → cosine = dot product
    )
    # shape: (N, embedding_dim)

    emb_map: dict[str, np.ndarray] = {
        inc_id: emb for inc_id, emb in zip(ids, embeddings)
    }

    if cache_path is not None:
        Path(cache_path).parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, "wb") as f:
            pickle.dump(emb_map, f)
        print(f"  Embeddings cached to {cache_path}")

    return emb_map


# ── Similarity computation ─────────────────────────────────────────────────


def text_similarity_matrix(
    emb_map: dict[str, np.ndarray],
    incident_ids: list[str],
) -> np.ndarray:
    """Compute the (N × N) pairwise cosine similarity matrix.

    Entries satisfy S[i, j] = S_text(incident_ids[i], incident_ids[j]).
    Since embeddings are unit-normalised, cosine similarity == dot product,
    so the full matrix is vectors @ vectors.T.

    Args:
        emb_map: {record_no: unit-normalised embedding}.
        incident_ids: Ordered list of N incident IDs.

    Returns:
        np.ndarray of shape (N, N) with values in [-1, 1].
    """
    vectors = np.vstack([emb_map[inc_id] for inc_id in incident_ids])
    return cosine_similarity(vectors)


def top_k_similar(
    emb_map: dict[str, np.ndarray],
    query_id: str,
    corpus_ids: list[str],
    k: int = 10,
) -> list[tuple[str, float]]:
    """Return the top-k most similar incidents to query_id from corpus_ids.

    The query incident is excluded from the result list.

    Args:
        emb_map: {record_no: unit-normalised embedding}.
        query_id: The incident to find neighbours for.
        corpus_ids: Pool of candidate incidents (query_id excluded internally).
        k: Number of results to return.

    Returns:
        List of (record_no, cosine_similarity) sorted descending by score.
    """
    corpus_filtered = [i for i in corpus_ids if i != query_id]
    query_vec = emb_map[query_id].reshape(1, -1)
    corpus_matrix = np.vstack([emb_map[i] for i in corpus_filtered])
    scores = cosine_similarity(query_vec, corpus_matrix).flatten()
    ranked = sorted(zip(corpus_filtered, scores.tolist()), key=lambda x: x[1], reverse=True)
    return ranked[:k]
