from __future__ import annotations

from delbot_platform.documents.classification.page_region import (
    PageRegion,
)


class PageClassifier:


    def classify(
        self,
        page_number: int,
        text: str = "",
    ) -> PageRegion:


        upper = text.upper()


        if page_number == 1:

            return PageRegion.COVER


        front_keywords = [
            "ABSTRAK",
            "ABSTRACT",
            "KATA PENGANTAR",
            "DAFTAR ISI",
            "LEMBAR PENGESAHAN",
        ]


        if any(
            keyword in upper
            for keyword in front_keywords
        ):

            return PageRegion.FRONT_MATTER


        return PageRegion.CONTENT