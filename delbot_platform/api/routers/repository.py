from __future__ import annotations

from fastapi import APIRouter

from delbot_platform.api.schemas.repository import (
    RepositoryIndexRequest,
    RepositoryIndexResponse,
)

from delbot_platform.application.factory import (
    ApplicationFactory,
)

from delbot_platform.repository.models import (
    RepositoryItem,
)

router = APIRouter(
    prefix="/repository",
    tags=["repository"],
)

application = (
    ApplicationFactory.repository()
)


@router.get("/health")
def repository_health():

    return {
        "service": "repository",
        "status": "ok",
    }


@router.post(
    "/index",
    response_model=RepositoryIndexResponse,
)
async def index_repository(
    request: RepositoryIndexRequest,
) -> RepositoryIndexResponse:

    repository = RepositoryItem(
        id=request.id,
        title=request.title,
        repository_url=request.repository_url,
        pdf_url=request.pdf_url,
    )

    artifact, result = await application.execute(
        repository,
    )

    return RepositoryIndexResponse(
        repository_id=result.repository_id,
        document_id=result.document_id,
        success=result.success,
        indexed=result.indexed,
        knowledge_created=result.knowledge_created,
        elapsed=result.elapsed,
    )


__all__ = [
    "router",
]
