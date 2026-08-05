from __future__ import annotations

from pydantic import BaseModel
from pydantic import Field


class RetrievalRequest(BaseModel):

    question: str = Field(
        min_length=1,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )


class RetrievalDocument(BaseModel):

    id: str

    score: float

    content: str

    source: str

    section: str | None = None

    page_start: int | None = None

    page_end: int | None = None


class RetrievalResponse(BaseModel):

    context: str

    documents: list[RetrievalDocument]
