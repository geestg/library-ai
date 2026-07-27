from __future__ import annotations

import json
from dataclasses import asdict

from pathlib import Path

from delbot_platform.repository.catalog.models import (
    CatalogRecord,
)


class RepositoryCatalogBuilder:
    """
    Build repository_catalog.json from repository metadata.

    Current version:
        Metadata only.

    Future:
        Metadata + PDF mapping.
    """

    def __init__(
        self,
        metadata_path: str,
        output_path: str,
    ) -> None:

        self.metadata_path = Path(
            metadata_path,
        )

        self.output_path = Path(
            output_path,
        )

    def _document_id(
        self,
        url: str,
    ) -> str:

        parts = (
            url.rstrip("/")
            .split("/")
        )

        if len(parts) >= 2:

            return (
                parts[-2]
                + "-"
                + parts[-1]
            )

        return parts[-1]

    def build(
        self,
    ) -> int:

        rows = json.loads(

            self.metadata_path.read_text(
                encoding="utf-8",
            )

        )

        catalog = []

        for row in rows:

            record = CatalogRecord(

                document_id=self._document_id(
                    row["url"],
                ),

                title=row.get(
                    "title",
                    "",
                ),

                author=row.get(
                    "author",
                    "",
                ),

                year=row.get(
                    "year",
                    "",
                ),

                abstract=row.get(
                    "abstract",
                    "",
                ),

                prodi=row.get(
                    "prodi",
                    "",
                ),

                url=row.get(
                    "url",
                    "",
                ),

                pdf_path=None,

                has_pdf=False,

                metadata=row,

            )

            catalog.append(
                asdict(record)
            )

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.output_path.write_text(

            json.dumps(
                catalog,
                indent=2,
                ensure_ascii=False,
            ),

            encoding="utf-8",

        )

        return len(
            catalog,
        )
