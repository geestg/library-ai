from __future__ import annotations


from fastapi import APIRouter
from fastapi import HTTPException


from delbot_platform.repository import (
    Repository,
)


from .schemas import (
    RepositoryRegisterRequest,
    RepositoryStatusResponse,
    RepositoryIndexResponse,
)


from .service import (
    RepositoryAPIService,
)



router = APIRouter(
    prefix="/repository",
    tags=[
        "repository",
    ],
)



service = RepositoryAPIService()



@router.post(
    "/register",
)
def register_repository(
    request: RepositoryRegisterRequest,
):


    repository = Repository(

        id=request.id,

        name=request.name,

        url=request.url,

        type=request.type,

    )


    service.register(
        repository,
    )


    return RepositoryStatusResponse(

        status="registered",

        message=(
            f"Repository {request.id} registered"
        ),

    )



@router.get(
    "/status/{repository_id}",
)
def repository_status(
    repository_id: str,
):


    exists = service.exists(
        repository_id,
    )


    return RepositoryStatusResponse(

        status=(

            "available"

            if exists

            else "missing"

        ),

        message=repository_id,

    )



@router.post(
    "/index/{item_id}",
)
async def index_repository_item(
    item_id: str,
):


    try:

        result = await service.index(
            item_id,
        )


    except Exception as exc:


        raise HTTPException(

            status_code=400,

            detail=str(
                exc,
            ),

        )



    return RepositoryIndexResponse(

        status=(

            "indexed"

            if result.success

            else "failed"

        ),

        document_id=result.document_id,

        chunks=result.chunks,

        vectors=result.vectors,

        message=(

            "Document indexed successfully"

            if result.success

            else "Document indexing failed"

        ),

    )