from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from delbot_platform.document_intelligence.loader.loaded_document import (
    LoadedDocument,
)
from delbot_platform.document_intelligence.models.parsed_document import (
    ParsedDocument,
)


class DocumentParser(ABC):

    @abstractmethod
    def parse(
        self,
        document: LoadedDocument,
    ) -> ParsedDocument:
        ...
