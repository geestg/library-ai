from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Any


class Backend(ABC):

    @abstractmethod
    def open(
        self,
        source: Path,
    ) -> Any:
        """
        Open a document using the concrete backend.

        Returns
        -------
        Backend-specific document object.
        """

        raise NotImplementedError

    @abstractmethod
    def close(
        self,
        document: Any,
    ) -> None:
        """
        Release backend resources.
        """

        raise NotImplementedError
