from __future__ import annotations

from qdrant_client.models import PointStruct

from delbot_platform.vectorstore.qdrant.singleton import (
    get_qdrant_store,
)


class QdrantStore:

    def __init__(
        self,
        collection: str = "delbot_documents",
    ) -> None:

        self.store = get_qdrant_store()
        self.collection = collection

    def create_collection(
        self,
        vector_size: int = 1024,
    ) -> None:

        self.store.create_collection()

    def insert(
        self,
        vectors: list[list[float]],
        payloads: list[dict],
    ) -> int:

        points: list[PointStruct] = []

        for index, (vector, payload) in enumerate(
            zip(vectors, payloads)
        ):

            document_id = payload.get(
                "document_id",
                f"vector-{index}",
            )

            points.append(
                PointStruct(
                    id=document_id,
                    vector=vector,
                    payload=payload,
                )
            )

        self.store.upsert(
            points,
        )

        return len(points)
