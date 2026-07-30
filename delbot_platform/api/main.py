from __future__ import annotations

from fastapi import FastAPI

#
# Legacy Workspace API
#
from delbot_platform.api.routes.workspace import (
    router as workspace_router,
)

from delbot_platform.api.routes.research import (
    router as legacy_research_router,
)

#
# Modern APIs
#
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
    title="DELBot API",
    version="1.0.0",
)

#
# Legacy routes
#
app.include_router(
    workspace_router,
)

app.include_router(
    legacy_research_router,
)

#
# Modern routes
#
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
        "service": "DELBot API",
        "status": "running",
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "delbot-api",
    }
