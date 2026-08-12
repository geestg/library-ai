from __future__ import annotations

from abc import ABC, abstractmethod

from ..metadata.metadata_result import MetadataResult
from .indexed_document import IndexedDocument


class DocumentIndexer(ABC):
    @abstractmethod
    def index(
        self,
        document: MetadataResult,
    ) -> IndexedDocument:
        raise NotImplementedError
