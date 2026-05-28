from pydantic import BaseModel
from typing import Optional


class Citation(BaseModel):

    source_id: int

    source_file: str

    page: Optional[int] = None

    chunk_index: Optional[int] = None

    score: Optional[float] = None

    content: Optional[str] = None