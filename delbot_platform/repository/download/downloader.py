from __future__ import annotations


from pathlib import Path


from delbot_platform.repository.download.result import (
    PDFDownloadResult,
)


class PDFDownloader:
    """
    PDF download orchestration layer.

    Responsibilities:

    - prepare storage directory
    - check existing PDF
    - save repository artifacts

    Remote download resolver will be added later.
    """


    def __init__(
        self,
        storage_path: str = "datasets/repository",
    ) -> None:

        self.storage = Path(
            storage_path
        )

        self.storage.mkdir(
            parents=True,
            exist_ok=True,
        )



    def exists(
        self,
        document_id: str,
    ) -> Path | None:

        folder = (
            self.storage
            / document_id
        )


        pdf = (
            folder
            / "thesis.pdf"
        )


        if pdf.exists():

            return pdf


        return None



    def prepare(
        self,
        document_id: str,
    ) -> Path:


        folder = (
            self.storage
            / document_id
        )


        folder.mkdir(
            parents=True,
            exist_ok=True,
        )


        return folder



    def register_existing(
        self,
        document_id: str,
        source: Path,
    ) -> PDFDownloadResult:


        target_dir = (
            self.prepare(
                document_id
            )
        )


        target = (
            target_dir
            / "thesis.pdf"
        )


        if not target.exists():

            target.write_bytes(
                source.read_bytes()
            )


        return PDFDownloadResult(

            document_id=document_id,

            success=True,

            path=str(target),

            status="available",

        )