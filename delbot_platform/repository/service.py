from __future__ import annotations

from dataclasses import replace

from delbot_platform.repository.catalog import (
    CatalogAdapter,
    CatalogLoader,
)

from delbot_platform.repository.models import (
    RepositoryItem,
    RepositoryScanResult,
)

from delbot_platform.repository.resolver import (
    LocalPDFResolver,
)


DEFAULT_CATALOG = (
    "delbot_platform/repository_data/metadata/"
    "repository_catalog.json"
)


class RepositoryService:
    """
    Repository orchestration service.

    Source of truth:

        repository_catalog.json
    """

    def __init__(
        self,
        catalog_path: str = DEFAULT_CATALOG,
        pdf_resolver: LocalPDFResolver | None = None,
    ) -> None:

        self.loader = CatalogLoader(
            catalog_path,
        )

        self.pdf_resolver = (
            pdf_resolver
            if pdf_resolver is not None
            else LocalPDFResolver()
        )

        self.items: list[RepositoryItem] = []

    def load(
        self,
    ) -> list[RepositoryItem]:

        catalog = self.loader.load()

        self.items = [

            CatalogAdapter.to_repository_item(
                record,
            )

            for record in catalog

        ]

        return self.items

    def resolve_pdf(
        self,
        item: RepositoryItem,
    ) -> RepositoryItem:

        pdf = self.pdf_resolver.resolve(
            item.id,
        )

        if pdf is None:
            return item

        return replace(
            item,
            local_path=str(pdf),
        )

    def scan(
        self,
    ) -> RepositoryScanResult:

        items = self.load()

        available = 0
        missing = 0

        results: list[RepositoryItem] = []

        for item in items:

            resolved = self.resolve_pdf(
                item,
            )

            results.append(
                resolved,
            )

            if resolved.local_path:
                available += 1
            else:
                missing += 1

        return RepositoryScanResult(

            total=len(results),

            pdf_available=available,

            pdf_missing=missing,

            items=results,

        )
