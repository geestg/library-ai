from __future__ import annotations


from fastapi import APIRouter


from delbot_platform.api.schemas.research import (
    ResearchAnswerRequest,
    ResearchAnswerResponse,
    CitationResponse,
)


from delbot_platform.research.services.answer import (
    ResearchAnswerService,
)



router = APIRouter(
    prefix="/research",
    tags=[
        "research",
    ],
)



service = ResearchAnswerService()



@router.post(
    "/answer",
    response_model=ResearchAnswerResponse,
)
async def answer_research(
    request: ResearchAnswerRequest,
) -> ResearchAnswerResponse:


    result = await service.answer(
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