from fastapi import FastAPI

from app.api.routes_search import router as search_router
from app.api.routes_chat import router as chat_router

app = FastAPI(title="Library AI")

app.include_router(search_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "Library AI Running"
    }