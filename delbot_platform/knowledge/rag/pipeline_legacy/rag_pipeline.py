from __future__ import annotations

from delbot_platform.ai.client.reranker_client import RerankerClient
from delbot_platform.knowledge.models import RAGResult
from delbot_platform.knowledge.rag.citation_builder import CitationBuilder
from delbot_platform.knowledge.rag.context_builder import ContextBuilder
from delbot_platform.knowledge.rag.vector_retriever import VectorRetriever


class RAGPipeline:

    def __init__(
        self,
    ) -> None:

        self.retriever = VectorRetriever()

        self.reranker = RerankerClient()

        self.context_builder = ContextBuilder()

        self.citation_builder = CitationBuilder()

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> RAGResult:

        documents = self.retriever.search(
            query=query,
            limit=20,
        )

        ranked = self.reranker.rerank(
            query=query,
            documents=documents,
        )

        ranked = ranked[:limit]

        context = self.context_builder.build(
            ranked,
        )

        citations = self.citation_builder.build(
            ranked,
        )

        return RAGResult(
            query=query,
            documents=ranked,
            context=context,
            citations=citations,
        )
