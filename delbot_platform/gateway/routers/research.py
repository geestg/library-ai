from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from delbot_platform.application.research.answer import (
    ResearchAnswerApplication,
)


router = APIRouter(
    prefix="/research",
    tags=["Research"],
)


class ResearchRequest(BaseModel):

    question: str
    session_id: str | None = None


class CitationResponse(BaseModel):

    document_id: str
    source: str
    section: str
    page_start: int | None = None
    page_end: int | None = None


class ResearchResponse(BaseModel):

    answer: str
    citations: list[CitationResponse]
    context_length: int
    documents: int
    retrieved: int
    session_id: str
    research_state: dict = {}


_application: ResearchAnswerApplication | None = None


def get_application() -> ResearchAnswerApplication:

    global _application

    if _application is None:
        _application = ResearchAnswerApplication()

    return _application


@router.post(
    "/answer",
    response_model=ResearchResponse,
)
async def research_answer(
    request: ResearchRequest,
):

    application = get_application()

    response = await application.execute(
        question=request.question,
        session_id=request.session_id,
    )

    citations = []

    for citation in response.citations:

        document = getattr(
            citation,
            "document",
            None,
        )

        document_id = getattr(
            citation,
            "document_id",
            "",
        )

        source = getattr(
            citation,
            "document_title",
            "",
        )

        metadata = getattr(
            citation,
            "metadata",
            {},
        ) or {}

        page = getattr(
            citation,
            "page",
            None,
        )

        page_start = metadata.get(
            "page_start",
            page,
        )

        page_end = metadata.get(
            "page_end",
            page,
        )

        section = metadata.get(
            "section",
            "",
        )

        if not document_id and document is not None:
            document_id = getattr(
                document,
                "document_id",
                "",
            )

        if not source and document is not None:
            source = getattr(
                document,
                "title",
                "",
            )

        citations.append(
            CitationResponse(
                document_id=str(
                    document_id or "",
                ),
                source=str(
                    source or "",
                ),
                section=str(
                    section or "",
                ),
                page_start=page_start,
                page_end=page_end,
            )
        )

    rag = response.rag

    return ResearchResponse(
        answer=response.answer,
        citations=citations,
        context_length=(
            len(rag.context)
            if rag is not None
            else 0
        ),
        documents=(
            len(rag.documents)
            if rag is not None
            else 0
        ),
        retrieved=(
            len(rag.citations)
            if rag is not None
            else 0
        ),
        session_id=response.session_id,
        research_state=response.research_state or {},
    )
