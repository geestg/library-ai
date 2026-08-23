from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from delbot_platform.documents.loader.source import (
    DocumentSource,
)
from delbot_platform.documents.models.document import (
    Document,
)


class DocumentParser(ABC):

    @abstractmethod
    def parse(
        self,
        source: DocumentSource,
    ) -> Document:
        ...