from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from delbot_platform.documents.registry.document import (
    DocumentRecord,
)


class DocumentRepository(ABC):

    @abstractmethod
    def get(
        self,
        document_id: str,
    ) -> DocumentRecord:
        ...

    @abstractmethod
    def save(
        self,
        record: DocumentRecord,
    ) -> None:
        ...

    @abstractmethod
    def exists(
        self,
        document_id: str,
    ) -> bool:
        ...