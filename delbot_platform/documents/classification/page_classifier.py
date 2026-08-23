from __future__ import annotations

from delbot_platform.documents.classification.page_type import (
    PageType,
)


class PageClassifier:

    def classify(
        self,
        page,
    ) -> PageType:

        text = page.get_text().strip()

        upper = text.upper()

        if not upper:

            return PageType.BLANK

        if page.number == 0:

            return PageType.COVER

        if "DAFTAR ISI" in upper:

            return PageType.TABLE_OF_CONTENTS

        if "DAFTAR PUSTAKA" in upper:

            return PageType.BIBLIOGRAPHY

        if "LAMPIRAN" in upper:

            return PageType.APPENDIX

        if "BAB " in upper:

            return PageType.CHAPTER

        if "KATA PENGANTAR" in upper:

            return PageType.PREFACE

        return PageType.UNKNOWN