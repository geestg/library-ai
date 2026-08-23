from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.repository.models.repository_item import (
    RepositoryItem,
)


@dataclass(slots=True)
class RepositoryScanResult:
    """
    Repository scan summary.
    """

    total: int

    pdf_available: int

    pdf_missing: int

    items: list[RepositoryItem] = field(
        default_factory=list,
    )
