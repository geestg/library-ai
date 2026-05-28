from pydantic import BaseModel
from typing import List

from app.schemas.citation import Citation


class ChatResponse(BaseModel):

    answer: str

    citations: List[Citation] = []