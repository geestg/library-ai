from fastapi import FastAPI

from delbot_platform.gateway.routers.chat import (
    router as chat_router,
)
from delbot_platform.gateway.routers.health import (
    router as health_router,
)


app = FastAPI(
    title="DELBot AI Gateway",
    description="Unified AI Gateway for DELBot Platform",
    version="2.0.0",
)


app.include_router(
    health_router,
    tags=["Health"],
)

app.include_router(
    chat_router,
    tags=["Chat"],
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
        "status": "running",
    }