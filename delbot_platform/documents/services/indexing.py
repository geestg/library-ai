from __future__ import annotations

from pathlib import Path

from delbot_platform.documents.pipeline.indexing import (
    DocumentIndexingPipeline,
)

from delbot_platform.documents.pipeline.models.index_result import (
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
    ) -> DocumentIndexResult:

        return await self.pipeline.index(
            pdf_path,
        )