from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Manifest:

    document_id: str

    checksum: str

    pdf_path: str

    processed: bool = False
