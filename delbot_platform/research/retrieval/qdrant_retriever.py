from __future__ import annotations

from delbot_platform.research.embedding.query import (
    QueryEmbedding,
)
from delbot_platform.vectorstore.qdrant.singleton import (
    get_qdrant_store,
)


class QdrantRetriever:

    def __init__(
        self,
    ) -> None:

        self.store = get_qdrant_store()
        self.store.create_collection()

        self.embedding = QueryEmbedding()

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict]:

        vector = self.embedding.embed(
            query,
        )

        results = self.store.search(
            query_vector=vector,
            limit=limit,
        )

        documents: list[dict] = []

        for item in results:

            documents.append(
                {
                    "score": item.score,
                    "payload": item.payload,
                }
            )

        return documents
