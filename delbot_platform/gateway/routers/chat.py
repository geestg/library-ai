from fastapi import APIRouter

from delbot_platform.gateway.schemas.request import ChatRequest
from delbot_platform.gateway.services.gateway import GatewayService


router = APIRouter()

service = GatewayService()


@router.post("/chat")
async def chat(request: ChatRequest):

    return await service.chat(request)