from __future__ import annotations

from fastapi import APIRouter

from delbot_platform.api.schemas.document import (
    DocumentIndexRequest,
)

from delbot_platform.application.factory import (
    ApplicationFactory,
)


router = APIRouter(
    prefix="/documents",
    tags=[
        "documents",
    ],
)


application = (
    ApplicationFactory.documents()
)


@router.post(
    "/index",
)
async def index_document(
    request: DocumentIndexRequest,
):

    artifact, result = await application.execute(
        request.pdf_path,
    )

    return {
        "document_id": artifact.document.document_id,
        "source": result.source,
        "pages": result.pages,
        "blocks": result.blocks,
        "sections": result.sections,
        "chunks": result.chunks,
        "vectors": result.vectors,
        "elapsed": result.elapsed,
        "success": result.success,
    }
