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


# =====================================
# PROCESS DOCUMENT
# =====================================

def process_document(file_path):

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

            page["text"]

            for page in pages
        ])

        return {

            "type": "pdf",

            "pages": pages,

            "text": text
        }

    # =================================
    # IMAGE
    # =================================

    elif ext in [

        ".png",

        ".jpg",

        ".jpeg",

        ".webp"

    ]:

        text = extract_text_from_image(
            file_path
        )

        return {

            "type": "image",

            "pages": [

                {
                    "page": 1,
                    "text": text
                }
            ],

            "text": text
        }

    # =================================
    # DOCX
    # =================================

    elif ext == ".docx":

        text = parse_docx(
            file_path
        )

        return {

            "type": "docx",

            "pages": [

                {
                    "page": 1,
                    "text": text
                }
            ],

            "text": text
        }

    # =================================
    # XLSX
    # =================================

    elif ext in [

        ".xlsx",

        ".xls"

    ]:

        text = parse_xlsx(
            file_path
        )

        return {

            "type": "xlsx",

            "pages": [

                {
                    "page": 1,
                    "text": text
                }
            ],

            "text": text
        }

    # =================================
    # PPTX
    # =================================

    elif ext == ".pptx":

        text = parse_pptx(
            file_path
        )

        return {

            "type": "pptx",

            "pages": [

                {
                    "page": 1,
                    "text": text
                }
            ],

            "text": text
        }

    # =================================
    # TXT
    # =================================

    elif ext == ".txt":

        text = parse_txt(
            file_path
        )

        return {

            "type": "txt",

            "pages": [

                {
                    "page": 1,
                    "text": text
                }
            ],

            "text": text
        }

    # =================================
    # CSV
    # =================================

    elif ext == ".csv":

        text = parse_csv(
            file_path
        )

        return {

            "type": "csv",

            "pages": [

                {
                    "page": 1,
                    "text": text
                }
            ],

            "text": text
        }

    # =================================
    # UNSUPPORTED
    # =================================

    raise Exception(
        f"Unsupported file type: {ext}"
    )