from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from delbot_platform.research.models.embedding import (
    Embedding,
)
from delbot_platform.research.models.embedding_collection import (
    EmbeddingCollection,
)


class BaseVectorStore(ABC):
    """
    Abstract interface for vector databases.

    Implementations
    ---------------
    - Qdrant
    - Milvus
    - PgVector
    - Pinecone
    """

    @abstractmethod
    def upsert(
        self,
        embeddings: EmbeddingCollection,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        vector: list[float],
        limit: int = 10,
    ) -> list[Embedding]:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        ids: list[str],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def clear(
        self,
    ) -> None:
        raise NotImplementedError
