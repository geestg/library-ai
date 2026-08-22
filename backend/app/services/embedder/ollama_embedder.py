import socket
import ollama

from app.core.config import settings
from app.services.embedder.base_embedder import BaseEmbedder

MAX_EMBED_CHARS = 6000
_fallback_model = None


def _is_service_listening(host: str, port: int, timeout: float = 1.5) -> bool:
    try:
        s = socket.create_connection((host, port), timeout=timeout)
        s.close()
        return True
    except Exception:
        return False


def _get_local_fallback_embedder():
    global _fallback_model
    if _fallback_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            print("[EMBEDDER FALLBACK] Loading local SentenceTransformer ('sentence-transformers/all-MiniLM-L6-v2')...")
            _fallback_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        except Exception as e:
            print(f"[EMBEDDER FALLBACK ERROR] Could not load SentenceTransformer: {e}")
            _fallback_model = False
    return _fallback_model


class OllamaEmbedder(BaseEmbedder):
    def __init__(self):
        self.host = settings.OLLAMA_BASE_URL.replace("host.docker.internal", "127.0.0.1")
        self.is_alive = _is_service_listening("127.0.0.1", 11434, timeout=1.0)
        if self.is_alive:
            print(f"[OLLAMA EMBEDDER] Connected to Ollama on 127.0.0.1:11434")
            self.client = ollama.Client(host=self.host)
        else:
            print("[OLLAMA EMBEDDER WARNING] Ollama service on 127.0.0.1:11434 is NOT running. Using SentenceTransformer fallback.")
            self.client = None

    def embed(self, text: str):
        if text is None:
            text = ""
        text = str(text)[:MAX_EMBED_CHARS]

        # Re-check if client is alive or try local fallback
        if self.client and self.is_alive:
            try:
                response = self.client.embeddings(
                    model=settings.DEFAULT_EMBED_MODEL,
                    prompt=text,
                )
                return response["embedding"]
            except Exception as e:
                print(f"[OLLAMA EMBEDDER ERROR] Ollama call failed ({e}). Switching to local fallback.")

        # Local SentenceTransformer Fallback
        local_model = _get_local_fallback_embedder()
        if local_model:
            vec = local_model.encode(text).tolist()
            # If Qdrant expects 768 vector size and MiniLM outputs 384, pad or scale to 768
            if len(vec) == 384:
                vec = vec + vec  # duplicate to match 768 dimensions
            return vec[:768]

        # Dummy fallback vector if all else fails
        return [0.0] * 768