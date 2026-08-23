from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class DocumentRecord:

    id: str

    source: str

    pdf_path: Path

    title: str | None = None

    author: str | None = None

    year: int | None = None