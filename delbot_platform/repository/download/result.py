from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PDFDownloadResult:
    document_id: str

    success: bool

    path: str | None = None

    status: str = "unknown"

    error: str | None = None
