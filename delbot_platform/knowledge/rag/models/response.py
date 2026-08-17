from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import TYPE_CHECKING

from delbot_platform.knowledge.reranking.result import (
    RerankResult,
)

if TYPE_CHECKING:
    from delbot_platform.research.models.citation import (
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
