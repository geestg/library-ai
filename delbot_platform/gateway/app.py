from fastapi import FastAPI

from delbot_platform.gateway.routers.chat import (
    router as chat_router,
)
from delbot_platform.gateway.routers.embedding import (
    router as embedding_router,
)
from delbot_platform.gateway.routers.health import (
    router as health_router,
)

from delbot_platform.gateway.routers.v1.chat import (
    router as chat_v1_router,
)
from delbot_platform.gateway.routers.v1.embedding import (
    router as embedding_v1_router,
)


app = FastAPI(
    title="DELBot AI Gateway",
    description="Unified AI Gateway for DELBot Platform",
    version="2.0.0",
)


#
# Legacy API
#

app.include_router(
    health_router,
    tags=["Health"],
)

app.include_router(
    chat_router,
    tags=["Chat"],
)

app.include_router(
    embedding_router,
    tags=["Embedding"],
)


#
# Stable V1 API
#

app.include_router(
    chat_v1_router,
)

app.include_router(
    embedding_v1_router,
)


@app.get(
    "/",
    tags=["Gateway"],
)
def root():

    return {

        "service": "DELBot AI Gateway",

        "project": "DELBot",

        "version": "2.0.0",

        "api": "v1",

        "status": "running",

    }