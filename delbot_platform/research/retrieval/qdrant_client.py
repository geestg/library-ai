from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import socket
from delbot_platform.core.config import settings


def _get_working_host(host: str, port: int) -> str:
    if host == "host.docker.internal":
        try:
            s = socket.create_connection(("host.docker.internal", port), timeout=1.5)
            s.close()
            return "host.docker.internal"
        except Exception:
            print(f"[QDRANT CLIENT] 'host.docker.internal:{port}' unreachable. Falling back to '127.0.0.1'.")
            return "127.0.0.1"
    return host


qdrant_host = _get_working_host(settings.QDRANT_HOST, settings.QDRANT_PORT)
print(f"[QDRANT CLIENT] Connected to {qdrant_host}:{settings.QDRANT_PORT}")

client = QdrantClient(
    host=qdrant_host,
    port=settings.QDRANT_PORT,
    timeout=120,
)


def ensure_collection_exists(
    collection_name: str,
    vector_size: int = 768,
):
    try:
        collections = client.get_collections()
        exists = any(c.name == collection_name for c in collections.collections)
        if not exists:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
            print(f"[QDRANT] Collection created: {collection_name}")
        else:
            print(f"[QDRANT] Collection already exists: {collection_name}")
    except Exception as e:
        print(f"[QDRANT ERROR] ensure_collection_exists failed: {e}")