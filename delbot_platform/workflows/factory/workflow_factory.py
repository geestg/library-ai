from __future__ import annotations

from delbot_platform.documents.services import (
    DocumentIndexService,
)

from delbot_platform.knowledge.services import (
    KnowledgeService,
)

from delbot_platform.repository.service import (
    RepositoryService,
)

from delbot_platform.workflows.repository import (
    RepositoryIngestionWorkflow,
)


class WorkflowFactory:
    """
    Factory for constructing workflow instances.

    Workflow creation is centralized here so
    dependency wiring remains consistent.
    """

    @staticmethod
    def repository_ingestion(
    ) -> RepositoryIngestionWorkflow:

        return RepositoryIngestionWorkflow(
            repository=RepositoryService(),
            documents=DocumentIndexService(),
            knowledge=KnowledgeService(),
        )
