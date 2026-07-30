from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from delbot_platform.repository.service import (
    RepositoryService,
)

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


class RepositoryItemResponse(BaseModel):
    id: str
    title: str
    status: str
    local_path: str | None = None


class RepositoryExplorerResponse(BaseModel):
    total: int
    pdf_available: int
    pdf_missing: int
    items: list[RepositoryItemResponse]


@router.post(
    "/scan",
    response_model=RepositoryScanResponse,
)
async def scan_repository(
    request: RepositoryScanRequest,
):

    from pathlib import Path

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


@router.get(
    "/explorer",
    response_model=RepositoryExplorerResponse,
)
async def repository_explorer():

    service = RepositoryService()

    result = service.scan()

    return RepositoryExplorerResponse(
        total=result.total,
        pdf_available=result.pdf_available,
        pdf_missing=result.pdf_missing,
        items=[
            RepositoryItemResponse(
                id=item.id,
                title=item.title,
                status=item.status.value,
                local_path=item.local_path,
            )
            for item in result.items
        ],
    )
