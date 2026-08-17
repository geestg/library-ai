from __future__ import annotations

from pathlib import Path

from delbot_platform.documents.registry.document import (
    DocumentRecord,
)
from delbot_platform.documents.registry.factory import (
    DocumentRepositoryFactory,
)
from delbot_platform.documents.registry.repository import (
    DocumentRepository,
)
from delbot_platform.repository.catalog.loader import (
    CatalogLoader,
)


class DocumentRegistryManager:

    def __init__(
        self,
        repository: DocumentRepository | None = None,
    ) -> None:

        self.repository = (
            repository
            if repository is not None
            else DocumentRepositoryFactory.build(
                "filesystem",
            )
        )

    def resolve(
        self,
        pdf_path: str,
        document_id: str | None = None,
    ) -> DocumentRecord:

        path = Path(
            pdf_path,
        )

        if not document_id:
            document_id = path.stem

        existing = self.repository.get(
            document_id,
        )

        metadata = self._catalog_metadata(
            path,
        )

        if existing is not None:
            changed = False

            if metadata:
                title = metadata.get("title")
                author = metadata.get("author")
                year = metadata.get("year")

                if title and existing.title != title:
                    existing.title = title
                    changed = True

                if author and existing.author != author:
                    existing.author = author
                    changed = True

                if year is not None:
                    try:
                        normalized_year = int(year)
                    except (TypeError, ValueError):
                        normalized_year = None

                    if (
                        normalized_year is not None
                        and existing.year != normalized_year
                    ):
                        existing.year = normalized_year
                        changed = True

            if changed:
                self.repository.save(
                    existing,
                )

            return existing

        record = DocumentRecord(
            id=document_id,
            source=path.name,
            pdf_path=str(
                path,
            ),
            title=(
                metadata.get("title")
                if metadata
                else None
            ),
            author=(
                metadata.get("author")
                if metadata
                else None
            ),
            year=(
                self._normalize_year(
                    metadata.get("year")
                )
                if metadata
                else None
            ),
        )

        self.repository.save(
            record,
        )

        return record

    def _catalog_metadata(
        self,
        pdf_path: Path,
    ) -> dict:
        catalog_path = (
            Path(__file__).resolve().parents[2]
            / "repository_data"
            / "metadata"
            / "repository_catalog.json"
        )

        if not catalog_path.exists():
            return {}

        try:
            catalog = CatalogLoader(
                str(catalog_path),
            ).load()
        except Exception:
            return {}

        target = str(
            pdf_path,
        ).replace(
            "\\",
            "/",
        )

        target_name = pdf_path.name

        for record in catalog:
            record_path = str(
                record.pdf_path or "",
            ).replace(
                "\\",
                "/",
            )

            if (
                record_path == target
                or Path(record_path).name == target_name
            ):
                return {
                    "title": record.title,
                    "author": record.author,
                    "year": record.year,
                }

        return {}

    def _normalize_year(
        self,
        value,
    ) -> int | None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def get(
        self,
        document_id: str,
    ) -> DocumentRecord | None:

        return self.repository.get(
            document_id,
        )

    def exists(
        self,
        document_id: str,
    ) -> bool:

        return self.repository.exists(
            document_id,
        )

    def list(
        self,
    ) -> list[
        DocumentRecord
    ]:

        return self.repository.list()

    def remove(
        self,
        document_id: str,
    ) -> bool:

        return self.repository.remove(
            document_id,
        )
