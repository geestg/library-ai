import os

from app.document.parsers.pdf_parser import (
    extract_pdf_pages
)

from app.document.ocr_engine import (
    extract_text_from_image
)

from app.document.parsers.docx_parser import (
    parse_docx
)

from app.document.parsers.xlsx_parser import (
    parse_xlsx
)

from app.document.parsers.pptx_parser import (
    parse_pptx
)

from app.document.parsers.txt_parser import (
    parse_txt
)

from app.document.parsers.csv_parser import (
    parse_csv
)

from app.document.document_classifier import (
    classify_document
)


# =====================================
# BUILD RESULT
# =====================================

def build_result(
    file_type,
    pages,
    text
):

    document_type = classify_document(
        text
    )

    return {

        "type":
            file_type,

        "document_type":
            document_type,

        "pages":
            pages,

        "text":
            text

    }


# =====================================
# PROCESS DOCUMENT
# =====================================

def process_document(
    file_path
):

    ext = os.path.splitext(
        file_path
    )[1].lower()

    # =================================
    # PDF
    # =================================

    if ext == ".pdf":

        pages = extract_pdf_pages(
            file_path
        )

        text = "\n".join([

            page.get(
                "text",
                ""
            )

            for page in pages

        ])

        return build_result(

            file_type="pdf",

            pages=pages,

            text=text

        )

    # =================================
    # IMAGE
    # =================================

    if ext in [

        ".png",
        ".jpg",
        ".jpeg",
        ".webp"

    ]:

        text = extract_text_from_image(
            file_path
        )

        pages = [

            {
                "page": 1,
                "text": text
            }

        ]

        return build_result(

            file_type="image",

            pages=pages,

            text=text

        )

    # =================================
    # DOCX
    # =================================

    if ext == ".docx":

        text = parse_docx(
            file_path
        )

        pages = [

            {
                "page": 1,
                "text": text
            }

        ]

        return build_result(

            file_type="docx",

            pages=pages,

            text=text

        )

    # =================================
    # XLSX / XLS
    # =================================

    if ext in [

        ".xlsx",
        ".xls"

    ]:

        text = parse_xlsx(
            file_path
        )

        pages = [

            {
                "page": 1,
                "text": text
            }

        ]

        return build_result(

            file_type="xlsx",

            pages=pages,

            text=text

        )

    # =================================
    # PPTX
    # =================================

    if ext == ".pptx":

        text = parse_pptx(
            file_path
        )

        pages = [

            {
                "page": 1,
                "text": text
            }

        ]

        return build_result(

            file_type="pptx",

            pages=pages,

            text=text

        )

    # =================================
    # TXT
    # =================================

    if ext == ".txt":

        text = parse_txt(
            file_path
        )

        pages = [

            {
                "page": 1,
                "text": text
            }

        ]

        return build_result(

            file_type="txt",

            pages=pages,

            text=text

        )

    # =================================
    # CSV
    # =================================

    if ext == ".csv":

        text = parse_csv(
            file_path
        )

        pages = [

            {
                "page": 1,
                "text": text
            }

        ]

        return build_result(

            file_type="csv",

            pages=pages,

            text=text

        )

    # =================================
    # UNSUPPORTED
    # =================================

    raise Exception(

        f"Unsupported file type: {ext}"

    )
