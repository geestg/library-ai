from __future__ import annotations

from pathlib import Path

from delbot_platform.repository import (
    RepositoryItem,
)

from delbot_platform.repository.ingestion import (
    MetadataParser,
    FileParser,
    FileDownloader,
)

from delbot_platform.repository.manifest import (
    ManifestBuilder,
)

from delbot_platform.repository.storage import (
    FilesystemRepositoryStorage,
)



class RepositoryIngestionService:
    """
    Orchestrates repository ingestion pipeline.
    """


    def __init__(
        self,
        metadata_parser: MetadataParser,
        file_parser: FileParser,
        downloader: FileDownloader,
    ) -> None:


        self.metadata_parser = (
            metadata_parser
        )

        self.file_parser = (
            file_parser
        )

        self.downloader = (
            downloader
        )

        self.storage = (
            FilesystemRepositoryStorage()
        )

        self.manifest = (
            ManifestBuilder()
        )


    def ingest(
        self,
        item: RepositoryItem,
        metadata: dict,
        files: dict,
        destination: Path,
    ):


        item = self.metadata_parser.parse(
            item,
            metadata,
        )


        item = self.file_parser.parse(
            item,
            files,
        )


        pdf = self.downloader.download(
            item,
            destination,
        )


        manifest = self.manifest.build(
            item.id,
            pdf,
        )


        self.storage.save_item(
            item,
        )


        self.storage.save_manifest(
            manifest,
        )


        return manifest
