from fastapi import APIRouter

from app.rag.embedder import get_embedding
from app.rag.qdrant_client import client

router = APIRouter()


@router.get("/search")
def semantic_search(query: str):

    embedding = get_embedding(query)

    results = client.query_points(
        collection_name="skripsi_collection",
        query=embedding,
        limit=5
    )

    return [
        {
            "score": point.score,
            "data": point.payload
        }
        for point in results.points
    ]