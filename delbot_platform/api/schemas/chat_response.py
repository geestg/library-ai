from pydantic import BaseModel
from typing import List

from delbot_platform.api.schemas.citation import Citation


class ChatResponse(BaseModel):

    answer: str

    citations: List[Citation] = []