from __future__ import annotations

import re


class AcademicHeadingDetector:


    def detect(
        self,
        text: str,
    ) -> bool:


        text = text.strip()


        if not text:

            return False


        upper = text.upper()


        patterns = [

            r"^BAB\s+[IVXLCDM]+",

            r"^\d+\.\d+\s+[A-Z]",

        ]


        for pattern in patterns:

            if re.match(
                pattern,
                upper,
            ):

                return True


        return False