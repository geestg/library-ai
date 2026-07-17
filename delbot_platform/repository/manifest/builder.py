from __future__ import annotations

import hashlib

from pathlib import Path

from delbot_platform.repository.models import (
    Manifest,
)


class ManifestBuilder:
    """
    Builds repository document manifest.

    Manifest stores document state,
    checksum and processing status.
    """


    def build(
        self,
        document_id: str,
        pdf_path: Path,
    ) -> Manifest:

        checksum = self._checksum(
            pdf_path,
        )

        return Manifest(
            document_id=document_id,
            checksum=checksum,
            pdf_path=str(
                pdf_path,
            ),
            processed=False,
        )


    def _checksum(
        self,
        path: Path,
    ) -> str:

        if not path.exists():

            return ""


        sha256 = hashlib.sha256()


        with path.open(
            "rb",
        ) as file:

            for chunk in iter(
                lambda: file.read(8192),
                b"",
            ):

                sha256.update(
                    chunk,
                )


        return sha256.hexdigest()
