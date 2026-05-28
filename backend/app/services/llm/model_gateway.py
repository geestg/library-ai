from app.core.config import settings

from app.services.llm.openrouter_provider import (
    OpenRouterProvider
)

from app.services.llm.ollama_provider import (
    OllamaProvider
)

from app.utils.error_handler import (
    handle_llm_error
)


class ModelGateway:

    def __init__(self):

        self.providers = {

            "openrouter": OpenRouterProvider(),

            "ollama": OllamaProvider()
        }

    # =====================================
    # GENERATE RESPONSE
    # =====================================

    def generate_response(
        self,
        prompt: str,
        model: str = None,
        provider: str = None
    ):

        provider = (
            provider
            or settings.DEFAULT_PROVIDER
        )

        model = (
            model
            or settings.DEFAULT_LLM
        )

        if provider not in self.providers:

            raise ValueError(
                f"Provider '{provider}' not found"
            )

        selected_provider = self.providers[
            provider
        ]

        try:

            return selected_provider.generate(

                model=model,

                prompt=prompt
            )

        except Exception as e:

            handle_llm_error(e)

    # =====================================
    # STREAM RESPONSE
    # =====================================

    def stream_response(
        self,
        prompt: str,
        model: str = None,
        provider: str = None
    ):

        provider = (
            provider
            or settings.DEFAULT_PROVIDER
        )

        model = (
            model
            or settings.DEFAULT_LLM
        )

        if provider not in self.providers:

            raise ValueError(
                f"Provider '{provider}' not found"
            )

        selected_provider = self.providers[
            provider
        ]

        try:

            return selected_provider.stream(

                model=model,

                prompt=prompt
            )

        except Exception as e:

            handle_llm_error(e)


gateway = ModelGateway()