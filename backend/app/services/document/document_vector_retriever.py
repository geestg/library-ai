from qdrant_client.models import (
    FieldCondition,
    Filter,
    MatchAny,
    MatchValue,
)

from app.core.constants import (
    USER_DOCUMENT_COLLECTION,
)

from app.rag.embedder import (
    get_embedding,
)

from app.rag.qdrant_client import (
    client,
)


# =====================================
# RETRIEVE DOCUMENT CHUNKS
# =====================================

def retrieve_document_chunks(

    query: str,

    session_id: str,

    active_document_ids: list,

    top_k: int = 12,

):

    # =================================
    # VALIDATE QUERY
    # =================================

    if not query.strip():

        return []

    # =================================
    # VALIDATE OWNERSHIP SCOPE
    # =================================

    if not session_id:

        return []

    if not active_document_ids:

        return []

    # =================================
    # QUERY EMBEDDING
    # =================================

    query_embedding = get_embedding(
        query
    )

    # =================================
    # OWNERSHIP FILTER
    # =================================

    ownership_filter = Filter(

        must=[

            FieldCondition(

                key="session_id",

                match=MatchValue(
                    value=session_id
                ),

            ),

            FieldCondition(

                key="document_id",

                match=MatchAny(
                    any=active_document_ids
                ),

            ),

            FieldCondition(

                key="source_type",

                match=MatchValue(
                    value="user_document"
                ),

            ),

        ]

    )

    # =================================
    # VECTOR SEARCH
    # =================================

    response = client.query_points(

        collection_name=(
            USER_DOCUMENT_COLLECTION
        ),

        query=query_embedding,

        query_filter=(
            ownership_filter
        ),

        limit=top_k,

        with_payload=True,

    )

    # =================================
    # BUILD RETRIEVAL RESULTS
    # =================================

    results = []

    for point in response.points:

        payload = (
            point.payload or {}
        )

        text = payload.get(
            "text",
            "",
        )

        if not text.strip():

            continue

        results.append({

            "point_id":
                str(point.id),

            "score":
                float(point.score),

            "session_id":
                payload.get(
                    "session_id"
                ),

            "document_id":
                payload.get(
                    "document_id"
                ),

            "source_type":
                payload.get(
                    "source_type"
                ),

            "title":
                payload.get(
                    "title"
                ),

            "author":
                payload.get(
                    "author"
                ),

            "year":
                payload.get(
                    "year"
                ),

            "source_file":
                payload.get(
                    "source_file"
                ),

            "page":
                payload.get(
                    "page"
                ),

            "chunk_index":
                payload.get(
                    "chunk_index"
                ),

            "chunk_length":
                payload.get(
                    "chunk_length"
                ),

            "text":
                text,

        })

    return results

