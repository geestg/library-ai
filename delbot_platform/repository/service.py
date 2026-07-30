from __future__ import annotations

import json
from pathlib import Path
from typing import List

from .catalog import CatalogAdapter
from .models import RepositoryItem, RepositoryStatus


class RepositoryService:

    def __init__(self) -> None:

        self.root = Path(__file__).resolve().parents[1]

        self.metadata_dir = (
            self.root
            / "repository_data"
            / "metadata"
        )

        self.runtime_dir = (
            self.root
            / "repository_data"
            / "runtime"
        )

        self.catalog_file = (
            self.metadata_dir
            / "repository_catalog.json"
        )

        self.overlay_file = (
            self.runtime_dir
            / "repository_overlay.json"
        )

    # -----------------------------------------------------------------

    def scan(self) -> List[RepositoryItem]:

        if self.overlay_file.exists():
            items = self._scan_overlay()

            if items:
                return items

        return self._scan_catalog()

    # -----------------------------------------------------------------

    def _scan_overlay(self) -> List[RepositoryItem]:

        try:

            data = json.loads(
                self.overlay_file.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:

            data = []

        items: List[RepositoryItem] = []

        for row in data:

            pdf_path = row.get("pdf_path")

            status_value = row.get(
                "status",
                RepositoryStatus.METADATA_ONLY.value,
            )

            try:
                status = RepositoryStatus(status_value)
            except Exception:
                status = RepositoryStatus.METADATA_ONLY

            metadata = {
                "author": row.get("author"),
                "year": row.get("year"),
                "abstract": row.get("abstract"),
                "prodi": row.get("prodi"),
                "resolution": row.get("resolution"),
                "pdf_uuid": row.get("pdf_uuid"),
                "has_pdf": row.get("has_pdf"),
            }

            items.append(

                RepositoryItem(

                    id=row.get("document_id", ""),

                    title=row.get("title", ""),

                    repository_url=row.get("url", ""),

                    pdf_url=pdf_path,

                    local_path=pdf_path,

                    status=status,

                    metadata=metadata,

                )

            )

        return items

    # -----------------------------------------------------------------

    def _scan_catalog(self) -> List[RepositoryItem]:

        adapter = CatalogAdapter(
            self.catalog_file
        )

        return adapter.load()

