from __future__ import annotations

from delbot_platform.repository.models import (
    RepositoryItem,
)

from delbot_platform.workflows.repository import (
    RepositoryIngestionWorkflow,
)

from delbot_platform.workflows.repository.models import (
    RepositoryIngestionArtifact,
    RepositoryIngestionResult,
)

from delbot_platform.workflows.factory import (
    WorkflowFactory,
)


class RepositoryIngestionApplication:
    """
    Repository ingestion use case.
    """

    def __init__(
        self,
        workflow: RepositoryIngestionWorkflow | None = None,
    ) -> None:

        self.workflow = (
            workflow
            if workflow is not None
            else WorkflowFactory.repository_ingestion()
        )

    async def execute(
        self,
        repository: RepositoryItem,
    ) -> tuple[
        RepositoryIngestionArtifact,
        RepositoryIngestionResult,
    ]:

        return await self.workflow.ingest_with_summary(
            repository,
        )
