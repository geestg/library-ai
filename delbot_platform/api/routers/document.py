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




@router.post(
    "/index",
)
async def index_document(
    request: DocumentIndexRequest,
):

    application = ApplicationFactory.documents()

    artifact, result = await application.execute(
        request.pdf_path,
    )

    return {
        "document_id": artifact.document.id,
        "source": result.source,
        "pages": result.pages,
        "blocks": result.blocks,
        "sections": result.sections,
        "chunks": result.chunks,
        "vectors": result.vectors,
        "elapsed": result.elapsed,
        "success": result.success,
    }


@router.post(
    "/index-all",
)
async def index_repository_documents():

    import time

    started = time.perf_counter()

    repository_application = (
        ApplicationFactory.repository_documents()
    )

    results = await repository_application.execute()

    documents = len(results)

    indexed = sum(
        1
        for result in results
        if result.get("success")
    )

    failed = documents - indexed

    elapsed = (
        time.perf_counter()
        - started
    )

    return {
        "documents": documents,
        "indexed": indexed,
        "failed": failed,
        "elapsed": elapsed,
        "success": failed == 0,
        "results": results,
    }
