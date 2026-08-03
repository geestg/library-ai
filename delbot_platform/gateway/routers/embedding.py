from fastapi import APIRouter


from delbot_platform.gateway.services.gateway import (
    GatewayService,
)

from delbot_platform.gateway.request import (
    EmbeddingRequest,
)



router = APIRouter(
    prefix="/v1",
    tags=["Embedding"],
)



_service: GatewayService | None = None

def get_service() -> GatewayService:
    global _service
    if _service is None:
        _service = GatewayService()
    return _service



@router.post("/embeddings")
async def embeddings(
    request:EmbeddingRequest,
):

    service = get_service()

    return await service.embedding(
        request
    )
