from __future__ import annotations

from delbot_platform.repository.models import (
    Repository,
    Collection,
    RepositoryItem,
)

from delbot_platform.repository.scanner.base import (
    RepositoryScanner,
)


class DSpaceScanner(
    RepositoryScanner,
):
    """
    DSpace repository scanner.

    Initial implementation is intentionally empty.

    Responsibilities later:

    - Discover collections
    - Discover items
    - Parse metadata
    - Find PDF bitstreams

    """


    def scan_repository(
        self,
        repository: Repository,
    ) -> list[Collection]:

        raise NotImplementedError(
            "DSpace collection scanner not implemented"
        )


    def scan_collection(
        self,
        collection: Collection,
    ) -> list[RepositoryItem]:

        raise NotImplementedError(
            "DSpace item scanner not implemented"
        )


    def scan_item(
        self,
        item: RepositoryItem,
    ) -> RepositoryItem:

        raise NotImplementedError(
            "DSpace item refresh not implemented"
        )

