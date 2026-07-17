from __future__ import annotations


from delbot_platform.repository.scanner.base import (
    RepositoryScanner,
)



class CollectionScanner(
    RepositoryScanner,
):
    """
    Scan repository collections.
    """


    def __init__(
        self,
        client,
    ) -> None:

        self.client = client


    def scan(
        self,
    ) -> list[dict]:

        return self.client.collections()
