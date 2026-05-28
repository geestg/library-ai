from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_search import router as search_router
from app.api.routes_chat import router as chat_router
from app.api.routes_chat_stream import router as stream_router
from app.api.routes_upload import router as upload_router
from app.api.routes_debug import router as debug_router

app = FastAPI(
    title="DELBot - AI Academic Knowledge Operating System"
)

# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================
# ROUTERS
# =========================================

app.include_router(search_router)

app.include_router(chat_router)

app.include_router(stream_router)

app.include_router(upload_router)

app.include_router(debug_router)

# =========================================
# ROOT ENDPOINT
# =========================================

@app.get("/")
def root():

    return {
        "status": "running",

        "system": "DELBot",

        "description": "AI Academic Knowledge Operating System",

        "features": [
            "Semantic Search",
            "Academic RAG",
            "Hybrid Retrieval",
            "AI Orchestration",
            "PDF Upload",
            "Document Chunking",
            "Streaming Chat",
            "Reranking",
            "Research Assistant"
        ]
    }