from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from delbot_platform.documents.loader.source import (
    DocumentSource,
)


class PDFBackend(ABC):

    @abstractmethod
    def open(
        self,
        source: DocumentSource,
    ) -> None:
        ...

    @abstractmethod
    def metadata(
        self,
    ) -> dict:
        ...

    @abstractmethod
    def page_count(
        self,
    ) -> int:
        ...

    @abstractmethod
    def page(
        self,
        index: int,
    ):
        ...

    @abstractmethod
    def toc(
        self,
    ) -> list:
        ...

    @abstractmethod
    def close(
        self,
    ) -> None:
        ...