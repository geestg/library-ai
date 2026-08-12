from __future__ import annotations

from abc import ABC, abstractmethod

from ..parser.parsed_document import ParsedDocument
from .chunked_document import ChunkedDocument


class DocumentChunker(ABC):
    @abstractmethod
    def chunk(
        self,
        document: ParsedDocument,
    ) -> ChunkedDocument:
        raise NotImplementedError
