from __future__ import annotations

from delbot_platform.documents.registry.document import (
    DocumentRecord,
)
from delbot_platform.documents.registry.repository import (
    DocumentRepository,
)


class InMemoryDocumentRepository(
    DocumentRepository,
):

    def __init__(
        self,
    ) -> None:

        self._documents: dict[
            str,
            DocumentRecord,
        ] = {}

    def save(
        self,
        document: DocumentRecord,
    ) -> None:

        self._documents[
            document.id
        ] = document

    def get(
        self,
        document_id: str,
    ) -> DocumentRecord | None:

        return self._documents.get(
            document_id,
        )

    def exists(
        self,
        document_id: str,
    ) -> bool:

        return (
            document_id
            in self._documents
        )

    def remove(
        self,
        document_id: str,
    ) -> bool:

        if not self.exists(
            document_id,
        ):
            return False

        del self._documents[
            document_id
        ]

        return True

    def list(
        self,
    ) -> list[
        DocumentRecord
    ]:

        return list(
            self._documents.values()
        )

    def clear(
        self,
    ) -> None:

        self._documents.clear()