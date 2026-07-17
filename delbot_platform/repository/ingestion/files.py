from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from delbot_platform.repository.models import (
    RepositoryItem,
)


class FileParser(ABC):
    """
    Extract repository files.

    Responsible for identifying:

    - PDF
    - supplementary files
    - assets

    """


    @abstractmethod
    def parse(
        self,
        item: RepositoryItem,
        raw: dict,
    ) -> RepositoryItem:
        ...
