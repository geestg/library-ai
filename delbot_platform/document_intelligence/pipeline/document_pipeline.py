from __future__ import annotations

from abc import ABC, abstractmethod

from ...documents.models.document import Document
from .pipeline_result import PipelineResult


class DocumentPipeline(ABC):
    @abstractmethod
    def process(
        self,
        document: Document,
    ) -> PipelineResult:
        raise NotImplementedError
