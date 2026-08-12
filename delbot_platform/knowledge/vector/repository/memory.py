from __future__ import annotations


from delbot_platform.knowledge.vector.models.record import (
    VectorRecord,
)


from delbot_platform.knowledge.vector.repository.base import (
    VectorRepository,
)



class InMemoryVectorRepository(
    VectorRepository,
):


    def __init__(
        self,
    ) -> None:

        self.records: list[VectorRecord] = []



    async def insert(
        self,
        records: list[VectorRecord],
    ) -> None:


        self.records.extend(
            records
        )



    async def search(
        self,
        vector: list[float],
        limit: int = 5,
        document_ids: list[str] | None = None,
    ) -> list[VectorRecord]:


        return self.records[:limit]