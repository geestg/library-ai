from app.rag.embedder import get_embedding

from app.rag.qdrant_client import client

from app.rag.bm25_engine import bm25_search


# =====================================
# VECTOR SEARCH
# =====================================

def vector_search(query: str, limit=15):

    embedding = get_embedding(query)

    results = client.query_points(

        collection_name="skripsi_collection",

        query=embedding,

        limit=limit
    )

    parsed = []

    for r in results.points:

        parsed.append({

            "payload": r.payload,

            "score": float(r.score)
        })

    return parsed


# =====================================
# HYBRID SEARCH
# =====================================

def hybrid_search(query: str, limit=15):

    # =================================
    # VECTOR RESULTS
    # =================================

    vector_results = vector_search(
        query,
        limit=limit
    )

    # =================================
    # BM25 RESULTS
    # =================================

    bm25_results = bm25_search(
        query,
        limit=limit
    )

    # =================================
    # FUSION
    # =================================

    fused_scores = {}

    # VECTOR SCORES

    for idx, result in enumerate(vector_results):

        key = str(
            result["payload"]
        )

        fused_scores[key] = {

            "payload": result["payload"],

            "score": 1 / (idx + 1)
        }

    # BM25 SCORES

    for idx, result in enumerate(bm25_results):

        key = str(
            result["payload"]
        )

        if key not in fused_scores:

            fused_scores[key] = {

                "payload": result["payload"],

                "score": 0
            }

        fused_scores[key]["score"] += (
            1 / (idx + 1)
        )

    # =================================
    # SORT FINAL
    # =================================

    final_results = sorted(

        fused_scores.values(),

        key=lambda x: x["score"],

        reverse=True
    )

    return final_results[:limit]