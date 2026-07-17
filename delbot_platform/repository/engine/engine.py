from __future__ import annotations


from delbot_platform.repository import (
    RepositoryCrawler,
)


class RepositoryEngine:


    def __init__(
        self,
        crawler: RepositoryCrawler,
        pipeline,
    ) -> None:


        self.crawler = crawler

        self.pipeline = pipeline



    def ingest_repository(
        self,
        repository_id: str,
    ):


        items = (
            self.crawler.scan(
                repository_id,
            )
        )


        results = []


        for item in items:

            result = (
                self.pipeline.execute(
                    item,
                )
            )

            results.append(
                result,
            )


        return results
