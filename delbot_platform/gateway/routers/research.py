from fastapi import APIRouter


from pydantic import BaseModel


from delbot_platform.research.services.rag import (
    RAGService,
)



router = APIRouter(
    prefix="/v1/research",
    tags=["Research"],
)



rag = RAGService()



class ResearchRequest(BaseModel):

    query:str



@router.post("/chat")
def research_chat(
    body:ResearchRequest
):


    result = rag.answer(
        body.query
    )


    return result
