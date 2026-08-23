from __future__ import annotations

from delbot_platform.ai.embedding.base_embedding_provider import (
    BaseEmbeddingProvider,
)
from delbot_platform.ai.embedding.embedding_request import (
    EmbeddingRequest,
)
from delbot_platform.research.models.embedding import (
    Embedding,
)
from delbot_platform.research.models.embedding_collection import (
    EmbeddingCollection,
)


class EmbeddingService:
    """
    High-level service responsible for generating embeddings.

    The service is provider-agnostic.
    """

    def __init__(
        self,
        provider: BaseEmbeddingProvider,
    ) -> None:

        self._provider = provider

    def embed(
        self,
        requests: list[EmbeddingRequest],
    ) -> EmbeddingCollection:

        results = self._provider.embed_many(
            requests,
        )

        collection = EmbeddingCollection()

        for request, result in zip(
            requests,
            results,
            strict=True,
        ):

            collection.add(
                Embedding(
                    id=request.id,
                    text=request.text,
                    vector=result.vector,
                    metadata={
                        **request.metadata,
                        **result.metadata,
                    },
                )
            )

        return collection
