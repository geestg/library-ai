from __future__ import annotations

from delbot_platform.documents.ingestion import (
    RepositoryDocumentIngestor,
)


class RepositoryDocumentIndexApplication:
    """
    Batch index every available PDF inside repository_data/pdf.

    This application is the MVP entry point for building the
    knowledge base from the local PDF repository.
    """

    def __init__(
        self,
        ingestor: RepositoryDocumentIngestor | None = None,
    ) -> None:

        self.ingestor = (
            ingestor
            if ingestor is not None
            else RepositoryDocumentIngestor()
        )

    async def execute(
        self,
    ) -> list[dict]:

        return await self.ingestor.ingest_available_documents()