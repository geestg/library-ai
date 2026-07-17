from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from delbot_platform.repository.models import (
    RepositoryItem,
)


class MetadataParser(ABC):
    """
    Metadata parser contract.

    Converts external repository metadata
    into DELBot repository model.
    """


    @abstractmethod
    def parse(
        self,
        item: RepositoryItem,
        raw: dict,
    ) -> RepositoryItem:
        ...
