from __future__ import annotations

import asyncio

from sentence_transformers import SentenceTransformer

from delbot_platform.documents.models.document_chunk import (
    DocumentChunk,
)
from delbot_platform.documents.embedding.models import (
    EmbeddingVector,
)
from delbot_platform.documents.embedding.base import (
    EmbeddingService,
)


class LocalEmbeddingProvider(
    EmbeddingService,
):

    MODEL_NAME = "BAAI/bge-m3"

    def __init__(
        self,
    ) -> None:

        self.model = SentenceTransformer(
            self.MODEL_NAME,
            device="cpu",
        )

    async def embed(
        self,
        chunks: list[DocumentChunk],
    ) -> list[EmbeddingVector]:

        texts = [
            chunk.text
            for chunk in chunks
        ]

        vectors = await asyncio.to_thread(
            self.model.encode,
            texts,
            batch_size=16,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        results: list[EmbeddingVector] = []

        for chunk, vector in zip(
            chunks,
            vectors,
        ):

            results.append(
                EmbeddingVector(
                    document_id=chunk.document_id,
                    chunk_id=chunk.chunk_id,
                    vector=vector.tolist(),
                    text=chunk.text,
                    metadata=chunk.metadata,
                    provider="local",
                    model=self.MODEL_NAME,
                    dimension=len(vector),
                )
            )

        return results
