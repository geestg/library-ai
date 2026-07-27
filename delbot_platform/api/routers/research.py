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
    tags=["research"],
)

application = ApplicationFactory.research()


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

    citations: list[CitationResponse] = []

    for item in result.citations:

        metadata = item.metadata or {}

        page_start = metadata.get(
            "page_start",
            item.page,
        )

        page_end = metadata.get(
            "page_end",
            item.page,
        )

        section = metadata.get(
            "section",
            "",
        )

        citations.append(
            CitationResponse(
                document_id=item.document_id,
                source=str(item.source_name),
                section=section,
                page_start=page_start,
                page_end=page_end,
            )
        )

    return ResearchAnswerResponse(
        answer=result.answer,
        citations=citations,
    )
