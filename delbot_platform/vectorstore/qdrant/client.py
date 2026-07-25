from __future__ import annotations

from pathlib import Path
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)


class QdrantVectorStore:

    def __init__(
        self,
        path: str = "data/qdrant",
        collection: str = "delbot_documents",
        vector_size: int = 1024,
    ) -> None:

        self.collection = collection
        self.vector_size = vector_size

        Path(path).mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = QdrantClient(
            path=path,
        )

    # =====================================================
    # Collection
    # =====================================================

    def create_collection(
        self,
    ) -> None:

        if self.collection_exists():
            return

        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
        )

    def collection_exists(
        self,
    ) -> bool:

        collections = (
            self.client
            .get_collections()
            .collections
        )

        return any(
            item.name == self.collection
            for item in collections
        )

    def collection_info(
        self,
    ) -> Any:

        return self.client.get_collection(
            self.collection,
        )

    # =====================================================
    # CRUD
    # =====================================================

    def upsert(
        self,
        points: list[PointStruct],
    ) -> None:

        self.client.upsert(
            collection_name=self.collection,
            points=points,
        )

    def delete_document(
        self,
        document_id: str,
    ) -> None:

        self.client.delete(
            collection_name=self.collection,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(
                            value=document_id,
                        ),
                    )
                ]
            ),
        )

    def retrieve(
        self,
        ids: list[str],
    ):

        return self.client.retrieve(
            collection_name=self.collection,
            ids=ids,
        )

    # =====================================================
    # Search
    # =====================================================

    def search(
        self,
        **kwargs,
    ):

        return self.client.search(
            collection_name=self.collection,
            **kwargs,
        )

    def scroll(
        self,
        **kwargs,
    ):

        return self.client.scroll(
            collection_name=self.collection,
            **kwargs,
        )

    def count(
        self,
    ) -> int:

        result = self.client.count(
            collection_name=self.collection,
        )

        return result.count

    # =====================================================
    # Utility
    # =====================================================

    def health(
        self,
    ) -> bool:

        try:
            self.client.get_collections()
            return True
        except Exception:
            return False

    def close(
        self,
    ) -> None:

        self.client.close()
