from __future__ import annotations

from pathlib import Path

from delbot_platform.documents.loader.source import (
    DocumentSource,
)


class LocalDocumentSource(DocumentSource):
    """
    Local filesystem implementation of DocumentSource.
    """

    def __init__(
        self,
        path: str | Path,
    ) -> None:

        self._path = Path(path)

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