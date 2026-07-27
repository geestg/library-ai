from __future__ import annotations

from delbot_platform.repository.catalog.models import (
    CatalogRecord,
)

from delbot_platform.repository.models import (
    RepositoryItem,
    RepositoryStatus,
)


class CatalogAdapter:
    """
    Convert Repository Catalog models into the legacy
    RepositoryItem model.

    This adapter allows the existing RepositoryService
    to migrate gradually without breaking downstream code.
    """

    @staticmethod
    def to_repository_item(
        record: CatalogRecord,
    ) -> RepositoryItem:

        return RepositoryItem(

            id=record.document_id,

            title=record.title,

            repository_url=record.url,

            local_path=record.pdf_path,

            status=(
                RepositoryStatus.PDF_AVAILABLE
                if record.has_pdf
                else RepositoryStatus.METADATA_ONLY
            ),

            metadata=record.metadata,

        )
