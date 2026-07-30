from __future__ import annotations

from delbot_platform.ai.registry.model_category import (
    ModelCategory,
)
from delbot_platform.ai.registry.registry import (
    ModelRegistry,
)
from delbot_platform.documents.models.document_chunk import (
    DocumentChunk,
)
from delbot_platform.documents.embedding.models import (
    EmbeddingVector,
)
from delbot_platform.documents.embedding.base import (
    EmbeddingService,
)
from delbot_platform.gateway.client import (
    GatewayClient,
)


class GatewayEmbeddingProvider(
    EmbeddingService,
):
    """
    Embedding provider backed by the DELBot AI Gateway.
    """

    def __init__(
        self,
    ) -> None:

        self.registry = ModelRegistry()
        self.client = GatewayClient()

    async def embed(
        self,
        chunks: list[DocumentChunk],
    ) -> list[EmbeddingVector]:

        runtime = self.registry.default(
            ModelCategory.EMBEDDING,
        ).runtime

        results: list[EmbeddingVector] = []

        for chunk in chunks:

            response = self.client.post(
                runtime=runtime,
                endpoint="/v1/embeddings",
                payload={
                    "model": "bge-m3",
                    "input": chunk.text,
                },
            )

            vector = response["data"][0]["embedding"]

            results.append(
                EmbeddingVector(
                    document_id=chunk.document_id,
                    chunk_id=chunk.chunk_id,
                    vector=vector,
                    text=chunk.text,
                    metadata=chunk.metadata,
                    provider="gateway",
                    model="bge-m3",
                    dimension=len(vector),
                )
            )

        return results
