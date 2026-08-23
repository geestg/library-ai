from __future__ import annotations


from pathlib import Path


from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
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



    def create_collection(
        self,
    ) -> None:


        collections = (
            self.client
            .get_collections()
            .collections
        )


        exists = any(

            item.name == self.collection

            for item in collections

        )


        if exists:

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