from __future__ import annotations

from enum import Enum


class PageType(str, Enum):

    UNKNOWN = "unknown"

    COVER = "cover"

    TABLE_OF_CONTENTS = "table_of_contents"

    PREFACE = "preface"

    CHAPTER = "chapter"

    BIBLIOGRAPHY = "bibliography"

    APPENDIX = "appendix"

    BLANK = "blank"

    def __str__(
        self,
    ) -> str:

        return self.value