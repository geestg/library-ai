from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter

from delbot_platform.api.schemas.research import (
    CitationResponse,
    ResearchAnswerRequest,
    ResearchAnswerResponse,
)

from delbot_platform.application.factory import (
    ApplicationFactory,
)


router = APIRouter(
    prefix="/api/research",
    tags=["research"],
)


_application = None


def get_application():

    global _application

    if _application is None:
        _application = ApplicationFactory.research()

    return _application


@router.post(
    "/answer",
    response_model=ResearchAnswerResponse,
)
async def answer_research(
    request: ResearchAnswerRequest,
) -> ResearchAnswerResponse:

    session_id = (
        request.session_id
        or str(uuid4())
    )

    application = get_application()

    result = await application.execute(
        question=request.question,
        session_id=session_id,
    )

    citations = []

    for item in result.citations:

        metadata = item.metadata or {}

        citations.append(
            CitationResponse(
                document_id=item.document_id,
                source=str(item.source_name),
                section=metadata.get(
                    "section",
                    "",
                ),
                page_start=metadata.get(
                    "page_start",
                    item.page,
                ),
                page_end=metadata.get(
                    "page_end",
                    item.page,
                ),
            )
        )

    return ResearchAnswerResponse(
        answer=result.answer,
        citations=citations,
        session_id=session_id,
        research_state=result.research_state,
    )
