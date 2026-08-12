from __future__ import annotations

from dataclasses import dataclass

from ..parser.parsed_document import ParsedDocument


@dataclass(slots=True)
class ChunkedDocument:
    source_document: ParsedDocument
    chunks: list
    metadata: dict
