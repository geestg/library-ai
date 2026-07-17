from __future__ import annotations


from delbot_platform.repository.crawler import (
    RepositoryCrawler,
)

from delbot_platform.repository.services.ingestion_service import (
    RepositoryIngestionService,
)

from delbot_platform.repository.state import (
    CheckpointManager,
    DocumentState,
    DocumentStatus,
)



class RepositoryCrawlService:
    """
    High level repository crawling orchestration.

    Responsible for:

    - crawling repository
    - checking checkpoint
    - triggering ingestion
    - updating state
    """

    def __init__(
        self,
        crawler: RepositoryCrawler,
        ingestion: RepositoryIngestionService,
        checkpoint: CheckpointManager | None = None,
    ) -> None:


        self.crawler = crawler

        self.ingestion = ingestion

        self.checkpoint = (
            checkpoint
            if checkpoint is not None
            else CheckpointManager()
        )


    def process(
        self,
        repository_id: str,
    ) -> list[DocumentState]:


        results: list[DocumentState] = []


        items = self.crawler.crawl(
            repository_id,
        )


        for item in items:


            existing = self.checkpoint.load(
                item.id,
            )


            if (
                existing is not None
                and existing.status
                == DocumentStatus.PROCESSED
            ):

                results.append(
                    existing
                )

                continue



            downloading = DocumentState(
                document_id=item.id,
                status=DocumentStatus.DOWNLOADING,
            )


            self.checkpoint.save(
                downloading,
            )


            try:

                manifest = (
                    self.ingestion.ingest(
                        item,
                    )
                )


                completed = DocumentState(
                    document_id=item.id,
                    status=DocumentStatus.PROCESSED,
                    checksum=manifest.checksum,
                )


                self.checkpoint.save(
                    completed,
                )


                results.append(
                    completed,
                )


            except Exception as exc:


                failed = DocumentState(
                    document_id=item.id,
                    status=DocumentStatus.FAILED,
                    error=str(exc),
                )


                self.checkpoint.save(
                    failed,
                )


                results.append(
                    failed,
                )


        return results
