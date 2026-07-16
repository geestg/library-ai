from __future__ import annotations


from delbot_platform.knowledge.retrieval.base import (
    Retriever,
)


from delbot_platform.knowledge.retrieval.result import (
    RetrievalResult,
)


from delbot_platform.knowledge.vector.repository.qdrant import (
    QdrantRepository,
)


from delbot_platform.documents.embedding.pipeline.pipeline import (
    EmbeddingPipeline,
)


from delbot_platform.documents.chunking.chunk import (
    DocumentChunk,
)


from delbot_platform.documents.metadata.chunk_metadata import (
    ChunkMetadata,
)



class QdrantRetriever(
    Retriever,
):


    def __init__(
        self,
    ) -> None:


        self.repository = QdrantRepository()


        self.embedding = EmbeddingPipeline(
            provider="gateway",
        )



    async def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> list[RetrievalResult]:


        query_chunk = DocumentChunk(

            id="query",

            content=query,

            metadata=ChunkMetadata(

                document_id="query",

                source="query",

                section="query",

                level=0,

            ),

        )


        vectors = await self.embedding.run(
            [
                query_chunk
            ],
        )


        results = await self.repository.search(

            vector=vectors[0].vector,

            limit=limit,

        )


        return [

            RetrievalResult(

                id=item.id,

                score=0.0,

                content="",

                metadata=item.metadata,

            )

            for item in results

        ]