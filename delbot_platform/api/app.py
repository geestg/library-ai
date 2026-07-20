from fastapi import FastAPI


from delbot_platform.api.routes.document import (
    router as document_router,
)

from delbot_platform.api.routes.research import (
    router as research_router,
)



app = FastAPI(
    title="DELBot Research API",
    version="1.0.0",
)



app.include_router(
    document_router
)


app.include_router(
    research_router
)



@app.get("/")
def root():

    return {

        "service":"DELBot Research API",

        "status":"running",

        "modules":[
            "document",
            "research",
        ]

    }
