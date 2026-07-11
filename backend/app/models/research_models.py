from typing import List
from typing import Optional

from pydantic import BaseModel


class ResearchRequest(
    BaseModel
):

    query: str

    top_k: int = 10

    mode: str = "analysis"

    active_document_ids: Optional[
        List[str]
    ] = []
