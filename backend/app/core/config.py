from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    # =====================================
    # QDRANT VECTOR DATABASE
    # =====================================
    QDRANT_HOST = os.getenv("QDRANT_HOST", "host.docker.internal")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))

    # =====================================
    # OLLAMA EMBEDDING SERVICE (Vector Embedder)
    # =====================================
    OLLAMA_BASE_URL = os.getenv(
        "OLLAMA_BASE_URL",
        "http://host.docker.internal:11434"
    )

    # =====================================
    # LLM (Primary MoE LLM - GPU Server, Port 11435)
    # =====================================
    LLM_BASE_URL = os.getenv(
        "LLM_BASE_URL",
        os.getenv("VLLM_BASE_URL", "http://host.docker.internal:11435/v1")
    )
    LLM_API_KEY = os.getenv(
        "LLM_API_KEY",
        os.getenv("VLLM_API_KEY", "EMPTY")
    )
    LLM_MODEL = os.getenv(
        "LLM_MODEL",
        os.getenv("VLLM_MODEL", "/workspace/Qwen3-30B-MoE")
    )

    # Legacy alias for backward compatibility
    VLLM_BASE_URL = LLM_BASE_URL    
    VLLM_API_KEY = LLM_API_KEY
    VLLM_MODEL = LLM_MODEL

    # =====================================
    # SLM (Small Language Model - Fast GPU, Port 11436)
    # =====================================
    SLM_BASE_URL = os.getenv(
        "SLM_BASE_URL",
        "http://127.0.0.1:11436/v1"
    )
    SLM_API_KEY = os.getenv(
        "SLM_API_KEY",
        "EMPTY"
    )
    SLM_MODEL = os.getenv(
        "SLM_MODEL",
        "/workspace/Qwen3-4B"
    )

    # =====================================
    # DEFAULT PROVIDERS (GPU DUAL-MODEL GATEWAY + OLLAMA EMBEDDER)
    # =====================================
    DEFAULT_PROVIDER = os.getenv(
        "DEFAULT_PROVIDER",
        "llm"
    )
    DEFAULT_LLM = os.getenv(
        "DEFAULT_LLM",
        LLM_MODEL
    )
    DEFAULT_FAST_MODEL = os.getenv(
        "DEFAULT_FAST_MODEL",
        SLM_MODEL
    )
    DEFAULT_EMBED_MODEL = os.getenv(
        "DEFAULT_EMBED_MODEL",
        "nomic-embed-text"
    )


settings = Settings()