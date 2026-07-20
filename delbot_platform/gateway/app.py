from fastapi import FastAPI

import uvicorn


from delbot_platform.gateway.routers.health import (
    router as health_router,
)


from delbot_platform.gateway.routers.research import (
    router as research_router,
)



app = FastAPI(
    title="DELBot AI Gateway",
    version="2.0.0",
)



app.include_router(
    health_router
)


app.include_router(
    research_router
)



@app.get("/")
def root():

    return {
        "service":"DELBot AI Gateway",
        "version":"2.0.0",
        "status":"running"
    }



if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8100,
    )
