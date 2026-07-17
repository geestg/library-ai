from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RepositoryItem:
    """
    External repository item.

    source_url:
        Original file/location from repository provider.

    pdf_path:
        Local downloaded artifact used by DELBot pipeline.

    """

    id: str

    collection_id: str

    title: str

    metadata_path: str | None = None

    source_url: str | None = None

    pdf_path: str | None = None