from __future__ import annotations


from delbot_platform.repository.scanner.base import (
    RepositoryScanner,
)



class ItemScanner(
    RepositoryScanner,
):
    """
    Scan repository items.
    """


    def __init__(
        self,
        client,
    ) -> None:

        self.client = client


    def scan(
        self,
        collection_id: str,
    ) -> list[dict]:

        return self.client.items(
            collection_id,
        )
