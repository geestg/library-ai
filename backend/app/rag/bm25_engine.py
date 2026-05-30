from rank_bm25 import BM25Okapi

from app.rag.qdrant_client import (
    client
)

from app.core.constants import (
    THESIS_DATASET_COLLECTION
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

        response = client.scroll(

            collection_name=
            THESIS_DATASET_COLLECTION,

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

            abstract = payload.get(
                "abstract",
                ""
            )

            chunk = payload.get(
                "chunk",
                ""
            )

            prodi = payload.get(
                "prodi",
                ""
            )

            text = f"""
            {title}

            {abstract}

            {chunk}

            {prodi}
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
                f"[BM25] Initialized with "
                f"{len(documents)} thesis documents"
            )

        else:

            bm25 = None

            print(
                "[BM25] No thesis documents found"
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
    query: str,
    limit: int = 10
):

    global bm25

    if bm25 is None:

        initialize_bm25()

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


# =====================================
# MANUAL TEST
# =====================================

if __name__ == "__main__":

    initialize_bm25()

    results = bm25_search(

        "dashboard penerimaan mahasiswa baru",

        limit=10
    )

    print()

    print("=" * 40)

    print("BM25 RESULTS")

    print("=" * 40)

    for i, result in enumerate(
        results,
        start=1
    ):

        payload = result["payload"]

        print()

        print(f"RESULT {i}")

        print(
            payload.get(
                "title",
                "-"
            )
        )

        print(
            f"SCORE: "
            f"{result['score']:.4f}"
        )