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

application = ApplicationFactory.research()


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
) -> ChatResponse:

    result = await application.execute(
        question=request.question,
    )

    return ChatResponse(
        answer=result.answer,
    )
