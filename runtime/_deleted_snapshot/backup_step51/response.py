from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.knowledge.citation.source import (
    CitationSource,
)
from delbot_platform.knowledge.rag.models.response import (
    RAGResponse,
)


@dataclass(slots=True)
class ResearchPipelineResponse:
    """
    Canonical output of the research answering pipeline.

    Combines the generated answer with the underlying
    RAG response so downstream layers can construct
    ResearchResult without repeating retrieval.
    """

    answer: str

    citations: list[CitationSource] = field(
        default_factory=list,
    )

    rag: RAGResponse | None = None