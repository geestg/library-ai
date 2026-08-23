from __future__ import annotations

import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from delbot_platform.api.routes.document import (
    router as document_router,
)

from delbot_platform.api.routes.research import (
    router as research_router,
)

from delbot_platform.api.routes.workspace import (
    router as workspace_router,
)


app = FastAPI(
    title="DELBot Unified Research & Academic Operating System",
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
# Platform Core Routers
# =========================================
app.include_router(
    document_router,
)

app.include_router(
    research_router,
)

app.include_router(
    workspace_router,
)

# =========================================
# DELBot Feature Routers (Hybrid Search, Chat, Voice, Vision, etc.)
# =========================================
try:
    from delbot_platform.api.routes.routes_search import router as search_router
    app.include_router(search_router)
except Exception as e:
    print(f"[WARN] Failed to load search_router: {e}")

try:
    from delbot_platform.api.routes.routes_chat import router as chat_router
    app.include_router(chat_router)
except Exception as e:
    print(f"[WARN] Failed to load chat_router: {e}")

try:
    from delbot_platform.api.routes.routes_chat_stream import router as stream_router
    app.include_router(stream_router)
except Exception as e:
    print(f"[WARN] Failed to load stream_router: {e}")

try:
    from delbot_platform.api.routes.routes_session import router as session_router
    app.include_router(session_router)
except Exception as e:
    print(f"[WARN] Failed to load session_router: {e}")

try:
    from delbot_platform.api.routes.routes_upload import router as upload_router
    app.include_router(upload_router)
except Exception as e:
    print(f"[WARN] Failed to load upload_router: {e}")

try:
    from delbot_platform.api.routes.routes_debug import router as debug_router
    app.include_router(debug_router)
except Exception as e:
    print(f"[WARN] Failed to load debug_router: {e}")

try:
    from delbot_platform.api.routes.research import router as backend_research_router
    app.include_router(backend_research_router)
except Exception as e:
    print(f"[WARN] Failed to load backend_research_router: {e}")

try:
    from delbot_platform.api.routes.title_generator import router as title_generator_router
    app.include_router(title_generator_router)
except Exception as e:
    print(f"[WARN] Failed to load title_generator_router: {e}")

try:
    from delbot_platform.api.routes.routes_document import router as backend_document_router
    app.include_router(backend_document_router)
except Exception as e:
    print(f"[WARN] Failed to load backend_document_router: {e}")

try:
    from delbot_platform.api.routes.routes_vision import router as vision_router
    app.include_router(vision_router)
except Exception as e:
    print(f"[WARN] Failed to load vision_router: {e}")

try:
    from delbot_platform.api.routes.routes_speech import router as speech_router
    app.include_router(speech_router)
except Exception as e:
    print(f"[WARN] Failed to load speech_router: {e}")


@app.get("/")
def root():

    return {
        "service": "DELBot Unified Research & Academic Operating System",
        "status": "running",
        "version": "2.0.0",
        "features": [
            "Platform Core (Document, Research, Workspace)",
            "Semantic & Hybrid BM25 Search",
            "Academic RAG & Streaming Chat",
            "Speech STT & TTS",
            "Multimodal Vision & OCR",
            "Thesis Gap Analysis & Title Generator",
        ],
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "delbot-unified-api",
    }
