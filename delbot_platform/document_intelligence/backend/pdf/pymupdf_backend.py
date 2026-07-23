from __future__ import annotations

from pathlib import Path
from typing import Any

import fitz

from delbot_platform.document_intelligence.backend.backend import (
    Backend,
)


class PyMuPDFBackend(Backend):

    def open(
        self,
        source: Path,
    ) -> Any:
        """
        Open a PDF document using PyMuPDF.
        """

        return fitz.open(source)

    def close(
        self,
        document: Any,
    ) -> None:
        """
        Close a PyMuPDF document.
        """

        if document is None:
            return

        document.close()