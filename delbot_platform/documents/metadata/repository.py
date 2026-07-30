from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from delbot_platform.documents.metadata.document_metadata import (
    DocumentMetadata,
)


class DocumentMetadataRepository:
    """
    Persist canonical metadata generated during indexing.
    """

    def __init__(
        self,
        root: str | Path = (
            "delbot_platform/repository_data/processed/documents"
        ),
    ) -> None:

        self.root = Path(root)

        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def directory(
        self,
        document_id: str,
    ) -> Path:

        return self.root / document_id

    def metadata_path(
        self,
        document_id: str,
    ) -> Path:

        return (
            self.directory(
                document_id,
            )
            / "metadata.json"
        )

    def save(
        self,
        metadata: DocumentMetadata,
    ) -> Path:

        directory = self.directory(
            metadata.document_id,
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        target = self.metadata_path(
            metadata.document_id,
        )

        target.write_text(
            json.dumps(
                asdict(metadata),
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return target

    def exists(
        self,
        document_id: str,
    ) -> bool:

        return self.metadata_path(
            document_id,
        ).exists()

    def load(
        self,
        document_id: str,
    ) -> DocumentMetadata | None:

        target = self.metadata_path(
            document_id,
        )

        if not target.exists():

            return None

        data = json.loads(
            target.read_text(
                encoding="utf-8",
            )
        )

        return DocumentMetadata(
            **data,
        )