import re


def clean_text(text: str) -> str:

    if not text:
        return ""

    # remove excessive newlines
    text = re.sub(r"\n+", "\n", text)

    # remove excessive spaces
    text = re.sub(r"\s+", " ", text)

    # remove page numbers
    text = re.sub(r"\b\d+\b", "", text)

    # trim
    text = text.strip()

    return text