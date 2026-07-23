from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from pathlib import Path

from delbot_platform.document_intelligence.loader.loaded_document import (
    LoadedDocument,
)


class DocumentLoader(ABC):

    @abstractmethod
    def load(
        self,
        source: Path,
    ) -> LoadedDocument:
        """
        Load a local document into an intermediate representation.
        """

        raise NotImplementedError
