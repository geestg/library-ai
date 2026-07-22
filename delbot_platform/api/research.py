from fastapi import APIRouter
from pydantic import BaseModel


from delbot_platform.research.research_engine import ResearchEngine



router = APIRouter(
    prefix="/research",
    tags=["Research"]
)



engine = ResearchEngine()



class ResearchRequest(BaseModel):

    query:str



@router.post("/ask")
def ask_research(
    request:ResearchRequest
):


    result = engine.ask(
        request.query
    )


    return result
