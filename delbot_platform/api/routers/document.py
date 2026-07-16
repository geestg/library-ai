from __future__ import annotations

from fastapi import APIRouter

from delbot_platform.api.schemas.document import (
    DocumentIndexRequest,
)

from delbot_platform.documents.services.indexing import (
    DocumentIndexService,
)


router = APIRouter(
    prefix="/documents",
    tags=[
        "documents",
    ],
)


service = DocumentIndexService()


@router.post(
    "/index",
)
async def index_document(
    request: DocumentIndexRequest,
):

    result = await service.index(
        request.pdf_path,
    )

    return {
        "document_id": result.document_id,
        "source": result.source,
        "pages": result.pages,
        "blocks": result.blocks,
        "sections": result.sections,
        "chunks": result.chunks,
        "vectors": result.vectors,
        "elapsed": result.elapsed,
        "success": result.success,
    }