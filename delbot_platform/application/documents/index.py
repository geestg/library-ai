from __future__ import annotations

from pathlib import Path

from delbot_platform.documents.pipeline.models import (
    DocumentIndexArtifact,
    DocumentIndexResult,
)

from delbot_platform.documents.services import (
    DocumentIndexService,
)


class DocumentIndexApplication:
    """
    Document indexing use case.
    """

    def __init__(
        self,
        service: DocumentIndexService | None = None,
    ) -> None:

        self.service = (
            service
            if service is not None
            else DocumentIndexService()
        )

    async def execute(
        self,
        pdf_path: str | Path,
    ) -> tuple[
        DocumentIndexArtifact,
        DocumentIndexResult,
    ]:

        return await self.service.index(
            pdf_path,
        )
