from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from pathlib import Path

from delbot_platform.repository.models import (
    RepositoryItem,
)


class FileDownloader(ABC):
    """
    Downloads repository files.

    Example:

        DSpace bitstream
        HTTP file
        Object storage

    """


    @abstractmethod
    def download(
        self,
        item: RepositoryItem,
        destination: Path,
    ) -> Path:
        ...
