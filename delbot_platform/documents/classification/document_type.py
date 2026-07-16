from __future__ import annotations

from enum import Enum


class DocumentBlockType(
    str,
    Enum,
):

    TITLE = "title"

    AUTHOR = "author"

    INSTITUTION = "institution"

    DATE = "date"

    HEADING = "heading"

    PARAGRAPH = "paragraph"

    UNKNOWN = "unknown"