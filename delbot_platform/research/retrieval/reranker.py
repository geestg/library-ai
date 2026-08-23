from sentence_transformers import (
    CrossEncoder
)

reranker_model = None

def get_reranker():
    global reranker_model
    if reranker_model is not None:
        return reranker_model

    try:
        # Coba load dari cache lokal terlebih dahulu tanpa request jaringan (offline-first)
        reranker_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2", local_files_only=True)
        print("[RERANKER] Loaded CrossEncoder from local cache.")
    except Exception:
        try:
            # Fallback jika belum ter-cache: coba download
            reranker_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
            print("[RERANKER] Downloaded and loaded CrossEncoder.")
        except Exception as e:
            print(f"[RERANKER WARNING] Could not load CrossEncoder model ({e}). Using RRF/Vector fallback.")
            reranker_model = None
    return reranker_model


# =====================================
# RERANK RESULTS
# =====================================
def rerank(
    query: str,
    documents: list,
    top_k: int = None
):

    if not documents:
        return []
    
    model = get_reranker()
    if model is None:
        # Fallback: jika model tidak tersedia (misal offline di container), gunakan score bawaan
        ranked = []
        for doc in documents:
            d = dict(doc)
            if "rerank_score" not in d:
                d["rerank_score"] = float(d.get("score", 0.0))
            ranked.append(d)
        ranked.sort(key=lambda x: x.get("rerank_score", 0.0), reverse=True)
        return ranked[:top_k] if top_k else ranked

    pairs = []

    # =================================
    # BUILD QUERY-DOCUMENT PAIRS
    # =================================
    for doc in documents:
        payload = doc.get(
            "payload",
            {}
        )

        # Ambil nilai-nilai payload dengan fallback dinamis
        title   = payload.get("title", payload.get("judul", ""))
        author  = payload.get("author", payload.get("penulis", ""))
        subject = payload.get("subject", payload.get("subjek", ""))
        description = payload.get("description", payload.get("deskripsi", ""))

        # Build document text:
        # Title & subject repeated 3x so English cross-encoder
        # (ms-marco) gives strong signal to exact title matches
        # like "Introduction to Algorithms" or "Data Structures and
        # Algorithm Analysis" even when description is in Indonesian.
        title_block   = f"{title} {title} {title}"
        subject_block = f"{subject} {subject} {subject}"
        # Truncate description to avoid diluting the signal
        desc_short = description[:200] if description else ""

        document_text = f"{title_block} by {author}. Subject: {subject_block}. {desc_short}"

        pairs.append(
            (
                query,
                document_text
            )
        )

    # =================================
    # PREDICT SCORES
    # =================================
    scores = model.predict(
        pairs
    )

    # =================================
    # ATTACH SCORES
    # =================================
    ranked_documents = []

    for doc, score in zip(
        documents,
        scores
    ):
        doc["rerank_score"] = float(
            score
        )
        ranked_documents.append(
            doc
        )

    # =================================
    # SORT DESC
    # =================================
    ranked_documents.sort(
        key=lambda x:
        x["rerank_score"],
        reverse=True
    )

    # =================================
    # RETURN TOP K
    # =================================
    if top_k:
        return ranked_documents[:top_k]
    return ranked_documents

# =====================================
# BACKWARD COMPATIBILITY
# =====================================
def rerank_results(
    query: str,
    documents: list,
    top_k: int = 10
):
    return rerank(
        query=query,
        documents=documents,
        top_k=top_k
    )