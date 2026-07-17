from __future__ import annotations


from pathlib import Path


from delbot_platform.repository.models import (
    RepositoryItem,
)

from delbot_platform.repository.scanner import (
    CollectionScanner,
    ItemScanner,
)

from delbot_platform.repository.services import (
    RepositoryIngestionService,
)



class RepositoryCrawler:
    """
    Full repository crawling orchestration.

    Flow:

    Collection
        |
        v
    Items
        |
        v
    Ingestion
    """


    def __init__(
        self,
        collection_scanner: CollectionScanner,
        item_scanner: ItemScanner,
        ingestion_service: RepositoryIngestionService,
    ) -> None:

        self.collection_scanner = (
            collection_scanner
        )

        self.item_scanner = (
            item_scanner
        )

        self.ingestion_service = (
            ingestion_service
        )


    def crawl(
        self,
        destination: Path,
    ) -> list:


        results = []


        collections = (
            self.collection_scanner.scan()
        )


        for collection in collections:


            collection_id = (
                collection["id"]
            )


            items = (
                self.item_scanner.scan(
                    collection_id,
                )
            )


            for raw_item in items:


                item = RepositoryItem(
                    id=str(
                        raw_item["id"]
                    ),
                    collection_id=collection_id,
                    title=raw_item.get(
                        "name",
                        "",
                    ),
                )


                results.append(
                    item
                )


        return results
