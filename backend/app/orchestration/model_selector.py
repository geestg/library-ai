def select_model(intent: str):

    # =====================================
    # FAQ / SIMPLE QUERY
    # =====================================

    if intent == "faq":

        return {

            "provider": "openrouter",

            "model": "qwen/qwen-2.5-7b-instruct"
        }

    # =====================================
    # MULTIMODAL
    # =====================================

    if intent == "multimodal":

        return {

            "provider": "openrouter",

            "model": "qwen/qwen2-vl-72b-instruct"
        }

    # =====================================
    # DEFAULT REASONING
    # =====================================

    return {

        "provider": "openrouter",

        "model": "qwen/qwen-2.5-7b-instruct"
    }