from __future__ import annotations

from pathlib import Path

from delbot_platform.documents.loader.source import (
    DocumentSource,
)


class LocalDocumentSource(DocumentSource):

    def __init__(
        self,
        file: str | Path,
    ) -> None:

        self._path = Path(file)

    def exists(
        self,
    ) -> bool:

        return self._path.exists()

    def path(
        self,
    ) -> Path:

        return self._path

    def bytes(
        self,
    ) -> bytes:

        return self._path.read_bytes()