from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from delbot_platform.document_intelligence.models.parsed_document import (
    ParsedDocument,
)
from delbot_platform.knowledge.models.document import (
    Document,
)


class DocumentBuilder(ABC):

    @abstractmethod
    def build(
        self,
        document: ParsedDocument,
    ) -> Document:
        ...
