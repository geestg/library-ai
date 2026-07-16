from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from pathlib import Path


class DocumentSource(ABC):

    @abstractmethod
    def exists(
        self,
    ) -> bool:
        ...

    @abstractmethod
    def path(
        self,
    ) -> Path:
        ...

    @abstractmethod
    def bytes(
        self,
    ) -> bytes:
        ...