from fastapi import APIRouter

from app.rag.qdrant_client import client

router = APIRouter(prefix="/debug", tags=["Debug"])

COLLECTION_NAME = "skripsi_collection"


@router.get("/collection")
async def debug_collection():

    try:

        collections = client.get_collections()

        collection_exists = any(
            c.name == COLLECTION_NAME
            for c in collections.collections
        )

        if not collection_exists:
            return {
                "status": "error",
                "message": f"Collection '{COLLECTION_NAME}' does not exist"
            }

        collection_info = client.get_collection(
            collection_name=COLLECTION_NAME
        )

        sample_points = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=3,
            with_payload=True,
            with_vectors=False
        )

        formatted_points = []

        for point in sample_points[0]:

            payload = point.payload or {}

            formatted_points.append({
                "id": point.id,
                "source_file": payload.get("source_file"),
                "page": payload.get("page"),
                "chunk_index": payload.get("chunk_index"),
                "text_preview": (
                    payload.get("text", "")[:300]
                    if payload.get("text")
                    else None
                )
            })

        return {
            "status": "success",
            "collection_name": COLLECTION_NAME,
            "vectors_count": collection_info.points_count,
            "indexed_vectors": collection_info.indexed_vectors_count,
            "vector_dimension": (
                collection_info.config.params.vectors.size
            ),
            "sample_points": formatted_points
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }