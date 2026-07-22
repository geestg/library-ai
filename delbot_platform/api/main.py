from __future__ import annotations


from fastapi import FastAPI


from delbot_platform.api.routes.research import router as research_router
from delbot_platform.api.routes.workspace import router as workspace_router




app = FastAPI(

    title="DELBot API",

    version="0.1.0"

)



app.include_router(
    research_router
)


app.include_router(
    workspace_router
)




@app.get("/health")
def health():

    return {

        "status":"healthy",

        "service":"delbot-api"

    }
