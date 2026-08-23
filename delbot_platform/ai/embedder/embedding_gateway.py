from delbot_platform.ai.embedder.ollama_embedder import (
    OllamaEmbedder
)


class EmbeddingGateway:

    def __init__(self):

        self.provider = OllamaEmbedder()

    def embed(self, text: str):

        return self.provider.embed(text)


embedding_gateway = EmbeddingGateway()