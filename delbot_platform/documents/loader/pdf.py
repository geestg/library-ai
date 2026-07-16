from __future__ import annotations

from pathlib import Path

import fitz


class PDFLoader:

    def load(
        self,
        pdf_path: str,
    ) -> fitz.Document:

        path = Path(
            pdf_path,
        )

        if not path.exists():

            raise FileNotFoundError(
                f"PDF not found: {path}"
            )

        if path.suffix.lower() != ".pdf":

            raise ValueError(
                f"Unsupported file type: {path}"
            )

        return fitz.open(
            path,
        )