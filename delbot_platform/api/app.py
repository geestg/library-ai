from __future__ import annotations

from fastapi import FastAPI

from delbot_platform.api.routers.document import (
    router as document_router,
)

from delbot_platform.api.routers.repository import (
    router as repository_router,
)

from delbot_platform.api.routers.research import (
    router as research_router,
)


app = FastAPI(
    title="DELBot Research API",
    version="1.0.0",
)


app.include_router(
    repository_router,
)

app.include_router(
    document_router,
)

app.include_router(
    research_router,
)


@app.get("/")
def root():

    return {
        "service": "DELBot Research API",
        "status": "running",
        "modules": [
            "repository",
            "documents",
            "research",
        ],
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
    }
