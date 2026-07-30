from __future__ import annotations

from uuid import NAMESPACE_DNS, uuid5

from qdrant_client.models import PointStruct

from delbot_platform.vectorstore.qdrant.singleton import (
    get_qdrant_store,
)
from delbot_platform.vectors import (
    VectorRecord,
)


class QdrantRepository:

    def __init__(
        self,
        store=None,
    ) -> None:

        self.store = (
            store
            if store is not None
            else get_qdrant_store()
        )

        self.store.create_collection()

    def delete_document(
        self,
        document_id: str,
    ) -> None:

        self.store.delete_document(
            document_id,
        )

    def save(
        self,
        vectors: list[VectorRecord],
    ) -> int:

        if not vectors:
            return 0

        first_payload = vectors[0].metadata

        document_id = first_payload.get(
            "document_id",
        )

        if document_id:
            self.delete_document(
                document_id,
            )

        points: list[PointStruct] = []

        for vector in vectors:

            payload = vector.metadata

            point_id = str(
                uuid5(
                    NAMESPACE_DNS,
                    vector.id,
                )
            )

            points.append(
                PointStruct(
                    id=point_id,
                    vector=vector.vector,
                    payload=payload,
                )
            )

        self.store.upsert(
            points,
        )

        return len(points)

    def count(
        self,
    ) -> int:

        return self.store.count()
