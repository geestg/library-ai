from __future__ import annotations

from delbot_platform.knowledge.citation.builder import (
    CitationBuilder,
)
from delbot_platform.knowledge.context.builder import (
    ContextBuilder,
)
from delbot_platform.knowledge.rag.models.response import (
    RAGResponse,
)
from delbot_platform.knowledge.reranking.gateway import (
    GatewayReranker,
)
from delbot_platform.knowledge.reranking.result import (
    RerankResult,
)
from delbot_platform.knowledge.retrieval.qdrant import (
    QdrantRetriever,
)


class RAGPipeline:

    def __init__(
        self,
    ) -> None:

        self.retriever = QdrantRetriever()

        self.reranker = GatewayReranker()

        self.context_builder = ContextBuilder()

        self.citation_builder = CitationBuilder()

    async def build(
        self,
        query: str,
        retrieve_limit: int = 20,
        rerank_limit: int = 5,
    ) -> RAGResponse:

        retrieved = await self.retriever.retrieve(
            query=query,
            limit=retrieve_limit,
        )

        candidates = [
            RerankResult(
                id=item.id,
                score=0.0,
                content=item.content,
                metadata=item.metadata,
            )
            for item in retrieved
        ]

        ranked = await self.reranker.rerank(
            query=query,
            documents=candidates,
            limit=rerank_limit,
        )

        context = self.context_builder.build(
            ranked,
        )

        citations = self.citation_builder.build(
            ranked,
        )

        return RAGResponse(
            context=context,
            citations=citations,
            documents=ranked,
        )