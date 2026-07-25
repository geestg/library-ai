from __future__ import annotations

from qdrant_client.models import PointStruct

from delbot_platform.vectorstore.qdrant.singleton import (
    get_qdrant_store,
)


class QdrantStorage:

    def __init__(
        self,
    ) -> None:

        self.store = get_qdrant_store()

    def ensure_collection(
        self,
        size: int,
    ) -> None:

        self.store.create_collection()

    def insert(
        self,
        vectors: list,
        payloads: list,
    ) -> int:

        points: list[PointStruct] = []

        for index, (vector, payload) in enumerate(
            zip(vectors, payloads)
        ):

            document_id = payload.get(
                "document_id",
                index,
            )

            points.append(
                PointStruct(
                    id=str(document_id),
                    vector=vector,
                    payload=payload,
                )
            )

        self.store.upsert(
            points,
        )

        return len(points)
