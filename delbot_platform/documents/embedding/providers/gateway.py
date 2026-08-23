from __future__ import annotations

from delbot_platform.ai.registry.model_category import (
    ModelCategory,
)
from delbot_platform.ai.registry.registry import (
    ModelRegistry,
)
from delbot_platform.documents.chunking.chunk import (
    DocumentChunk,
)
from delbot_platform.documents.embedding.base import (
    EmbeddingService,
)
from delbot_platform.documents.embedding.vector import (
    VectorRecord,
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
    ) -> list[VectorRecord]:

        runtime = self.registry.default(
            ModelCategory.EMBEDDING,
        ).runtime

        results: list[VectorRecord] = []

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
                VectorRecord(
                    id=chunk.id,
                    vector=vector,
                    metadata={
                        "document_id": chunk.metadata.document_id,
                        "source": chunk.metadata.source,
                        "section": chunk.metadata.section,
                        "page_start": chunk.metadata.page_start,
                        "page_end": chunk.metadata.page_end,
                        "text": chunk.text,
                    },
                )
            )

        return results
