from __future__ import annotations

from fastapi import APIRouter

from delbot_platform.api.schemas.retrieval import (
    RetrievalRequest,
    RetrievalResponse,
)

from delbot_platform.application.factory import (
    ApplicationFactory,
)

router = APIRouter(
    prefix="/retrieval",
    tags=["retrieval"],
)

_application = None


def get_application():

    global _application

    if _application is None:
        _application = ApplicationFactory.retrieval()

    return _application


@router.post(
    "",
    response_model=RetrievalResponse,
)
async def retrieve(
    request: RetrievalRequest,
) -> RetrievalResponse:

    application = get_application()

    result = await application.execute(
        question=request.question,
    )

    return RetrievalResponse(
        context=result.context,
        citations=result.citations,
        documents=result.documents,
    )
