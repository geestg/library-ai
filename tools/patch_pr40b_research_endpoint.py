from __future__ import annotations

from pathlib import Path
import ast
import py_compile

ROOT = Path(__file__).resolve().parents[1]

router_file = ROOT / "delbot_platform/gateway/routers/research.py"

router_code = '''from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from delbot_platform.application.research.answer import (
    ResearchAnswerApplication,
)

router = APIRouter(
    prefix="/research",
    tags=["Research"],
)


class ResearchRequest(BaseModel):
    question: str


class ResearchResponse(BaseModel):
    answer: str
    citations: list
    context_length: int
    documents: int
    retrieved: int


application = ResearchAnswerApplication()


@router.post(
    "/answer",
    response_model=ResearchResponse,
)
async def research_answer(
    request: ResearchRequest,
):

    response = await application.execute(
        question=request.question,
    )

    return ResearchResponse(
        answer=response.answer,
        citations=response.citations,
        context_length=len(response.rag.context),
        documents=len(response.rag.documents),
        retrieved=len(response.rag.citations),
    )
'''

router_file.write_text(router_code)

print("PATCHED")
print(router_file)

print()
print("=" * 72)
print("AST")
print("=" * 72)

ast.parse(router_code)

print("PASS")

print()
print("=" * 72)
print("PY_COMPILE")
print("=" * 72)

py_compile.compile(
    str(router_file),
    doraise=True,
)

print("PASS")
