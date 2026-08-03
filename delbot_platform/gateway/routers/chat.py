from __future__ import annotations

from fastapi import APIRouter

from delbot_platform.gateway.request import (
    ChatRequest,
)
from delbot_platform.gateway.services.gateway import (
    GatewayService,
)

router = APIRouter()

_service: GatewayService | None = None


def get_service() -> GatewayService:

    global _service

    if _service is None:
        _service = GatewayService()

    return _service


@router.post("/chat")
async def chat(
    request: ChatRequest,
):

    service = get_service()

    return await service.chat(
        request,
    )
