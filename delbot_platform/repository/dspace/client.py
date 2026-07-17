from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class DSpaceClient(ABC):
    """
    Abstract DSpace API client.

    Responsible for communication with
    external DSpace repository.
    """


    @abstractmethod
    def get_item(
        self,
        item_id: str,
    ) -> dict:
        ...


    @abstractmethod
    def get_metadata(
        self,
        item_id: str,
    ) -> dict:
        ...


    @abstractmethod
    def get_files(
        self,
        item_id: str,
    ) -> list[dict]:
        ...
