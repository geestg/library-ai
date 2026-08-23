from pathlib import Path

try:
    import fitz  # PyMuPDF
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False

try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False


class PDFParser:

    def extract(
        self,
        pdf_path: str,
    ) -> list[dict]:

        path = Path(pdf_path)
        pages = []

        if HAS_FITZ:
            doc = fitz.open(str(path))
            for index, page in enumerate(doc):
                text = page.get_text() or ""
                pages.append(
                    {
                        "page": index + 1,
                        "text": text,
                    }
                )
            doc.close()
            return pages

        elif HAS_PYPDF:
            reader = PdfReader(path)
            for index, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                pages.append(
                    {
                        "page": index + 1,
                        "text": text,
                    }
                )
            return pages

        else:
            raise RuntimeError("Neither PyMuPDF (fitz) nor pypdf is installed.")

