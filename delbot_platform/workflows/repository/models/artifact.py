from __future__ import annotations

from dataclasses import dataclass

from delbot_platform.documents.pipeline.models import (
    DocumentIndexArtifact,
)

from delbot_platform.knowledge.pipeline.models import (
    KnowledgeArtifact,
)

from delbot_platform.repository.models import (
    RepositoryItem,
)


@dataclass(slots=True)
class RepositoryIngestionArtifact:
    """
    Canonical artifact produced by the
    repository ingestion workflow.
    """

    repository: RepositoryItem

    document: DocumentIndexArtifact

    knowledge: KnowledgeArtifact
