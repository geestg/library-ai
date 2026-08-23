from __future__ import annotations

from enum import Enum


class HeadingLevel(str, Enum):
    """
    Semantic heading level.

    UNKNOWN
        Level has not been resolved yet.

    TITLE
        Document title.

    H1-H5
        Section hierarchy.
    """

    UNKNOWN = "unknown"

    TITLE = "title"

    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
