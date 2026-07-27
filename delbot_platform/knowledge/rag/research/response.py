from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.knowledge.rag.models.response import (
    RAGResponse,
)
from delbot_platform.research.models import (
    Citation,
)


@dataclass(slots=True)
class ResearchPipelineResponse:
    """
    Canonical output of the research answering pipeline.
    """

    answer: str

    citations: list[Citation] = field(
        default_factory=list,
    )

    rag: RAGResponse | None = None
