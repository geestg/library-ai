from __future__ import annotations

from abc import ABC
from abc import abstractmethod


from delbot_platform.documents.models.document_chunk import (
    DocumentChunk,
)
from delbot_platform.documents.embedding.models import (
    EmbeddingVector,
)



class EmbeddingService(ABC):


    @abstractmethod
    async def embed(
        self,
        chunks: list[DocumentChunk],
    ) -> list[EmbeddingVector]:

        pass