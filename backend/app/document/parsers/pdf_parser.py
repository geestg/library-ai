import fitz
import pytesseract

from PIL import Image


# =====================================
# EXTRACT PDF PAGES
# =====================================

def extract_pdf_pages(pdf_path):

    doc = fitz.open(pdf_path)

    pages = []

    for page_number in range(len(doc)):

        page = doc.load_page(page_number)

        # =================================
        # NORMAL TEXT EXTRACTION
        # =================================

        text = page.get_text().strip()

        # =================================
        # OCR FALLBACK
        # =================================

        if not text:

            pix = page.get_pixmap()

            img = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            text = pytesseract.image_to_string(img)

            print(
                f"[OCR] Page {page_number + 1} processed"
            )

        pages.append({

            "page": page_number + 1,

            "text": text
        })

    return pages