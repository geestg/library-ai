from fastapi import APIRouter

from app.models.research_models import (
    ResearchRequest
)

from app.services.research_service import (
    research_analysis
)

router = APIRouter()


# =====================================
# RESEARCH ANALYSIS
# =====================================

@router.post(
    "/research-analysis"
)
async def research_analysis_route(
    request: ResearchRequest
):

    return research_analysis(

        query=request.query,

        top_k=request.top_k,

        mode=request.mode
    )