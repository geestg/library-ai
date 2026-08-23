from __future__ import annotations

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
    prefix="/research",
    tags=[
        "research",
    ],
)


application = (
    ApplicationFactory.research()
)


@router.post(
    "/answer",
    response_model=ResearchAnswerResponse,
)
async def answer_research(
    request: ResearchAnswerRequest,
) -> ResearchAnswerResponse:

    result = await application.execute(
        question=request.question,
    )

    citations = [
        CitationResponse(
            document_id=item.document_id,
            source=item.source,
            section=item.section,
            page_start=item.page_start,
            page_end=item.page_end,
        )
        for item in result.citations
    ]

    return ResearchAnswerResponse(
        answer=result.answer,
        citations=citations,
    )
