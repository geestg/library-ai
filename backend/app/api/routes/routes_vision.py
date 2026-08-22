from fastapi import APIRouter

from app.schemas.vision import VisionChatRequest
from app.services.multimodal.vision_service import vision_chat

router = APIRouter(
    prefix="/api/vision",
    tags=["Vision"],
)


@router.post("/chat")
async def vision_chat_route(request: VisionChatRequest):
    return vision_chat(
        prompt=request.prompt,
        image_base64=request.image_base64,
        image_url=request.image_url,
    )
