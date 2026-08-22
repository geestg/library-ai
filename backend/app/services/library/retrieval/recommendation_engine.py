from __future__ import annotations

from typing import Dict, List
from app.rag.reranker import rerank
from app.services.library.retrieval.bilingual_expander import clean_search_query, expand_bilingual_terms
from app.services.library.retrieval.hybrid_library_search import LibraryRetrieval

RERANK_THRESHOLD = -5.0
TOP_K = 5


class RecommendationEngine:
    """
    Mesin rekomendasi RAG dengan Cross-Encoder reranker & threshold filter.
    """
    def __init__(self):
        self.retrieval = LibraryRetrieval()

    def recommend_by_query(
        self,
        query: str,
        limit: int = TOP_K,
        filter_params: Dict = None,
    ) -> List[dict]:
        clean_q = clean_search_query(query)
        search_query = expand_bilingual_terms(clean_q)

        print(f"[RECOMMENDATION ENGINE] Query: '{query}' -> Clean: '{clean_q}' -> Search: '{search_query}'")

        raw_results = self.retrieval.hybrid_search(
            query=search_query,
            limit=50,
            filter_params=filter_params,
        )

        if not raw_results:
            return []

        documents = []
        for item in raw_results:
            payload = item.get("payload", {})
            text = payload.get("text", "") or (
                f"{payload.get('title', '')} "
                f"{payload.get('subject', '')} "
                f"{payload.get('description', '')}"
            )
            documents.append({
                "text": text,
                "payload": payload,
                "score": item.get("score", 0),
            })

        reranked = rerank(search_query, documents)

        filtered = [
            doc for doc in reranked
            if doc.get("rerank_score", 0) >= RERANK_THRESHOLD
        ]

        return filtered[:limit]

    def recommend_similar_books(
        self,
        book_payload: dict,
        limit: int = TOP_K,
    ) -> List[dict]:
        query = (
            f"{book_payload.get('title', '')} "
            f"{book_payload.get('subject', '')} "
            f"{book_payload.get('description', '')}"
        ).strip()

        if not query:
            return []

        return self.recommend_by_query(query, limit=limit)
