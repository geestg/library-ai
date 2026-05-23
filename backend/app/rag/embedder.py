import ollama
from app.core.config import settings

client = ollama.Client(
    host=settings.OLLAMA_BASE_URL
)

def get_embedding(text: str):

    response = client.embeddings(
        model="nomic-embed-text",
        prompt=text
    )

    return response["embedding"]