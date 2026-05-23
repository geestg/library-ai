from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    QDRANT_HOST = os.getenv("QDRANT_HOST")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT"))

    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

settings = Settings()