from __future__ import annotations

from fastapi import FastAPI
import uvicorn

from delbot_platform.gateway.routers.health import (
    router as health_router,
)
from delbot_platform.gateway.routers.research import (
    router as research_router,
)

from delbot_platform.api.routers.retrieval import (
    router as retrieval_router,
)
from delbot_platform.api.routers.repository import (
    router as repository_router,
)
from delbot_platform.gateway.routers.chat import (
    router as chat_router,
)
from delbot_platform.gateway.routers.embedding import (
    router as embedding_router,
)
from delbot_platform.gateway.routers.models import (
    router as models_router,
)

from delbot_platform.api.routers.document import (
    router as document_router,
)

app = FastAPI(
    title="DELBot AI Gateway",
    version="2.0.0",
)

#
# Core
#

app.include_router(
    health_router,
)

app.include_router(
    research_router,
)

app.include_router(
    retrieval_router,
)

app.include_router(
    repository_router,
)

#
# AI APIs
#

app.include_router(
    chat_router,
)

app.include_router(
    embedding_router,
)

app.include_router(
    models_router,
)

app.include_router(
    document_router,
)


@app.get("/")
def root():

    return {
        "service": "DELBot AI Gateway",
        "version": "2.0.0",
        "status": "running",
    }


if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8100,
    )
