from __future__ import annotations

import time
from pathlib import Path

from delbot_platform.documents.services import (
    DocumentIndexService,
)

from delbot_platform.knowledge.services import (
    KnowledgeService,
)

from delbot_platform.repository.models import (
    RepositoryItem,
)

from delbot_platform.repository.service import (
    RepositoryService,
)

from delbot_platform.workflows.repository.models import (
    RepositoryIngestionArtifact,
    RepositoryIngestionResult,
)


class RepositoryIngestionWorkflow:

    def __init__(
        self,
        repository: RepositoryService | None = None,
        documents: DocumentIndexService | None = None,
        knowledge: KnowledgeService | None = None,
    ) -> None:

        self.repository = (
            repository
            if repository is not None
            else RepositoryService()
        )

        self.documents = (
            documents
            if documents is not None
            else DocumentIndexService()
        )

        self.knowledge = (
            knowledge
            if knowledge is not None
            else KnowledgeService()
        )

    async def ingest(
        self,
        item: RepositoryItem,
    ) -> RepositoryIngestionArtifact | None:

        resolved = self.repository.resolve_pdf(
            item,
        )

        if not resolved.local_path:
            return None

        pdf = Path(
            resolved.local_path,
        )

        if not pdf.exists():
            return None

        document_artifact, _ = (
            await self.documents.index(
                str(pdf),
                document_id=resolved.id,
            )
        )

        knowledge_artifact, _ = (
            self.knowledge.process(
                document_artifact,
            )
        )

        return RepositoryIngestionArtifact(
            repository=resolved,
            document=document_artifact,
            knowledge=knowledge_artifact,
        )

    def summarize(
        self,
        artifact: RepositoryIngestionArtifact,
        elapsed: float,
    ) -> RepositoryIngestionResult:

        return RepositoryIngestionResult(
            repository_id=artifact.repository.id,
            document_id=artifact.document.document_id,
            success=True,
            indexed=True,
            knowledge_created=True,
            elapsed=elapsed,
        )

    async def ingest_with_summary(
        self,
        item: RepositoryItem,
    ) -> tuple[
        RepositoryIngestionArtifact | None,
        RepositoryIngestionResult | None,
    ]:

        started = time.perf_counter()

        artifact = await self.ingest(
            item,
        )

        if artifact is None:
            return (
                None,
                None,
            )

        elapsed = (
            time.perf_counter()
            - started
        )

        result = self.summarize(
            artifact,
            elapsed,
        )

        return (
            artifact,
            result,
        )
