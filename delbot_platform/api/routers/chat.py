from __future__ import annotations

from uuid import uuid4

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

    session_id = (
        request.session_id
        or str(uuid4())
    )

    application = get_application()

    result = await application.execute(
        question=request.question,
        session_id=session_id,
    )

    return ChatResponse(
        answer=result.answer,
        session_id=result.session_id,
    )
