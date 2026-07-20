from __future__ import annotations

from fastapi import APIRouter


router = APIRouter(
    prefix="/repository",
    tags=["repository"],
)


@router.get("/health")
def repository_health():

    return {
        "service": "repository",
        "status": "ok",
    }


__all__ = [
    "router",
]
