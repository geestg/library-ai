from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..chunker.chunked_document import ChunkedDocument


@dataclass(slots=True)
class MetadataResult:
    source_document: ChunkedDocument
    metadata: dict[str, Any]
    sections: list[str]
