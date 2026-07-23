from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from delbot_platform.document_intelligence.models.parsed_document import (
    ParsedDocument,
)


class DocumentAnalyzer(ABC):

    @abstractmethod
    def analyze(
        self,
        document: ParsedDocument,
    ) -> ParsedDocument:
        pass
