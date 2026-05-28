from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    # =====================================
    # QDRANT
    # =====================================

    QDRANT_HOST = os.getenv("QDRANT_HOST")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT"))

    # =====================================
    # OLLAMA
    # =====================================

    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

    # =====================================
    # OPENROUTER
    # =====================================

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    OPENROUTER_BASE_URL = os.getenv(
        "OPENROUTER_BASE_URL"
    )

    # =====================================
    # DEFAULT MODELS
    # =====================================

    DEFAULT_PROVIDER = os.getenv(
        "DEFAULT_PROVIDER",
        "openrouter"
    )

    DEFAULT_LLM = os.getenv(
        "DEFAULT_LLM",
        "qwen/qwen3-32b"
    )

    DEFAULT_FAST_MODEL = os.getenv(
        "DEFAULT_FAST_MODEL",
        "qwen/qwen3-8b"
    )

    DEFAULT_EMBED_MODEL = os.getenv(
        "DEFAULT_EMBED_MODEL",
        "nomic-embed-text"
    )


settings = Settings()