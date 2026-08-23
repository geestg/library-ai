from __future__ import annotations

from abc import ABC, abstractmethod


class RepositoryProvider(ABC):


    @abstractmethod
    def resolve_pdf(
        self,
        url: str,
    ) -> str:
        pass
