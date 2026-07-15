from pydantic import BaseModel


class ChatResponse(BaseModel):
    model: str
    response: str
    finish_reason: str = "stop"