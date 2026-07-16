from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ChunkPolicy:
    """
    Configuration for semantic document chunking.

    Values are intentionally conservative and can later
    be overridden from configuration.
    """

    max_characters: int = 2000

    min_characters: int = 400

    overlap_characters: int = 200

    preserve_heading: bool = True

    preserve_page_boundary: bool = False

    merge_short_paragraphs: bool = True

    keep_empty_lines: bool = False

    strip_whitespace: bool = True

    max_pages_per_chunk: int = 3