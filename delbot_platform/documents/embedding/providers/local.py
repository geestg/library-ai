from __future__ import annotations

import asyncio

from sentence_transformers import SentenceTransformer

from delbot_platform.documents.embedding.base import (
    EmbeddingService,
)

from delbot_platform.documents.embedding.vector import (
    VectorRecord,
)

from delbot_platform.documents.chunking.chunk import (
    DocumentChunk,
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
    ) -> list[VectorRecord]:


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


        results = []


        for chunk, vector in zip(
            chunks,
            vectors,
        ):

            results.append(

                VectorRecord(

                    id=chunk.id,

                    vector=vector.tolist(),

                    metadata={

                        "document_id":
                            chunk.metadata.document_id,

                        "section":
                            chunk.metadata.section,

                    },

                )

            )


        return results