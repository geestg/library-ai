from __future__ import annotations

from fastapi import APIRouter

from delbot_platform.api.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from delbot_platform.application.factory import (
    ApplicationFactory,
)

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)

_application = None


def get_application():

    global _application

    if _application is None:
        _application = ApplicationFactory.research()

    return _application


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
) -> ChatResponse:

    application = get_application()

    result = await application.execute(
        question=request.question,
    )

    return ChatResponse(
        answer=result.answer,
    )
