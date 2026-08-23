from __future__ import annotations

from abc import ABC
from abc import abstractmethod


from delbot_platform.documents.chunking.chunk import (
    DocumentChunk,
)

from delbot_platform.documents.embedding.vector import (
    VectorRecord,
)


class EmbeddingService(ABC):


    @abstractmethod
    async def embed(
        self,
        chunks: list[DocumentChunk],
    ) -> list[VectorRecord]:

        pass