from __future__ import annotations

from pathlib import Path

from delbot_platform.documents.registry.document import (
    DocumentRecord,
)
from delbot_platform.documents.registry.factory import (
    DocumentRepositoryFactory,
)
from delbot_platform.documents.registry.repository import (
    DocumentRepository,
)


class DocumentRegistryManager:

    def __init__(
        self,
        repository: DocumentRepository | None = None,
    ) -> None:

        self.repository = (
            repository
            if repository is not None
            else DocumentRepositoryFactory.build(
                "filesystem",
            )
        )

    def resolve(
        self,
        pdf_path: str,
    ) -> DocumentRecord:

        path = Path(
            pdf_path,
        )

        document_id = (
            path.parent.name
        )

        existing = self.repository.get(
            document_id,
        )

        if existing is not None:

            return existing

        record = DocumentRecord(
            id=document_id,
            source=path.name,
            pdf_path=str(
                path,
            ),
        )

        self.repository.save(
            record,
        )

        return record

    def get(
        self,
        document_id: str,
    ) -> DocumentRecord | None:

        return self.repository.get(
            document_id,
        )

    def exists(
        self,
        document_id: str,
    ) -> bool:

        return self.repository.exists(
            document_id,
        )

    def list(
        self,
    ) -> list[
        DocumentRecord
    ]:

        return self.repository.list()

    def remove(
        self,
        document_id: str,
    ) -> bool:

        return self.repository.remove(
            document_id,
        )