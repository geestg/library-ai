from __future__ import annotations

from typing import Dict, List, Optional
from qdrant_client.models import Filter, FieldCondition, MatchValue

from delbot_platform.core.constants import LIBRARY_BOOKS_COLLECTION
from delbot_platform.research.retrieval.embedder import get_embedding
from delbot_platform.research.retrieval.qdrant_client import client
from delbot_platform.knowledge.library.retrieval.bm25_library import normalize_result, bm25_search


class LibraryRetrieval:
    """
    Mesin pencari hybrid katalog buku (Qdrant Dense Vector + BM25 Okapi + RRF Fusion).
    """

    def semantic_search(
        self,
        query: str,
        limit: int = 50,
        filter_params: Optional[Dict] = None,
    ) -> List[dict]:
        embedding = get_embedding(query)

        qdrant_filter = None
        if filter_params:
            conditions = []
            
            if filter_params.get("location"):
                conditions.append(
                    FieldCondition(
                        key="location",
                        match=MatchValue(value=filter_params["location"])
                    )
                )
                
            if filter_params.get("language"):
                conditions.append(
                    FieldCondition(
                        key="language",
                        match=MatchValue(value=filter_params["language"])
                    )
                )
                
            if filter_params.get("author"):
                conditions.append(
                    FieldCondition(
                        key="author",
                        match=MatchValue(value=filter_params["author"])
                    )
                )
                
            if filter_params.get("publisher"):
                conditions.append(
                    FieldCondition(
                        key="publisher",
                        match=MatchValue(value=filter_params["publisher"])
                    )
                )

            if conditions:
                qdrant_filter = Filter(must=conditions)

        try:
            response = client.query_points(
                collection_name=LIBRARY_BOOKS_COLLECTION,
                query=embedding,
                limit=limit,
                with_payload=True,
                query_filter=qdrant_filter,
            )
        except Exception as e:
            print(f"[LIBRARY RETRIEVAL] Qdrant search error with filter: {e}. Retrying without filter...")
            if qdrant_filter is not None:
                try:
                    response = client.query_points(
                        collection_name=LIBRARY_BOOKS_COLLECTION,
                        query=embedding,
                        limit=limit,
                        with_payload=True,
                        query_filter=None,
                    )
                except Exception as inner_e:
                    print(f"[LIBRARY RETRIEVAL] Qdrant global search error: {inner_e}")
                    return []
            else:
                return []

        results = []
        for point in response.points:
            results.append(
                normalize_result(point.payload, float(point.score))
            )

        return results

    def hybrid_search(
        self,
        query: str,
        limit: int = 20,
        filter_params: Optional[Dict] = None,
    ) -> List[dict]:
        q_lower = f" {query.lower()} "
        expanded_query = query
        if " ai " in q_lower:
            expanded_query += " artificial intelligence kecerdasan buatan"
        if " ml " in q_lower:
            expanded_query += " machine learning"
            
        vector_results = self.semantic_search(expanded_query, limit=50, filter_params=filter_params)

        if not vector_results and filter_params:
            print(f"[LIBRARY RETRIEVAL] Hasil kosong dengan filter {filter_params}. Melonggarkan filter...")
            relaxed_params = filter_params.copy()
            
            if "location" in relaxed_params:
                del relaxed_params["location"]
                vector_results = self.semantic_search(expanded_query, limit=50, filter_params=relaxed_params)

            if not vector_results:
                if "author" in relaxed_params:
                    del relaxed_params["author"]
                if "publisher" in relaxed_params:
                    del relaxed_params["publisher"]
                vector_results = self.semantic_search(expanded_query, limit=50, filter_params=relaxed_params)

            if not vector_results:
                vector_results = self.semantic_search(expanded_query, limit=50, filter_params=None)

        bm25_results = bm25_search(expanded_query, limit=50)

        rrf_k = 60
        fused: Dict[str, dict] = {}

        def get_composite_id(item: dict) -> str:
            title = str(item.get("title") or "").strip().lower()
            author = str(item.get("author") or "").strip().lower()
            isbn = str(item.get("isbn") or "").strip().lower()
            if not isbn or isbn == "-" or isbn.lower() == "none" or isbn.startswith("979000") or isbn.startswith("978000") or len(isbn) < 5:
                return f"{title}_{author}"
            return f"{title}_{author}_{isbn}"

        for rank, item in enumerate(vector_results, start=1):
            doc_id = get_composite_id(item)
            if not doc_id:
                continue
            if doc_id not in fused:
                fused[doc_id] = {"payload": item["payload"], "score": 0}
            fused[doc_id]["score"] += 1 / (rrf_k + rank)

        for rank, item in enumerate(bm25_results, start=1):
            doc_id = get_composite_id(item)
            if not doc_id:
                continue
            if doc_id not in fused:
                fused[doc_id] = {"payload": item["payload"], "score": 0}
            fused[doc_id]["score"] += 1 / (rrf_k + rank)

        sorted_results = sorted(fused.values(), key=lambda x: x["score"], reverse=True)

        return sorted_results[:limit]

    def search_by_metadata(
        self,
        query: str,
        filter_params: Dict,
        limit: int = 20,
    ) -> List[dict]:
        return self.hybrid_search(query, limit=limit, filter_params=filter_params)

    def search_by_classification(
        self,
        classification: str,
        limit: int = 10,
    ) -> List[dict]:
        return bm25_search(classification, limit=limit)

    def collection_info(self) -> dict:
        try:
            info = client.get_collection(LIBRARY_BOOKS_COLLECTION)
            return {
                "points_count": info.points_count,
                "status": info.status,
            }
        except Exception as e:
            return {"error": str(e)}
