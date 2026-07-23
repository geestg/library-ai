from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from delbot_platform.knowledge.extraction.extraction_result import (
    ExtractionResult,
)
from delbot_platform.knowledge.models.document_chunk import (
    DocumentChunk,
)


class KnowledgeExtractor(ABC):

    @abstractmethod
    def extract(
        self,
        chunk: DocumentChunk,
    ) -> ExtractionResult:
        """
        Extract knowledge from a document chunk.
        """

        raise NotImplementedError
