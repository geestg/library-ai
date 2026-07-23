from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from delbot_platform.ai.embedding.embedding_request import (
    EmbeddingRequest,
)
from delbot_platform.ai.embedding.embedding_result import (
    EmbeddingResult,
)


class BaseEmbeddingProvider(ABC):
    """
    Base interface for embedding providers.

    Providers should optimize batch embedding because
    embedding models are significantly faster when
    processing multiple texts at once.
    """

    @abstractmethod
    def embed_many(
        self,
        requests: list[EmbeddingRequest],
    ) -> list[EmbeddingResult]:
        """
        Embed multiple requests.
        """
        raise NotImplementedError

    def embed(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResult:
        """
        Convenience wrapper for single embedding.
        """

        return self.embed_many(
            [
                request,
            ]
        )[0]
