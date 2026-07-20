from fastapi import APIRouter
from pydantic import BaseModel


from delbot_platform.research.services.rag import (
    RAGService,
)



router = APIRouter(
    prefix="/research",
    tags=["research"],
)



rag = RAGService()



class ResearchRequest(BaseModel):

    question:str



@router.post("/chat")
def chat(
    request:ResearchRequest
):

    return rag.answer(
        request.question
    )
