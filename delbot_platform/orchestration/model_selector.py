from delbot_platform.core.config import settings


def select_model(intent: str):
    """Choose fast SLM for lightweight conversational intents and LLM for deep research intents."""
    # Intent Cepat (Clarification / FAQ / Short Chat) -> SLM GPU (Port 11436)
    if intent in ["intent_classification", "clarification", "faq"]:
        return {
            "provider": "slm",
            "model": settings.SLM_MODEL
        }

    # Intent Riset Berat (Thesis Idea, Literature Review, Admin SQL, Analysis) -> MoE LLM GPU (Port 11435)
    return {
        "provider": settings.DEFAULT_PROVIDER,
        "model": settings.DEFAULT_LLM
    }