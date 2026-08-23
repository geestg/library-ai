from __future__ import annotations


from qdrant_client import QdrantClient

from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct
)

import uuid



class QdrantStore:


    def __init__(
        self,
        collection="delbot_documents"
    ):

        self.client = QdrantClient(
            host="localhost",
            port=6333
        )

        self.collection = collection



    def create_collection(
        self,
        vector_size=1024
    ):


        if self.client.collection_exists(
            self.collection
        ):

            return



        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )



    def insert(
        self,
        vectors,
        payloads
    ):


        points=[]


        for vector,payload in zip(
            vectors,
            payloads
        ):

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload=payload
                )
            )


        self.client.upsert(
            collection_name=self.collection,
            points=points
        )


        return len(points)
