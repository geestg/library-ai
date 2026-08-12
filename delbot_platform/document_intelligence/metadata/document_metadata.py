from __future__ import annotations

from abc import ABC, abstractmethod

from ..chunker.chunked_document import ChunkedDocument
from .metadata_result import MetadataResult


class DocumentMetadata(ABC):
    @abstractmethod
    def extract(
        self,
        document: ChunkedDocument,
    ) -> MetadataResult:
        raise NotImplementedError
