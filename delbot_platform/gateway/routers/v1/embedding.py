from fastapi import APIRouter

from delbot_platform.gateway.request import EmbeddingRequest
from delbot_platform.gateway.services.gateway import GatewayService


router = APIRouter(
    prefix="/v1",
    tags=["Embedding"],
)


service = GatewayService()


@router.post(
    "/embeddings",
)
async def embedding(
    request: EmbeddingRequest,
):

    return await service.embedding(
        request,
    )
