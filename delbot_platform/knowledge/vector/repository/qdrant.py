from __future__ import annotations


from qdrant_client import QdrantClient

from qdrant_client.models import (
    PointStruct,
)

from delbot_platform.knowledge.vector.models.record import (
    VectorRecord,
)

from delbot_platform.knowledge.vector.repository.base import (
    VectorRepository,
)



class QdrantRepository(
    VectorRepository,
):


    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        collection: str = "delbot_documents",
    ) -> None:


        self.client = QdrantClient(
            host=host,
            port=port,
        )


        self.collection = collection



    async def insert(
        self,
        records: list[VectorRecord],
    ) -> None:


        points = []


        for record in records:


            points.append(

                PointStruct(

                    id=record.id,

                    vector=record.vector,

                    payload=record.metadata,

                )

            )


        self.client.upsert(

            collection_name=self.collection,

            points=points,

        )



    async def search(
        self,
        vector: list[float],
        limit: int = 5,
    ) -> list[VectorRecord]:


        results = self.client.search(

            collection_name=self.collection,

            query_vector=vector,

            limit=limit,

        )


        records = []


        for item in results:


            records.append(

                VectorRecord(

                    id=str(
                        item.id
                    ),

                    vector=[],

                    metadata=item.payload or {},

                )

            )


        return records