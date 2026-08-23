from __future__ import annotations


from qdrant_client import QdrantClient

from qdrant_client.models import (
    Distance,
    VectorParams,
)



class QdrantCollectionManager:


    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        collection: str = "delbot_documents",
        vector_size: int = 1024,
    ) -> None:


        self.client = QdrantClient(
            host=host,
            port=port,
        )


        self.collection = collection

        self.vector_size = vector_size



    def exists(
        self,
    ) -> bool:


        collections = (
            self.client
            .get_collections()
            .collections
        )


        names = [

            item.name

            for item in collections

        ]


        return (
            self.collection
            in names
        )



    def create(
        self,
    ) -> None:


        self.client.create_collection(

            collection_name=self.collection,

            vectors_config=VectorParams(

                size=self.vector_size,

                distance=Distance.COSINE,

            ),

        )



    def ensure(
        self,
    ) -> None:


        if not self.exists():

            self.create()