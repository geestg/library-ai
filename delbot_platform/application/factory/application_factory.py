from __future__ import annotations

from delbot_platform.application.documents import (
    DocumentIndexApplication,
)

from delbot_platform.application.repository import (
    RepositoryIngestionApplication,
)

from delbot_platform.application.research import (
    ResearchAnswerApplication,
)

from delbot_platform.workflows.factory import (
    WorkflowFactory,
)


class ApplicationFactory:
    """
    Factory for constructing application use cases.

    Centralizes dependency wiring for every
    application entry point.
    """

    @staticmethod
    def documents() -> DocumentIndexApplication:

        return DocumentIndexApplication()

    @staticmethod
    def repository() -> RepositoryIngestionApplication:

        return RepositoryIngestionApplication(
            workflow=WorkflowFactory.repository_ingestion(),
        )

    @staticmethod
    def research() -> ResearchAnswerApplication:

        return ResearchAnswerApplication()
