from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from delbot_platform.documents.pipeline.indexing import (
    DocumentIndexingPipeline,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

PDF_ROOT = (
    Path(__file__).resolve().parents[2]
    / "repository_data"
    / "pdf"
)


class BatchIndexRequest(BaseModel):
    limit: int = 25


class BatchIndexResponse(BaseModel):
    success: bool
    indexed: int
    skipped: int
    total_pdf: int


@router.post(
    "/index-all",
    response_model=BatchIndexResponse,
)
async def index_all(
    request: BatchIndexRequest,
):

    pdfs = sorted(PDF_ROOT.rglob("*.pdf"))

    total = len(pdfs)

    pipeline = DocumentIndexingPipeline()

    indexed = 0

    for pdf in pdfs[: request.limit]:

        try:
            await pipeline.index_with_summary(
                str(pdf)
            )
            indexed += 1

        except Exception:
            continue

    skipped = max(
        total - indexed,
        0,
    )

    return BatchIndexResponse(
        success=True,
        indexed=indexed,
        skipped=skipped,
        total_pdf=total,
    )
