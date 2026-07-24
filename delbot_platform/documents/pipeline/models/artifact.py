from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.documents.chunking.chunk import (
    DocumentChunk,
)
from delbot_platform.documents.registry.document import (
    DocumentRecord,
)
from delbot_platform.documents.structure.section.section import (
    DocumentSection,
)
from delbot_platform.vectors import (
    VectorRecord,
)


@dataclass(slots=True)
class DocumentIndexArtifact:
    """
    Canonical output of the Documents domain.

    This artifact represents the complete indexing result and is the
    contract between the Documents domain and downstream domains such
    as Knowledge, Research, and future Graph pipelines.

    It intentionally contains the full semantic representation of a
    processed document rather than summary statistics.
    """

    document: DocumentRecord

    sections: list[DocumentSection] = field(
        default_factory=list,
    )

    chunks: list[DocumentChunk] = field(
        default_factory=list,
    )

    vectors: list[VectorRecord] = field(
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

        return len(
            self.sections,
        )

    @property
    def chunk_count(
        self,
    ) -> int:

        return len(
            self.chunks,
        )

    @property
    def vector_count(
        self,
    ) -> int:

        return len(
            self.vectors,
        )
