from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ResearchAnswerRequest(BaseModel):

    question: str = Field(
        min_length=1,
    )

    session_id: str | None = None


class CitationResponse(BaseModel):

    document_id: str

    source: str

    section: str

    page_start: int | None = None

    page_end: int | None = None


class ResearchAnswerResponse(BaseModel):

    answer: str

    citations: list[CitationResponse]

    session_id: str

    research_state: dict[str, Any] = Field(
        default_factory=dict,
    )
