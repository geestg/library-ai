import ollama

from app.core.config import settings

from app.services.embedder.base_embedder import (
    BaseEmbedder
)


class OllamaEmbedder(BaseEmbedder):

    def __init__(self):

        self.client = ollama.Client(
            host=settings.OLLAMA_BASE_URL
        )

    def embed(self, text: str):

        response = self.client.embeddings(

            model=settings.DEFAULT_EMBED_MODEL,

            prompt=text
        )

        return response["embedding"]