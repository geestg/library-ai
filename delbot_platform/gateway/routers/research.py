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


class ResearchResponse(BaseModel):
    answer: str
    citations: list
    context_length: int
    documents: int
    retrieved: int


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
    )

    return ResearchResponse(
        answer=response.answer,
        citations=response.citations,
        context_length=len(response.rag.context),
        documents=len(response.rag.documents),
        retrieved=len(response.rag.citations),
    )
