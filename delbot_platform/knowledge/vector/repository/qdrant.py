from __future__ import annotations

from qdrant_client.models import PointStruct

from delbot_platform.knowledge.vector.models.record import (
    VectorRecord,
)
from delbot_platform.knowledge.vector.repository.base import (
    VectorRepository,
)
from delbot_platform.vectorstore.qdrant.singleton import (
    get_qdrant_store,
)


class QdrantRepository(
    VectorRepository,
):

    def __init__(
        self,
        collection: str = "delbot_documents",
    ) -> None:

        self.store = get_qdrant_store()
        self.collection = collection

        self.store.create_collection()

    async def insert(
        self,
        records: list[VectorRecord],
    ) -> None:

        points: list[PointStruct] = []

        for record in records:

            points.append(
                PointStruct(
                    id=record.id,
                    vector=record.vector,
                    payload=record.metadata,
                )
            )

        self.store.upsert(
            points,
        )

    async def search(
        self,
        vector: list[float],
        limit: int = 5,
    ) -> list[VectorRecord]:

        results = self.store.search(
            query_vector=vector,
            limit=limit,
        )

        records: list[VectorRecord] = []

        for item in results:

            payload = item.payload or {}

            records.append(
                VectorRecord(
                    id=str(item.id),
                    score=float(item.score),
                    vector=None,
                    metadata=payload,
                )
            )

        return records
