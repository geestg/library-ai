from delbot_platform.core.config import settings


def select_model(intent: str):
    """Select the active MoE LLM model for all intents."""
    return {
        "provider": "llm",
        "model": "/workspace/Qwen3-30B-MoE"
    }