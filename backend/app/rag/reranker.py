from sentence_transformers import CrossEncoder

reranker_model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank(query, documents):

    pairs = [
        (query, doc["text"])
        for doc in documents
    ]

    scores = reranker_model.predict(pairs)

    for i, score in enumerate(scores):
        documents[i]["rerank_score"] = float(score)

    ranked = sorted(
        documents,
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return ranked