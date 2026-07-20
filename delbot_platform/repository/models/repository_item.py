from __future__ import annotations

from dataclasses import dataclass
from enum import Enum



class RepositoryStatus(str, Enum):

    METADATA_ONLY = "metadata_only"

    PDF_AVAILABLE = "pdf_available"

    FAILED = "failed"



@dataclass(slots=True)
class RepositoryItem:

    id: str

    title: str

    repository_url: str

    pdf_url: str | None = None

    local_path: str | None = None

    status: RepositoryStatus = (
        RepositoryStatus.METADATA_ONLY
    )

    metadata: dict | None = None