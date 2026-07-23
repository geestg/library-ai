from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class LoadedDocument:

    source_path: Path

    backend_document: Any

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )
