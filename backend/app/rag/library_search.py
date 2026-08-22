from app.rag.embedder import (
    get_embedding
)

from app.rag.qdrant_client import (
    client
)

from app.rag.library_bm25 import (
    library_bm25_search
)

from app.core.constants import (
    LIBRARY_BOOKS_COLLECTION
)

# =====================================
# VECTOR SEARCH — LIBRARY BOOKS
# =====================================
def library_vector_search(
    query: str,
    limit: int = 50
):
    embedding = get_embedding(
        query
    )

    response = client.query_points(
        collection_name=
        LIBRARY_BOOKS_COLLECTION,
        query=embedding,
        limit=limit,
        with_payload=True
    )
    results = []

    for point in response.points:
        print("\n===================")
        print("LIBRARY VECTOR PAYLOAD")
        print("===================")

        print(
            "TITLE:",
            point.payload.get("title")
        )

        results.append({

            "payload":
            point.payload,

            "score":
            float(point.score)
        })

    return results


# =====================================
# HYBRID SEARCH — LIBRARY BOOKS
# =====================================
def library_hybrid_search(
    query: str,
    limit: int = 20,
    bm25_query: str = None
):
    """
    Hybrid search: vector uses full bilingual query (nomic-embed handles cross-lingual),
    BM25 uses English-only query to avoid boosting Indonesian books
    with exact keyword matches on Indonesian words like 'algoritma'.
    """
    vector_results = library_vector_search(
        query=query,
        limit=50
    )

    # BM25 uses English-only query if provided, else falls back to full query
    effective_bm25_query = bm25_query if bm25_query else query

    bm25_results = library_bm25_search(
        query=effective_bm25_query,
        limit=50
    )
    fused = {}
    rrf_k = 60

    # VECTOR
    for rank, item in enumerate(
        vector_results,
        start=1
    ):
        payload = item["payload"]
        title_str = payload.get("title") or payload.get("judul") or ""
        author_str = payload.get("author") or payload.get("penulis") or ""
        doc_id = f"{title_str.strip().lower()}_{author_str.strip().lower()}"
        if not doc_id.strip("_"):
            doc_id = str(payload.get("isbn", id(payload)))

        if doc_id not in fused:
            fused[doc_id] = {
                "payload": payload,
                "score": 0
            }

        fused[doc_id]["score"] += (
            1 / (rrf_k + rank)
        )

    # BM25
    for rank, item in enumerate(
        bm25_results,
        start=1
    ):
        payload = item["payload"]
        title_str = payload.get("title") or payload.get("judul") or ""
        author_str = payload.get("author") or payload.get("penulis") or ""
        doc_id = f"{title_str.strip().lower()}_{author_str.strip().lower()}"
        if not doc_id.strip("_"):
            doc_id = str(payload.get("isbn", id(payload)))

        if doc_id not in fused:
            fused[doc_id] = {
                "payload": payload,
                "score": 0
            }

        fused[doc_id]["score"] += (
            1 / (rrf_k + rank)
        )

    results = sorted(
        fused.values(),
        key=lambda x:
        x["score"],
        reverse=True
    )

    return results[:limit]
