from __future__ import annotations

from fastapi import APIRouter

from delbot_platform.api.schemas.retrieval import (
    RetrievalDocument,
    RetrievalRequest,
    RetrievalResponse,
)

from delbot_platform.application.factory import (
    ApplicationFactory,
)


router = APIRouter(
    prefix="/retrieval",
    tags=["retrieval"],
)


_application = None


def get_application():

    global _application

    if _application is None:
        _application = ApplicationFactory.retrieval()

    return _application


@router.post(
    "",
    response_model=RetrievalResponse,
)
async def retrieve(
    request: RetrievalRequest,
) -> RetrievalResponse:

    application = get_application()

    result = await application.execute(
        question=request.question,
        retrieve_limit=request.top_k,
        rerank_limit=request.top_k,
    )

    documents = []

    for item in result.documents:

        metadata = item.metadata

        documents.append(
            RetrievalDocument(
                id=item.id,
                score=float(item.score),
                content=item.content,
                source=metadata.source,
                section=metadata.section_title,
                page_start=metadata.page_start,
                page_end=metadata.page_end,
            )
        )

    return RetrievalResponse(
        context=result.context,
        documents=documents,
    )
