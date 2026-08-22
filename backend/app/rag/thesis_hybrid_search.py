from app.rag.embedder import (
    get_embedding
)
from app.rag.qdrant_client import (
    client
)
from app.rag.thesis_bm25 import (
    thesis_bm25_search
)
from app.core.constants import (
    THESIS_DATASET_COLLECTION
)


# =====================================
# THESIS VECTOR SEARCH
# =====================================
def thesis_vector_search(
    query: str,
    limit: int = 50,
    prodi_names: list[str] = None,
    offset: int = 0
):
    try:
        embedding = get_embedding(
            query
        )

        qdrant_filter = None
        if prodi_names:
            from qdrant_client.models import Filter, FieldCondition, MatchAny
            qdrant_filter = Filter(
                must=[
                    FieldCondition(
                        key="prodi",
                        match=MatchAny(any=prodi_names)
                    )
                ]
            )

        response = client.query_points(
            collection_name=THESIS_DATASET_COLLECTION,
            query=embedding,
            limit=limit,
            offset=offset,
            query_filter=qdrant_filter,
            with_payload=True
        )
        results = []

        for point in response.points:
            results.append({
                "payload": point.payload,
                "score": float(point.score)
            })
        return results
    except Exception as e:
        print("[THESIS_VECTOR_SEARCH] Vector retrieval failed, falling back to BM25-only retrieval.")
        print(f"[THESIS_VECTOR_SEARCH] ERROR: {e}")
        return []

# =====================================
# THESIS HYBRID SEARCH
# =====================================
def hybrid_search(
    query: str,
    limit: int = 20,
    prodi_names: list[str] = None,
    offset: int = 0
):
    """
    Hybrid search specifically over the thesis dataset.
    Fuses Vector search and BM25 search using Reciprocal Rank Fusion (RRF).
    """

    try:
        vector_results = thesis_vector_search(
            query=query,
            limit=50,
            prodi_names=prodi_names,
            offset=offset
        )
    except Exception as e:
        print(f"[THESIS_HYBRID_SEARCH] Vector search failed: {e}")
        vector_results = []

    try:
        bm25_results = thesis_bm25_search(
            query=query,
            limit=50,
            prodi_names=prodi_names,
            offset=offset
        )
    except Exception as e:
        print(f"[THESIS_HYBRID_SEARCH] BM25 search failed: {e}")
        bm25_results = []

    fused = {}
    rrf_k = 60

    # VECTOR RRF
    for rank, item in enumerate(
        vector_results,
        start=1
    ):
        payload = item["payload"] or {}
        # Identify by unique key (title/url)
        doc_id = payload.get("url") or payload.get("title") or ""

        if not doc_id:
            continue
        if doc_id not in fused:
            fused[doc_id] = {
                "payload": payload,
                "score": 0
            }
        fused[doc_id]["score"] += 1 / (rrf_k + rank)

    # BM25 RRF
    for rank, item in enumerate(
        bm25_results,
        start=1
    ):
        payload = item["payload"] or {}
        doc_id = payload.get("url") or payload.get("title") or ""
    
        if not doc_id:
            continue
        if doc_id not in fused:
            fused[doc_id] = {
                "payload": payload,
                "score": 0
            }
        fused[doc_id]["score"] += 1 / (rrf_k + rank)

    results = sorted(
        fused.values(),
        key=lambda x: x["score"],
        reverse=True
    )
    return results[:limit]