from pathlib import Path
from pypdf import PdfReader


class PDFParser:


    def extract(
        self,
        pdf_path: str,
    ) -> list[dict]:

        path = Path(pdf_path)

        reader = PdfReader(path)

        pages = []

        for index, page in enumerate(reader.pages):

            text = page.extract_text() or ""

            pages.append(
                {
                    "page": index + 1,
                    "text": text,
                }
            )


        return pages
