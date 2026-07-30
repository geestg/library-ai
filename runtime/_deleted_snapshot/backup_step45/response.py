from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.knowledge.citation.source import (
    CitationSource,
)
from delbot_platform.knowledge.reranking.result import (
    RerankResult,
)


@dataclass(slots=True)
class RAGResponse:
    """
    Canonical output of the RAG pipeline.

    This object preserves the reranked documents so downstream
    layers (Research Pipeline, Research Engine, API, etc.) can
    derive additional metadata without performing retrieval again.
    """

    context: str

    citations: list[CitationSource] = field(
        default_factory=list,
    )

    documents: list[RerankResult] = field(
        default_factory=list,
    )