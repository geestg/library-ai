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
def initialize_thesis_bm25():
    global documents
    global payload_store
    global bm25

    # Check if already initialized
    if bm25 is not None:
        return
    print("[THESIS BM25] Initializing BM25 index for thesis dataset...")
    
    try:
        offset = None
        documents = []
        payload_store = []

        while True:
            response = client.scroll(
                collection_name=THESIS_DATASET_COLLECTION,
                limit=10000,
                offset=offset,
                with_payload=True,
                with_vectors=False
            )
            points = response[0]
            offset = response[1]
            if not points:
                break

            for point in points:
                payload = point.payload or {}
                title = payload.get("title", "")
                abstract = payload.get("abstract", "")
                chunk = payload.get("chunk", "")
                prodi = payload.get("prodi", "")

                text = f"""
                {title}
                {abstract}
                {chunk}
                {prodi}
                """

                if not text.strip():
                    continue

                documents.append(text)
                payload_store.append(payload)

            if offset is None:
                break

        print(f"[THESIS BM25] Loaded {len(documents)} document chunks for BM25 indexing.")

        if documents:
            tokenized_corpus = [
                doc.lower().split()
                for doc in documents
            ]
            bm25 = BM25Okapi(tokenized_corpus)
            print("[THESIS BM25] BM25 indexing complete!")

    except Exception as e:
        print(f"[THESIS BM25 ERROR] Failed to initialize BM25: {e}")
        bm25 = None


# =====================================
# SEARCH
# =====================================
def thesis_bm25_search(
    query: str,
    limit: int = 50,
    prodi_names: list[str] = None,
    offset: int = 0
):
    global bm25
    global payload_store
    if bm25 is None:
        initialize_thesis_bm25()

    if bm25 is None or not payload_store:
        return []

    tokenized_query = query.lower().split()

    # If prodi_names filter is provided, filter payload indices first
    target_indices = range(len(payload_store))
    if prodi_names:
        prodi_names_lower = [p.lower() for p in prodi_names]
        target_indices = [
            i for i in target_indices
            if any(
                p_req in str(payload_store[i].get("prodi", "")).lower()
                or str(payload_store[i].get("prodi", "")).lower() in p_req
                for p_req in prodi_names_lower
            )
        ]

    if not target_indices:
        return []

    # Get BM25 scores for all target documents
    all_scores = bm25.get_scores(tokenized_query)
    scored_indices = [
        (idx, float(all_scores[idx]))
        for idx in target_indices
        if all_scores[idx] > 0
    ]

    # Sort by score descending
    scored_indices.sort(key=lambda x: x[1], reverse=True)
    
    # Get offset-based slice
    top_results = scored_indices[offset : offset + limit]
    results = []
    for idx, score in top_results:
        results.append({
            "payload": payload_store[idx],
            "score": score
        })
    return results

