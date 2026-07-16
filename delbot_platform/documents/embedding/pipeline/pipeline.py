from __future__ import annotations


from delbot_platform.documents.chunking.chunk import (
    DocumentChunk,
)


from delbot_platform.documents.embedding.vector import (
    VectorRecord,
)


from delbot_platform.documents.embedding.factory.provider import (
    EmbeddingProviderFactory,
)



class EmbeddingPipeline:


    def __init__(
        self,
        provider: str = "local",
    ) -> None:

        self.provider = (
            EmbeddingProviderFactory.build(
                provider,
            )
        )


    async def run(
        self,
        chunks: list[DocumentChunk],
    ) -> list[VectorRecord]:

        return await self.provider.embed(
            chunks,
        )