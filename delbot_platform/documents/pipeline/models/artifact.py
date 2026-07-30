from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.documents.models.document_chunk import (
    DocumentChunk,
)
from delbot_platform.documents.metadata.document_metadata import (
    DocumentMetadata,
)
from delbot_platform.documents.registry.document import (
    DocumentRecord,
)
from delbot_platform.documents.structure.section.section import (
    DocumentSection,
)
from delbot_platform.documents.embedding.models import (
    EmbeddingVector,
)


@dataclass(slots=True)
class DocumentIndexArtifact:
    """
    Canonical output of the Documents domain.

    This artifact represents the complete indexing result and is the
    contract between the Documents domain and downstream domains such
    as Knowledge, Research, and future Graph pipelines.
    """

    document: DocumentRecord

    metadata: DocumentMetadata

    sections: list[DocumentSection] = field(
        default_factory=list,
    )

    chunks: list[DocumentChunk] = field(
        default_factory=list,
    )

    vectors: list[EmbeddingVector] = field(
        default_factory=list,
    )

    @property
    def document_id(
        self,
    ) -> str:
        return self.document.id

    @property
    def source(
        self,
    ) -> str:
        return self.document.source

    @property
    def page_count(
        self,
    ) -> int:

        if not self.sections:
            return 0

        return max(
            section.page_end
            for section in self.sections
        )

    @property
    def block_count(
        self,
    ) -> int:

        return sum(
            section.block_count
            for section in self.sections
        )

    @property
    def section_count(
        self,
    ) -> int:
        return len(self.sections)

    @property
    def chunk_count(
        self,
    ) -> int:
        return len(self.chunks)

    @property
    def vector_count(
        self,
    ) -> int:
        return len(self.vectors)