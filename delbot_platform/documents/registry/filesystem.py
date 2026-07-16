from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from delbot_platform.documents.registry.document import (
    DocumentRecord,
)
from delbot_platform.documents.registry.repository import (
    DocumentRepository,
)


class FilesystemDocumentRepository(
    DocumentRepository,
):

    def __init__(
        self,
        root: str | Path = "repository",
    ) -> None:

        self.root = Path(
            root,
        )

        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    #
    # Internal
    #

    def _directory(
        self,
        document_id: str,
    ) -> Path:

        return self.root / document_id

    def _metadata(
        self,
        document_id: str,
    ) -> Path:

        return (
            self._directory(
                document_id,
            )
            / "metadata.json"
        )

    #
    # CRUD
    #

    def save(
        self,
        document: DocumentRecord,
    ) -> None:

        directory = self._directory(
            document.id,
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        metadata = self._metadata(
            document.id,
        )

        metadata.write_text(
            json.dumps(
                asdict(document),
                indent=2,
            ),
            encoding="utf-8",
        )

    def get(
        self,
        document_id: str,
    ) -> DocumentRecord | None:

        metadata = self._metadata(
            document_id,
        )

        if not metadata.exists():

            return None

        data = json.loads(
            metadata.read_text(
                encoding="utf-8",
            )
        )

        return DocumentRecord(
            **data,
        )

    def exists(
        self,
        document_id: str,
    ) -> bool:

        return self._metadata(
            document_id,
        ).exists()

    def remove(
        self,
        document_id: str,
    ) -> bool:

        directory = self._directory(
            document_id,
        )

        if not directory.exists():

            return False

        for file in directory.iterdir():

            file.unlink()

        directory.rmdir()

        return True

    def list(
        self,
    ) -> list[
        DocumentRecord
    ]:

        result: list[
            DocumentRecord
        ] = []

        for directory in self.root.iterdir():

            if not directory.is_dir():

                continue

            metadata = (
                directory
                / "metadata.json"
            )

            if not metadata.exists():

                continue

            data = json.loads(
                metadata.read_text(
                    encoding="utf-8",
                )
            )

            result.append(
                DocumentRecord(
                    **data,
                )
            )

        return result

    def clear(
        self,
    ) -> None:

        for document in self.list():

            self.remove(
                document.id,
            )