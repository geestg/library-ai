from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.documents.pipeline.models import (
    DocumentIndexArtifact,
)

from delbot_platform.knowledge.models import (
    Document,
)


@dataclass(slots=True)
class KnowledgeArtifact:
    """
    Canonical output produced by the
    Knowledge Pipeline.

    This artifact enriches the indexing
    artifact with knowledge-domain objects.
    """

    document_index: DocumentIndexArtifact

    document: Document | None = None

    entities: list = field(
        default_factory=list,
    )

    relations: list = field(
        default_factory=list,
    )

    citations: list = field(
        default_factory=list,
    )

    @property
    def document_id(
        self,
    ) -> str:

        return self.document_index.document_id

    @property
    def source(
        self,
    ) -> str:

        return self.document_index.source
