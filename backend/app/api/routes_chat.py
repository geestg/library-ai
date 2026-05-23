from fastapi import APIRouter
from pydantic import BaseModel
import ollama

from app.rag.embedder import get_embedding
from app.rag.qdrant_client import client
from app.core.config import settings

router = APIRouter()

ollama_client = ollama.Client(
    host=settings.OLLAMA_BASE_URL
)

class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(req: ChatRequest):

    embedding = get_embedding(req.message)

    results = client.query_points(
        collection_name="skripsi_collection",
        query=embedding,
        limit=3
    )

    context = "\n\n".join([
        f"""
        Judul: {r.payload.get('judul', '')}

        Abstrak:
        {r.payload.get('abstrak', '')}
        """
        for r in results.points
    ])

    prompt = f"""
    Kamu adalah AI akademik.

    Jawab pertanyaan berdasarkan konteks berikut.

    KONTEKS:
    {context}

    PERTANYAAN:
    {req.message}
    """

    response = ollama_client.chat(
        model="qwen2.5:7b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "response": response["message"]["content"]
    }