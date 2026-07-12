import unicodedata

import fitz
import pytesseract

from PIL import Image


# =====================================
# MOJIBAKE MARKERS
# =====================================

MOJIBAKE_MARKERS = (

    "ΓÇ",

    "Γå",

    "┬",

    "├",

    "ÔÇ",

    "â€",

    "ï¿½",

)


# =====================================
# COUNT MOJIBAKE MARKERS
# =====================================

def count_mojibake_markers(
    text: str,
) -> int:

    if not text:

        return 0

    return sum(

        text.count(marker)

        for marker in MOJIBAKE_MARKERS

    )


# =====================================
# TRY CP437 UTF-8 REPAIR
# =====================================

def try_cp437_utf8_repair(
    text: str,
) -> str:

    if not text:

        return text

    try:

        repaired = (

            text
            .encode("cp437")
            .decode("utf-8")

        )

    except (
        UnicodeEncodeError,
        UnicodeDecodeError,
    ):

        return text

    original_score = (
        count_mojibake_markers(text)
    )

    repaired_score = (
        count_mojibake_markers(repaired)
    )

    # =================================
    # ACCEPT ONLY CLEAR IMPROVEMENT
    # =================================

    if repaired_score < original_score:

        return repaired

    return text


# =====================================
# NORMALIZE EXTRACTED TEXT
# =====================================

def normalize_extracted_text(
    text: str,
) -> str:

    if not text:

        return ""

    normalized = str(text)

    # =================================
    # NORMALIZE LINE ENDINGS
    # =================================

    normalized = normalized.replace(
        "\r\n",
        "\n",
    )

    normalized = normalized.replace(
        "\r",
        "\n",
    )

    # =================================
    # REPAIR KNOWN MOJIBAKE
    # =================================

    if count_mojibake_markers(
        normalized
    ):

        normalized = (
            try_cp437_utf8_repair(
                normalized
            )
        )

    # =================================
    # UNICODE NORMALIZATION
    # =================================

    normalized = unicodedata.normalize(
        "NFC",
        normalized,
    )

    # =================================
    # REMOVE NULL CHARACTERS
    # =================================

    normalized = normalized.replace(
        "\x00",
        "",
    )

    # =================================
    # TRIM TRAILING WHITESPACE
    # =================================

    lines = [

        line.rstrip()

        for line in normalized.splitlines()

    ]

    normalized = "\n".join(
        lines
    )

    return normalized.strip()


# =====================================
# EXTRACT PAGE TEXT
# =====================================

def extract_page_text(
    page,
) -> str:

    text = page.get_text(
        "text"
    )

    return normalize_extracted_text(
        text
    )


# =====================================
# EXTRACT PAGE WITH OCR
# =====================================

def extract_page_with_ocr(
    page,
    page_number: int,
) -> str:

    pix = page.get_pixmap(

        matrix=fitz.Matrix(
            2,
            2,
        ),

        alpha=False,

    )

    image = Image.frombytes(

        "RGB",

        [
            pix.width,
            pix.height,
        ],

        pix.samples,

    )

    text = pytesseract.image_to_string(
        image
    )

    print(
        f"[OCR] Page "
        f"{page_number} processed"
    )

    return normalize_extracted_text(
        text
    )


# =====================================
# EXTRACT PDF PAGES
# =====================================

def extract_pdf_pages(
    pdf_path,
):

    pages = []

    doc = fitz.open(
        pdf_path
    )

    try:

        for page_number in range(
            len(doc)
        ):

            page = doc.load_page(
                page_number
            )

            # =================================
            # NORMAL TEXT EXTRACTION
            # =================================

            text = extract_page_text(
                page
            )

            # =================================
            # OCR FALLBACK
            # =================================

            if not text:

                text = extract_page_with_ocr(

                    page=page,

                    page_number=(
                        page_number + 1
                    ),

                )

            # =================================
            # BUILD PAGE RESULT
            # =================================

            pages.append({

                "page":
                    page_number + 1,

                "text":
                    text,

            })

    finally:

        doc.close()

    return pages

