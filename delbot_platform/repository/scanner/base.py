from __future__ import annotations

from abc import ABC
from abc import abstractmethod



class RepositoryScanner(ABC):
    """
    Base repository scanner.

    Responsible for discovering
    repository resources.
    """


    @abstractmethod
    def scan(
        self,
    ):
        ...