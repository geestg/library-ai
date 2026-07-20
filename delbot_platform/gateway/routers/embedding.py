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



service = GatewayService()



@router.post("/embeddings")
async def embeddings(
    request:EmbeddingRequest,
):

    return await service.embedding(
        request
    )
