from pydantic import BaseModel


class ResearchRequest(
    BaseModel
):

    query: str

    top_k: int = 10

    mode: str = "analysis"