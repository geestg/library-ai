from __future__ import annotations

import re


class HeadingScorer:


    ROMAN_NUMBERS = {
        "I",
        "II",
        "III",
        "IV",
        "V",
        "VI",
        "VII",
        "VIII",
        "IX",
        "X",
    }


    def score(
        self,
        text: str,
        font_size: float = 0,
        bold: bool = False,
    ) -> float:


        text = text.strip()


        if not text:

            return 0.0


        score = 0.0


        upper = text.upper()


        words = text.split()


        #
        # BAB detection
        #

        if len(words) >= 2:

            first = words[0].upper()

            second = words[1].upper()


            if (
                first == "BAB"
                and second in self.ROMAN_NUMBERS
            ):

                score += 0.8



        #
        # Numbered section
        #

        if re.match(
            r"^\d+\.\d+\s+",
            text,
        ):

            score += 0.7



        #
        # Style hints
        #

        if bold:

            score += 0.1


        if font_size >= 14:

            score += 0.1



        #
        # Paragraph penalty
        #

        if len(words) > 12:

            score -= 0.5


        if text.lower().startswith(
            "bab ini"
        ):

            score -= 0.8


        return max(
            0.0,
            min(
                score,
                1.0,
            )
        )