from __future__ import annotations

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


    async def embed(
        self,
        chunks: list[DocumentChunk],
    ) -> list[VectorRecord]:


        results = []


        for chunk in chunks:

            results.append(

                VectorRecord(

                    id=chunk.id,

                    vector=[
                        0.0
                    ],

                    metadata={

                        "document_id":
                            chunk.metadata.document_id,

                        "section":
                            chunk.metadata.section,

                    },

                )

            )


        return results