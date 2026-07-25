from __future__ import annotations

from delbot_platform.ai.client.embedding_client import (
    EmbeddingClient,
)
from delbot_platform.vectorstore.qdrant.singleton import (
    get_qdrant_store,
)


class VectorRetriever:

    def __init__(
        self,
    ) -> None:

        self.store = get_qdrant_store()
        self.store.create_collection()

        self.embedder = EmbeddingClient()

    def search(
        self,
        query: str,
        limit: int = 10,
    ):

        vector = self.embedder.embed(
            [query],
        )[0]

        results = self.store.search(
            query_vector=vector,
            limit=limit,
            with_payload=True,
        )

        output = []

        for item in results:

            output.append(
                {
                    "score": item.score,
                    "payload": item.payload,
                }
            )

        return output
