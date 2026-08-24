from __future__ import annotations

from fastapi import FastAPI

from delbot_platform.api.routers.chat import (
    router as chat_router,
)

from delbot_platform.api.routers.document import (
    router as document_router,
)

from delbot_platform.api.routers.repository import (
    router as repository_router,
)

from delbot_platform.api.routers.research import (
    router as research_router,
)

from delbot_platform.api.routers.retrieval import (
    router as retrieval_router,
)
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="DELBot Research API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    repository_router,
)

app.include_router(
    chat_router,
)

app.include_router(
    document_router,
)

app.include_router(
    research_router,
)

app.include_router(
    retrieval_router,
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
