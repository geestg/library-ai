from __future__ import annotations

from delbot_platform.ai.vector_store.base_vector_store import (
    BaseVectorStore,
)
from delbot_platform.research.models.embedding import (
    Embedding,
)
from delbot_platform.research.models.embedding_collection import (
    EmbeddingCollection,
)


class QdrantVectorStore(
    BaseVectorStore,
):
    """
    Vector store backed by Qdrant.

    The actual qdrant_client integration will be added
    when the infrastructure layer is connected.
    """

    def __init__(
        self,
        collection_name: str,
    ) -> None:

        self._collection_name = collection_name

    def upsert(
        self,
        embeddings: EmbeddingCollection,
    ) -> None:

        raise NotImplementedError(
            "Qdrant integration is not implemented yet."
        )

    def search(
        self,
        vector: list[float],
        limit: int = 10,
    ) -> list[Embedding]:

        raise NotImplementedError(
            "Qdrant integration is not implemented yet."
        )

    def delete(
        self,
        ids: list[str],
    ) -> None:

        raise NotImplementedError(
            "Qdrant integration is not implemented yet."
        )

    def clear(
        self,
    ) -> None:

        raise NotImplementedError(
            "Qdrant integration is not implemented yet."
        )
