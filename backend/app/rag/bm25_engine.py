from rank_bm25 import BM25Okapi

from app.rag.qdrant_client import (
    client,
    COLLECTION_NAME
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

def initialize_bm25():

    global documents
    global payload_store
    global bm25

    try:

        # =============================
        # LOAD DATA FROM QDRANT
        # =============================

        response = client.scroll(

            collection_name=COLLECTION_NAME,

            limit=10000,

            with_payload=True,

            with_vectors=False
        )

        points = response[0]

        # =============================
        # RESET STORAGE
        # =============================

        documents = []

        payload_store = []

        # =============================
        # EXTRACT DOCUMENTS
        # =============================

        for point in points:

            payload = point.payload or {}

            text = payload.get(
                "text",
                ""
            )

            if not text.strip():
                continue

            documents.append(text)

            payload_store.append(payload)

        # =============================
        # TOKENIZE
        # =============================

        tokenized_docs = [

            doc.lower().split()

            for doc in documents
        ]

        # =============================
        # BUILD BM25
        # =============================

        if len(tokenized_docs) > 0:

            bm25 = BM25Okapi(
                tokenized_docs
            )

            print(
                f"[BM25] Initialized with {len(documents)} documents"
            )

        else:

            bm25 = None

            print(
                "[BM25] No documents found"
            )

    except Exception as e:

        print(
            f"[BM25 ERROR] {e}"
        )

        bm25 = None


# =====================================
# BM25 SEARCH
# =====================================

def bm25_search(

    query,

    limit=5
):

    global bm25

    # =============================
    # AUTO INIT
    # =============================

    if bm25 is None:

        initialize_bm25()

    if bm25 is None:

        return []

    # =============================
    # TOKENIZE QUERY
    # =============================

    tokenized_query = query.lower().split()

    # =============================
    # GET SCORES
    # =============================

    scores = bm25.get_scores(
        tokenized_query
    )

    # =============================
    # SORT RESULTS
    # =============================

    ranked_results = sorted(

        enumerate(scores),

        key=lambda x: x[1],

        reverse=True
    )

    # =============================
    # BUILD OUTPUT
    # =============================

    results = []

    for idx, score in ranked_results[:limit]:

        results.append({

            "text": documents[idx],

            "score": float(score),

            "payload": payload_store[idx]
        })

    return results