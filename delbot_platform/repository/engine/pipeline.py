from __future__ import annotations

from dataclasses import dataclass


from delbot_platform.repository import (
    RepositoryItem,
    Manifest,
)


@dataclass(slots=True)
class RepositoryPipelineResult:

    item_id: str

    manifest: Manifest

    success: bool = True

    error: str | None = None



class RepositoryPipeline:

    """
    Repository ingestion pipeline.

    Flow:

        RepositoryItem
              |
              v
        Ingestion
              |
              v
        Manifest
    """


    def __init__(
        self,
        ingestion_service,
        manifest_builder,
    ) -> None:

        self.ingestion_service = (
            ingestion_service
        )

        self.manifest_builder = (
            manifest_builder
        )


    def execute(
        self,
        item: RepositoryItem,
    ) -> RepositoryPipelineResult:


        try:

            manifest = (
                self.ingestion_service.ingest(
                    item,
                )
            )


            manifest = (
                self.manifest_builder.build(
                    manifest,
                )
            )


            return RepositoryPipelineResult(

                item_id=item.id,

                manifest=manifest,

                success=True,

            )


        except Exception as exc:

            return RepositoryPipelineResult(

                item_id=item.id,

                manifest=None,

                success=False,

                error=str(exc),

            )
