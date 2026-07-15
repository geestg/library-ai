from pathlib import Path


class PathManager:
    ROOT = Path(__file__).resolve().parents[2]

    BACKEND = ROOT / "backend"
    FRONTEND = ROOT / "frontend"

    DATA = ROOT / "data"
    CACHE = ROOT / "cache"
    MODELS = ROOT / "models"
    LOGS = ROOT / "logs"
    RUNTIME = ROOT / "runtime"
    DOCS = ROOT / "docs"

    CONFIG = ROOT / "delbot_platform" / "config"

    @classmethod
    def ensure_directories(cls):
        directories = [
            cls.DATA,
            cls.CACHE,
            cls.MODELS,
            cls.LOGS,
            cls.RUNTIME,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)