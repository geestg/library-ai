from pydantic import BaseModel


class ChatRequest(BaseModel):
    model: str
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 1024