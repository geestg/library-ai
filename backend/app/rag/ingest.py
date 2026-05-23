import json
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.rag.qdrant_client import client
from app.rag.embedder import get_embedding

COLLECTION_NAME = "skripsi_collection"

def create_collection():

    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if COLLECTION_NAME not in names:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=768,
                distance=Distance.COSINE
            )
        )

def ingest_data():

    create_collection()

    with open("/app/datasets/skripsi_dataset.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    points = []

    for idx, item in enumerate(data):

        text = f"""
        Judul: {item.get('judul', '')}
        Abstrak: {item.get('abstrak', '')}
        """

        embedding = get_embedding(text)

        points.append(
            PointStruct(
                id=idx,
                vector=embedding,
                payload=item
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print("INGEST SUCCESS")

if __name__ == "__main__":
    ingest_data()