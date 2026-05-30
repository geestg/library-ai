from app.rag.thesis_hybrid_search import (
    hybrid_search
)

from app.rag.reranker import (
    rerank_results
)


def search_thesis_dataset(
    query: str,
    top_k: int = 5
):

    hybrid_results = hybrid_search(
        query=query,
        limit=50
    )

    reranked_results = rerank_results(
        query=query,
        documents=hybrid_results,
        top_k=30
    )

    unique_thesis = {}

    for result in reranked_results:

        payload = result.get(
            "payload",
            {}
        )

        thesis_key = (
            payload.get("url")
            or payload.get("title")
        )

        score = result.get(
            "rerank_score",
            0.0
        )

        if thesis_key not in unique_thesis:

            unique_thesis[thesis_key] = {

                "score": score,

                "title":
                payload.get("title"),

                "author":
                payload.get("author"),

                "year":
                payload.get("year"),

                "prodi":
                payload.get("prodi"),

                "abstract":
                payload.get("abstract"),

                "chunk":
                payload.get("chunk"),

                "url":
                payload.get("url"),
            }

    results = sorted(

        unique_thesis.values(),

        key=lambda x:
        x["score"],

        reverse=True
    )

    return results[:top_k]