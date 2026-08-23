from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from delbot_platform.api.routes.chat import router as chat_router
from delbot_platform.api.routes.search import router as search_router
from delbot_platform.api.routes.research import router as research_router
from delbot_platform.api.routes.document import router as document_router
from delbot_platform.api.routes.session import router as session_router
from delbot_platform.api.routes.multimodal import router as multimodal_router
from delbot_platform.api.routes.debug import router as debug_router


app = FastAPI(
    title="DELBot Unified Research & Academic Operating System",
    description="Enterprise Multi-Agent AI Academic Knowledge Platform for IT Del",
    version="2.0.0",
)

# =========================================
# CORS Middleware
# =========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================
# Unified Route Registration (7 Master Modules)
# =========================================
app.include_router(chat_router, tags=["Chat"])
app.include_router(search_router, tags=["Search"])
app.include_router(research_router, tags=["Research"])
app.include_router(document_router, tags=["Document"])
app.include_router(session_router, tags=["Session"])
app.include_router(multimodal_router, tags=["Multimodal"])
app.include_router(debug_router, tags=["Debug"])


@app.get("/", tags=["System"])
def root():
    return {
        "service": "DELBot Unified Research & Academic Operating System",
        "status": "running",
        "version": "2.0.0",
        "modules": [
            "chat (Sync & Streaming)",
            "search (Hybrid BM25 + Qdrant)",
            "research (Academic Reasoning, Gap Detector, Title Gen)",
            "document (PDF Parser, Chunking, Document Chat)",
            "session (Workspace & History)",
            "multimodal (Speech STT/TTS & Vision OCR)",
        ],
    }


@app.get("/health", tags=["System"])
def health():
    return {
        "status": "healthy",
        "service": "delbot-unified-api",
    }
