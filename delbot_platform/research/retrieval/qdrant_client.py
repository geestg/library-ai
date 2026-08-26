import os
import socket
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from delbot_platform.core.config import settings


def _init_qdrant_client():
    host = settings.QDRANT_HOST.replace("host.docker.internal", "127.0.0.1")
    port = settings.QDRANT_PORT
    try:
        s = socket.create_connection((host, port), timeout=1.0)
        s.close()
        print(f"[QDRANT CLIENT] Connected via network to {host}:{port}")
        return QdrantClient(host=host, port=port, timeout=120)
    except Exception:
        pass

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../qdrant_storage"))
    if os.path.exists(base_dir):
        try:
            print(f"[QDRANT CLIENT] Network port {port} offline. Using embedded local storage at: {base_dir}")
            return QdrantClient(path=base_dir)
        except Exception as lock_err:
            print(f"[QDRANT CLIENT WARNING] Local storage lock issue ({lock_err}). Using in-memory fallback.")
            return QdrantClient(":memory:")

    print(f"[QDRANT CLIENT] Defaulting to in-memory fallback client.")
    return QdrantClient(":memory:")


client = _init_qdrant_client()


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