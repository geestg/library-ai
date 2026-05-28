from app.orchestration.intent_classifier import (
    classify_intent
)

from app.orchestration.model_selector import (
    select_model
)


def route_query(query: str):

    # =====================================
    # INTENT CLASSIFICATION
    # =====================================

    intent = classify_intent(query)

    # =====================================
    # MODEL SELECTION
    # =====================================

    selected = select_model(intent)

    # =====================================
    # RESPONSE
    # =====================================

    return {

        "intent": intent,

        "provider": selected["provider"],

        "model": selected["model"]
    }