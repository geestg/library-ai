from __future__ import annotations

from abc import ABC, abstractmethod

from .parsed_document import ParsedDocument
from ..loader.loaded_document import LoadedDocument


class DocumentParser(ABC):
    @abstractmethod
    def parse(
        self,
        document: LoadedDocument,
    ) -> ParsedDocument:
        raise NotImplementedError
