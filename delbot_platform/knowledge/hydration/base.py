from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class DocumentProvider(
    ABC,
):

    @abstractmethod
    async def citation(
        self,
        document_id: str,
        page_start: int,
        page_end: int,
        section: str,
        text: str,
    ) -> Citation:
        """
        Resolve a RetrievalResult into
        a complete Research Citation.
        """
        raise NotImplementedError
