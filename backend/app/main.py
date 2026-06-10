import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles



from app.api.routes.routes_search import (
    router as search_router
)

from app.api.routes.routes_chat import (
    router as chat_router
)

from app.api.routes.routes_chat_stream import (
    router as stream_router
)

from app.api.routes.routes_upload import (
    router as upload_router
)

from app.api.routes.routes_debug import (
    router as debug_router
)

from app.api.routes.research import (
    router as research_router
)

from app.api.routes.title_generator import (
    router as title_generator_router
)

from app.api.routes.routes_document import (
    router as document_router
)

from app.api.routes.routes_vision import (
    router as vision_router
)

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

app.include_router(
    search_router
)

app.include_router(
    chat_router
)

app.include_router(
    stream_router
)

app.include_router(
    upload_router
)

app.include_router(
    debug_router
)

app.include_router(
    research_router
)

app.include_router(
    title_generator_router
)

# =========================================
# DOCUMENT CHAT
# =========================================

app.include_router(
    document_router
)

app.include_router(
    vision_router
)


# =========================================
# UPLOAD STATIC FILES (for image preview)
# =========================================

UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


# =========================================
# ROOT ENDPOINT
# =========================================

@app.get("/")
def root():

    return {

        "status": "running",

        "system": "DELBot",

        "description":
        "AI Academic Knowledge Operating System",

        "features": [

            "Semantic Search",

            "Academic RAG",

            "Hybrid Retrieval",

            "AI Orchestration",

            "PDF Upload",

            "Document Chunking",

            "Document Chat",

            "Session Documents",

            "Streaming Chat",

            "Reranking",

            "Research Assistant",

            "Research Intelligence",

            "Thesis Knowledge Base",

            "Research Gap Analysis",

            "Thesis Title Generator"
        ]
    }