from __future__ import annotations

from delbot_platform.knowledge.context.builder import (
    ContextBuilder,
)
from delbot_platform.knowledge.hydration import (
    CitationHydrator,
    LocalDocumentProvider,
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

        self.retriever = None

        self.reranker = None

        self.context_builder = None

        self.provider = None

        self.hydrator = None

    

    def _initialize(self):

        if self.retriever is None:
            self.retriever = QdrantRetriever()

        if self.reranker is None:
            self.reranker = GatewayReranker()

        if self.context_builder is None:
            self.context_builder = ContextBuilder()

        if self.provider is None:
            self.provider = LocalDocumentProvider()

        if self.hydrator is None:
            self.hydrator = CitationHydrator(
                self.provider,
            )


    async def build(
        self,
        query: str,
        retrieve_limit: int = 20,
        rerank_limit: int = 5,
    ) -> RAGResponse:

        self._initialize()

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

        citations = await self.hydrator.hydrate_many(
            ranked,
        )

        return RAGResponse(
            context=context,
            citations=citations,
            documents=ranked,
        )
