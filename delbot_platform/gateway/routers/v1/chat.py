from __future__ import annotations

from fastapi import APIRouter

from delbot_platform.gateway.request import ChatRequest
from delbot_platform.gateway.services.gateway import GatewayService


router = APIRouter(
    prefix="/v1",
    tags=["Chat"],
)


service = GatewayService()


@router.post(
    "/chat/completions",
)
async def chat(
    request: ChatRequest,
):

    response = await service.chat(
        request,
    )

    return response
