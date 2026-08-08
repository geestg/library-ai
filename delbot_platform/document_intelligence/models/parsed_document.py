from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from ..loader.loaded_document import LoadedDocument
from .page import Page


@dataclass(slots=True)
class ParsedDocument:
    source_document: LoadedDocument

    pages: list[Page] = field(
        default_factory=list,
    )

    headings: list[Any] = field(
        default_factory=list,
    )

    paragraphs: list[Any] = field(
        default_factory=list,
    )
