from __future__ import annotations

import uuid

from qdrant_client.models import PointStruct

from delbot_platform.ai.client.embedding_client import (
    EmbeddingClient,
)
from delbot_platform.vectorstore.qdrant.singleton import (
    get_qdrant_store,
)


class QdrantIngest:

    def __init__(
        self,
    ) -> None:

        self.store = get_qdrant_store()
        self.store.create_collection()

        self.embedding = EmbeddingClient()

    def ensure_collection(
        self,
    ) -> None:

        self.store.create_collection()

    def insert(
        self,
        text: str,
        metadata: dict,
    ) -> bool:

        vector = self.embedding.embed(
            text,
        )

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "text": text,
                **metadata,
            },
        )

        self.store.upsert(
            [point],
        )

        return True
