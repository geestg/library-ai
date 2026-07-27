from __future__ import annotations

import json

from pathlib import Path

from delbot_platform.repository.catalog.models import (
    CatalogRecord,
    RepositoryCatalog,
)


class CatalogLoader:
    """
    Load Repository Catalog from JSON.
    """

    def __init__(
        self,
        catalog_path: str,
    ) -> None:

        self.catalog_path = Path(
            catalog_path,
        )

    def exists(
        self,
    ) -> bool:

        return self.catalog_path.exists()

    def load(
        self,
    ) -> RepositoryCatalog:

        if not self.catalog_path.exists():

            raise FileNotFoundError(
                self.catalog_path,
            )

        data = json.loads(
            self.catalog_path.read_text(
                encoding="utf-8",
            )
        )

        catalog = RepositoryCatalog()

        for row in data:

            catalog.add(

                CatalogRecord(

                    document_id=row["document_id"],

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

                    pdf_path=row.get(
                        "pdf_path",
                    ),

                    has_pdf=row.get(
                        "has_pdf",
                        False,
                    ),

                    metadata=row.get(
                        "metadata",
                        {},
                    ),

                )

            )

        return catalog
