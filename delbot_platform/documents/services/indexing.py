from __future__ import annotations

from pathlib import Path

from delbot_platform.documents.pipeline.indexing import (
    DocumentIndexingPipeline,
)
from delbot_platform.documents.pipeline.models import (
    DocumentIndexArtifact,
    DocumentIndexResult,
)


class DocumentIndexService:

    def __init__(
        self,
    ) -> None:

        self.pipeline = DocumentIndexingPipeline()

    async def index(
        self,
        pdf_path: str | Path,
        document_id: str | None = None,
    ) -> tuple[
        DocumentIndexArtifact,
        DocumentIndexResult,
    ]:

        return await self.pipeline.index_with_summary(
            str(pdf_path),
            document_id=document_id,
        )
