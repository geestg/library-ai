from __future__ import annotations

from enum import Enum


class PageRegion(
    str,
    Enum,
):

    COVER = "cover"

    FRONT_MATTER = "front_matter"

    CONTENT = "content"

    REFERENCES = "references"

    UNKNOWN = "unknown"