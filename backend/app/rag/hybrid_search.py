from app.rag.embedder import (
    get_embedding
)

from app.rag.qdrant_client import (
    client
)

from app.rag.bm25_engine import (
    bm25_search
)

from app.core.constants import (
    THESIS_DATASET_COLLECTION
)


# =====================================
# VECTOR SEARCH
# =====================================

def vector_search(
    query: str,
    limit: int = 50
):

    embedding = get_embedding(
        query
    )

    response = client.query_points(

        collection_name=
        THESIS_DATASET_COLLECTION,

        query=embedding,

        limit=limit,

        with_payload=True
    )

    results = []

    for point in response.points:

        results.append({

            "payload":
            point.payload,

            "score":
            float(point.score)
        })

    return results


# =====================================
# HYBRID SEARCH
# =====================================

def hybrid_search(
    query: str,
    limit: int = 20
):

    vector_results = vector_search(

        query=query,

        limit=50
    )

    bm25_results = bm25_search(

        query=query,

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

        doc_id = (

            payload.get("url")

            or payload.get("title")
        )

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

        doc_id = (

            payload.get("url")

            or payload.get("title")
        )

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