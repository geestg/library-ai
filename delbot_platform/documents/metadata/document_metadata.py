from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DocumentMetadata:
    """
    Canonical metadata describing one indexed PDF.
    """

    document_id: str

    source: str

    pages: int

    blocks: int

    sections: int

    chunks: int

    language: str = "id"

    repository_id: str | None = None

    title: str | None = None

    authors: list[str] | None = None

    year: int | None = None

    attributes: dict = None

    def __post_init__(self) -> None:

        if self.attributes is None:

            self.attributes = {}