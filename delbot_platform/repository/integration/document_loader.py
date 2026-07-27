from __future__ import annotations

from pathlib import Path


class RepositoryDocumentLoader:
    """
    Discover available PDF documents directly from the repository.

    Repository layout:

    delbot_platform/
        repository_data/
            pdf/
                *.pdf
    """

    def __init__(
        self,
        repository_path: str = "delbot_platform/repository_data/pdf",
    ) -> None:

        self.repository_path = Path(repository_path)

    def load_available(
        self,
    ) -> list[dict]:

        if not self.repository_path.exists():
            raise FileNotFoundError(
                self.repository_path
            )

        documents: list[dict] = []

        for pdf in sorted(
            self.repository_path.glob("*.pdf")
        ):

            documents.append(
                {
                    "document_id": pdf.stem,
                    "pdf_path": str(pdf),
                    "source": pdf.name,
                }
            )

        return documents