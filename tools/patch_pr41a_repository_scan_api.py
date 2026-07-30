from __future__ import annotations

from pathlib import Path
import ast
import py_compile

ROOT = Path(__file__).resolve().parents[1]

router = ROOT / "delbot_platform/api/routers/repository.py"

router.write_text(
'''from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/repository",
    tags=["Repository"],
)


class RepositoryScanRequest(BaseModel):
    path: str


class RepositoryScanResponse(BaseModel):
    repository: str
    exists: bool
    pdf_files: int
    metadata_files: int
    total_files: int


@router.post(
    "/scan",
    response_model=RepositoryScanResponse,
)
async def scan_repository(
    request: RepositoryScanRequest,
):

    root = Path(request.path)

    exists = root.exists()

    pdf_files = 0
    metadata_files = 0
    total_files = 0

    if exists:

        for f in root.rglob("*"):

            if not f.is_file():
                continue

            total_files += 1

            if f.suffix.lower() == ".pdf":
                pdf_files += 1

            if f.name.lower() == "metadata.json":
                metadata_files += 1

    return RepositoryScanResponse(
        repository=str(root),
        exists=exists,
        pdf_files=pdf_files,
        metadata_files=metadata_files,
        total_files=total_files,
    )
''',
encoding="utf-8",
)

ast.parse(router.read_text(encoding="utf-8"))
py_compile.compile(str(router), doraise=True)

print("PATCH OK")
