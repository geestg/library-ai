from __future__ import annotations


from qdrant_client import QdrantClient

from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
)



class QdrantStorage:


    def __init__(self):
        import os
        from delbot_platform.core.config import settings
        host = os.environ.get("QDRANT_HOST", settings.QDRANT_HOST)
        port = int(os.environ.get("QDRANT_PORT", settings.QDRANT_PORT))
        is_in_docker = os.path.exists("/.dockerenv") or os.environ.get("DOCKER_CONTAINER") == "1"
        if not is_in_docker and "host.docker.internal" in host:
            host = "127.0.0.1"

        self.client = QdrantClient(
            host=host,
            port=port,
        )


        self.collection="delbot_documents"



    def ensure_collection(
        self,
        size:int,
    ):


        collections=[
            c.name
            for c in self.client.get_collections().collections
        ]


        if self.collection not in collections:

            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=size,
                    distance=Distance.COSINE,
                ),
            )



    def insert(
        self,
        vectors:list,
        payloads:list,
    ):


        points=[]


        for idx,vector in enumerate(vectors):

            points.append(
                PointStruct(
                    id=idx,
                    vector=vector,
                    payload=payloads[idx],
                )
            )


        self.client.upsert(
            collection_name=self.collection,
            points=points,
        )
