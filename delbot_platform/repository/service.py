from __future__ import annotations

from dataclasses import replace

from delbot_platform.repository.ingestion import (
    DatasetLoader,
)
from delbot_platform.repository.models import (
    RepositoryItem,
    RepositoryScanResult,
)
from delbot_platform.repository.resolver import (
    LocalPDFResolver,
)


class RepositoryService:
    """
    Repository orchestration service.

    Responsibilities:

    - load repository metadata
    - resolve PDF artifacts
    - provide repository state
    """

    def __init__(
        self,
        dataset_path: str = "backend/app/dataset/skripsi_dataset.json",
        pdf_resolver: LocalPDFResolver | None = None,
    ) -> None:

        self.loader = DatasetLoader(
            dataset_path,
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

        self.items = self.loader.load()

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
