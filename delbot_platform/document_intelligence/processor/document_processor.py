from __future__ import annotations

from pathlib import Path

from delbot_platform.document_intelligence.loader.document_loader import (
    DocumentLoader,
)
from delbot_platform.document_intelligence.pipeline.document_pipeline import (
    DocumentPipeline,
)


class DocumentProcessor:

    def __init__(
        self,
        loader: DocumentLoader,
        pipeline: DocumentPipeline,
    ) -> None:
        self._loader = loader
        self._pipeline = pipeline

    def process(
        self,
        path: str | Path,
    ):

        loaded_document = self._loader.load(
            Path(path),
        )

        return self._pipeline.process(
            loaded_document,
        )
