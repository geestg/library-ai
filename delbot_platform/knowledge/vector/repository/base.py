from __future__ import annotations

from abc import ABC
from abc import abstractmethod


from delbot_platform.knowledge.vector.models.record import (
    VectorRecord,
)



class VectorRepository(ABC):


    @abstractmethod
    async def insert(
        self,
        records: list[VectorRecord],
    ) -> None:

        pass



    @abstractmethod
    async def search(
        self,
        vector: list[float],
        limit: int = 5,
    ) -> list[VectorRecord]:

        pass