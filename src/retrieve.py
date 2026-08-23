"""Retrieve top-k chunks for a query under a given retrieval strategy.

`retrieval_strategy` (dense, bm25, or hybrid) is a config parameter, never
hardcoded. Hybrid combines dense and BM25 rankings via reciprocal rank
fusion (RRF, k=60 -- the standard constant from the original RRF paper,
fixed identically across every run). `top_k` is held constant at 5 across
all conditions.
"""

import faiss
from rank_bm25 import BM25Okapi

from index import embed_query, tokenize_for_bm25

TOP_K = 5
RRF_K = 60


def retrieve_dense(query: str, faiss_index: faiss.Index, chunks: list[dict], k: int = TOP_K) -> list[dict]:
    """Return the top-k chunks by dense cosine similarity."""
    query_vec = embed_query(query).reshape(1, -1)
    scores, indices = faiss_index.search(query_vec, k)
    return [
        {**chunks[i], "score": float(score)}
        for score, i in zip(scores[0], indices[0])
        if i != -1
    ]


def retrieve_bm25(query: str, bm25_index: BM25Okapi, chunks: list[dict], k: int = TOP_K) -> list[dict]:
    """Return the top-k chunks by BM25 score, ties broken by chunk_id.

    BM25 produces exact ties in bulk -- every chunk containing none of the
    query terms scores 0.0, which on this corpus is most of them. A plain
    `np.argsort` is quicksort (unstable), so which tied chunks land in the top-5
    is arbitrary and can differ between numpy builds. That is exactly the
    non-determinism the reproducibility requirement says must be pinned
    down, so ties are resolved on `chunk_id`: deterministic, corpus-order
    independent, and identical under both chunk sizes.
    """
    tokenized_query = tokenize_for_bm25(query)
    scores = bm25_index.get_scores(tokenized_query)
    order = sorted(range(len(chunks)), key=lambda i: (-scores[i], chunks[i]["chunk_id"]))
    return [{**chunks[i], "score": float(scores[i])} for i in order[:k]]


def _reciprocal_rank_fusion(*ranked_id_lists: list[str], k: int = RRF_K) -> dict[str, float]:
    """Fuse multiple ranked chunk_id lists into a single RRF score per chunk_id."""
    fused_scores: dict[str, float] = {}
    for ranked_ids in ranked_id_lists:
        for rank, chunk_id in enumerate(ranked_ids):
            fused_scores[chunk_id] = fused_scores.get(chunk_id, 0.0) + 1.0 / (k + rank + 1)
    return fused_scores


def retrieve_hybrid(
    query: str,
    faiss_index: faiss.Index,
    bm25_index: BM25Okapi,
    chunks: list[dict],
    k: int = TOP_K,
) -> list[dict]:
    """Return the top-k chunks by reciprocal rank fusion of dense + BM25 rankings.

    Each ranker is run over the full chunk set (not just top-k) so fusion
    sees each ranker's complete ordering before truncating to k.
    """
    n = len(chunks)
    dense_ranked = retrieve_dense(query, faiss_index, chunks, k=n)
    bm25_ranked = retrieve_bm25(query, bm25_index, chunks, k=n)

    dense_ids = [c["chunk_id"] for c in dense_ranked]
    bm25_ids = [c["chunk_id"] for c in bm25_ranked]
    fused_scores = _reciprocal_rank_fusion(dense_ids, bm25_ids)

    chunks_by_id = {c["chunk_id"]: c for c in chunks}
    # Ties broken on chunk_id, for the same reason as retrieve_bm25. Sorting on
    # the score alone is stable, so equal-scoring chunks would silently inherit
    # dict-insertion order -- which here means dense-first, a quiet bias toward
    # one leg of the fusion in the very condition meant to weigh both equally.
    top_ids = sorted(fused_scores, key=lambda cid: (-fused_scores[cid], cid))[:k]
    return [{**chunks_by_id[cid], "score": fused_scores[cid]} for cid in top_ids]


def retrieve(query: str, strategy: str, faiss_index: faiss.Index, bm25_index: BM25Okapi, chunks: list[dict], k: int = TOP_K) -> list[dict]:
    """Dispatch to the retriever for `strategy` ('dense', 'bm25', or 'hybrid')."""
    if strategy == "dense":
        return retrieve_dense(query, faiss_index, chunks, k)
    if strategy == "bm25":
        return retrieve_bm25(query, bm25_index, chunks, k)
    if strategy == "hybrid":
        return retrieve_hybrid(query, faiss_index, bm25_index, chunks, k)
    raise ValueError(f"Unknown retrieval_strategy: {strategy!r}")
