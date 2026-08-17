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

    overlay_file = (
        PDF_ROOT.parent
        / "runtime"
        / "repository_overlay.json"
    )

    overlay_by_pdf = {}

    if overlay_file.exists():
        try:
            import json

            overlay_data = json.loads(
                overlay_file.read_text(
                    encoding="utf-8"
                )
            )

            if isinstance(overlay_data, list):
                for row in overlay_data:
                    if not isinstance(row, dict):
                        continue

                    pdf_path = str(
                        row.get("pdf_path", "")
                        or ""
                    )

                    document_id = str(
                        row.get("document_id", "")
                        or ""
                    )

                    if pdf_path and document_id:
                        overlay_by_pdf[
                            Path(pdf_path).name
                        ] = document_id

        except Exception:
            overlay_by_pdf = {}

    indexed = 0

    for pdf in pdfs[: request.limit]:

        document_id = overlay_by_pdf.get(
            pdf.name
        )

        try:
            await pipeline.index_with_summary(
                str(pdf),
                document_id=document_id,
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
