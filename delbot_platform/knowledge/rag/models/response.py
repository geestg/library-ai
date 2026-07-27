from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.knowledge.reranking.result import (
    RerankResult,
)
from delbot_platform.research.models import (
    Citation,
)


@dataclass(slots=True)
class RAGResponse:
    """
    Canonical output of the RAG pipeline.
    """

    context: str

    citations: list[Citation] = field(
        default_factory=list,
    )

    documents: list[RerankResult] = field(
        default_factory=list,
    )
