from rank_bm25 import BM25Okapi

from app.rag.qdrant_client import (
    client
)

from app.core.constants import (
    LIBRARY_BOOKS_COLLECTION
)

# =====================================
# GLOBAL STORAGE
# =====================================
documents = []
payload_store = []
bm25 = None


# =====================================
# INITIALIZE BM25
# =====================================
def initialize_library_bm25():
    global documents
    global payload_store
    global bm25

    try:
        response = client.scroll(
            collection_name=
            LIBRARY_BOOKS_COLLECTION,
            limit=10000,
            with_payload=True,
            with_vectors=False
        )
        points = response[0]
        documents = []
        payload_store = []

        # =============================
        # BUILD DOCUMENTS
        # =============================
        for point in points:
            payload = point.payload or {}
            title = payload.get(
                "title",
                ""
            )

            subject = payload.get(
                "subject",
                payload.get("subjek", "")
            )

            author = payload.get(
                "author",
                payload.get("penulis", "")
            )

            publisher = payload.get(
                "publisher",
                payload.get("penerbit", "")
            )

            description = payload.get(
                "description",
                payload.get("deskripsi", "")
            )

            text = f"""
            {title}
            {subject}
            {author}
            {publisher}
            {description}
            """

            if not text.strip():
                continue
            documents.append(
                text
            )
            payload_store.append(
                payload
            )

        # =============================
        # TOKENIZE
        # =============================
        tokenized_docs = [
            doc.lower().split()
            for doc in documents
        ]

        # =============================
        # BUILD BM25 INDEX
        # =============================
        if len(tokenized_docs) > 0:
            bm25 = BM25Okapi(
                tokenized_docs
            )
            print(
                f"[LIBRARY BM25] Initialized with "
                f"{len(documents)} book documents"
            )

        else:
            bm25 = None
            print(
                "[LIBRARY BM25] No book documents found "
                "in library_books collection"
            )

    except Exception as e:
        print(
            f"[LIBRARY BM25 ERROR] {e}"
        )
        bm25 = None

# =====================================
# BM25 SEARCH
# =====================================
def library_bm25_search(
    query: str,
    limit: int = 10
):
    global bm25

    if bm25 is None:
        initialize_library_bm25()

    if bm25 is None:
        return []

    tokenized_query = (
        query
        .lower()
        .strip()
        .split()
    )
    scores = bm25.get_scores(
        tokenized_query
    )
    ranked_results = sorted(
        enumerate(scores),
        key=lambda x: x[1],
        reverse=True
    )
    results = []

    for idx, score in ranked_results[:limit]:
        results.append({
            "text":
            documents[idx],

            "score":
            float(score),

            "payload":
            payload_store[idx]
        })
    return results
