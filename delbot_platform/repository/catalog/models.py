from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field


@dataclass(slots=True)
class CatalogRecord:
    """
    Unified repository record.

    This model represents a single thesis inside the repository
    regardless of whether the corresponding PDF is available.
    """

    document_id: str

    title: str

    author: str

    year: str

    abstract: str

    prodi: str

    url: str

    pdf_path: str | None = None

    has_pdf: bool = False

    metadata: dict = field(
        default_factory=dict,
    )


@dataclass(slots=True)
class RepositoryCatalog:
    """
    In-memory repository catalog.
    """

    records: list[CatalogRecord] = field(
        default_factory=list,
    )

    def __len__(self) -> int:
        return len(
            self.records
        )

    def __iter__(self):
        return iter(
            self.records
        )

    def add(
        self,
        record: CatalogRecord,
    ) -> None:

        self.records.append(
            record,
        )

    def all(
        self,
    ) -> list[CatalogRecord]:

        return list(
            self.records,
        )
