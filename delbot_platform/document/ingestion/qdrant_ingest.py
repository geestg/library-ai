from __future__ import annotations


import uuid


from qdrant_client import QdrantClient

from qdrant_client.models import (
    PointStruct,
    VectorParams,
    Distance,
)


from delbot_platform.research.embedding.query import (
    QueryEmbedding,
)



class QdrantIngest:


    COLLECTION = "delbot_documents"


    def __init__(self):

        self.client = QdrantClient(
            host="127.0.0.1",
            port=6333,
        )


        self.embedding = QueryEmbedding()



    def ensure_collection(self):

        exists = self.client.collection_exists(
            self.COLLECTION
        )


        if not exists:

            self.client.create_collection(
                collection_name=self.COLLECTION,
                vectors_config=VectorParams(
                    size=32,
                    distance=Distance.COSINE,
                ),
            )



    def insert(
        self,
        text:str,
        metadata:dict,
    ):


        vector = self.embedding.embed(
            text
        )


        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "text":text,
                **metadata
            },
        )


        self.client.upsert(
            collection_name=self.COLLECTION,
            points=[
                point
            ],
        )


        return True
