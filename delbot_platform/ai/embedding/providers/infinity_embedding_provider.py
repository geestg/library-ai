from __future__ import annotations

from delbot_platform.ai.embedding.base_embedding_provider import (
    BaseEmbeddingProvider,
)
from delbot_platform.ai.embedding.embedding_request import (
    EmbeddingRequest,
)
from delbot_platform.ai.embedding.embedding_result import (
    EmbeddingResult,
)


class InfinityEmbeddingProvider(
    BaseEmbeddingProvider,
):
    """
    Embedding provider backed by an Infinity server.

    The HTTP implementation will be added after the
    AI Infrastructure layer is connected.
    """

    def __init__(
        self,
        endpoint: str,
        model: str,
    ) -> None:

        self._endpoint = endpoint
        self._model = model

    def embed(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResult:

        raise NotImplementedError(
            "Infinity embedding provider is not implemented yet."
        )
