from __future__ import annotations

from delbot_platform.documents.registry.repository import (
    DocumentRepository,
)
from delbot_platform.documents.registry.memory import (
    InMemoryDocumentRepository,
)
from delbot_platform.documents.registry.filesystem import (
    FilesystemDocumentRepository,
)


class DocumentRepositoryFactory:

    @staticmethod
    def build(
        backend: str = "filesystem",
    ) -> DocumentRepository:

        backend = backend.lower()

        if backend == "memory":

            return InMemoryDocumentRepository()

        if backend == "filesystem":

            return FilesystemDocumentRepository()

        raise ValueError(
            f"Unknown document repository: {backend}"
        )