from __future__ import annotations


from pathlib import Path


from delbot_platform.repository.models import (
    RepositoryItem,
)


from delbot_platform.repository.dspace import (
    DSpaceDownloader,
)


from delbot_platform.repository.services.repository_service import (
    RepositoryService,
)


class RepositoryArtifactService:
    """
    Resolve local PDF artifact.

    Responsibility:

    - Check existing PDF
    - Download missing PDF
    - Update RepositoryItem
    """


    def __init__(
        self,
        repository_service: RepositoryService | None = None,
        downloader: DSpaceDownloader | None = None,
    ) -> None:


        self.repository_service = (
            repository_service
            if repository_service is not None
            else RepositoryService()
        )


        self.downloader = (
            downloader
            if downloader is not None
            else DSpaceDownloader()
        )


    def resolve(
        self,
        item_id: str,
    ) -> Path:


        item = (
            self.repository_service
            .get_item(
                item_id,
            )
        )


        if item is None:

            raise ValueError(
                f"Repository item not found: {item_id}"
            )


        #
        # Existing artifact
        #

        if item.pdf_path:

            path = Path(
                item.pdf_path,
            )

            if path.exists() and path.stat().st_size > 0:

                return path


        #
        # Download artifact
        #

        destination = (
            Path(
                "repository"
            )
            /
            item.id
        )


        pdf = self.downloader.download(
            item,
            destination,
        )


        updated = RepositoryItem(
            id=item.id,
            collection_id=item.collection_id,
            title=item.title,
            metadata_path=item.metadata_path,
            source_url=item.source_url,
            pdf_path=str(pdf),
        )


        self.repository_service.register_item(
            updated,
        )


        return pdf
