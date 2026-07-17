from __future__ import annotations


from delbot_platform.repository.scanner import (
    CollectionScanner,
)


class CollectionCrawler:
    """
    Handles repository collection discovery.
    """


    def __init__(
        self,
        scanner: CollectionScanner,
    ) -> None:

        self.scanner = scanner


    def crawl(
        self,
    ) -> list[dict]:

        return self.scanner.scan()
