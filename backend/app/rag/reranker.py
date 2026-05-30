from sentence_transformers import (
    CrossEncoder
)

# =====================================
# LOAD MODEL
# =====================================

reranker_model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

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

    pairs = []

    # =================================
    # BUILD QUERY-DOCUMENT PAIRS
    # =================================

    for doc in documents:

        payload = doc.get(
            "payload",
            {}
        )

        document_text = f"""
        Title:
        {payload.get("title", "")}

        Abstract:
        {payload.get("abstract", "")}

        Chunk:
        {payload.get("chunk", "")}

        Program Studi:
        {payload.get("prodi", "")}
        """

        pairs.append(
            (
                query,
                document_text
            )
        )

    # =================================
    # PREDICT SCORES
    # =================================

    scores = reranker_model.predict(
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