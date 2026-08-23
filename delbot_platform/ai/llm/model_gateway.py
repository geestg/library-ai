from delbot_platform.core.config import settings

from delbot_platform.core.error_handler import (
    handle_llm_error
)

from delbot_platform.ai.llm.vllm_provider import (
    VLLMProvider
)

class ModelGateway:

    def __init__(self):

        # LLM: Besar, berat, untuk riset akademik dan RAG
        # SLM: Cepat, ringan, untuk FAQ / klarifikasi / klasifikasi sederhana
        self.providers = {
            "llm": VLLMProvider(
                name="LLM",
                base_url=settings.LLM_BASE_URL,
                api_key=settings.LLM_API_KEY
            ),
            "slm": VLLMProvider(
                name="SLM",
                base_url=settings.SLM_BASE_URL,
                api_key=settings.SLM_API_KEY
            )
        }
        # Backward compatibility for legacy provider name
        self.providers["vllm"] = self.providers["llm"]

    # =====================================
    # GENERATE RESPONSE
    # =====================================
    def generate_response(
        self,
        prompt: str,
        model: str = None,
        provider: str = None,
        image_ref: str = None,
        max_tokens: int = None
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
            print("="*60)
            print("PROVIDER :", provider)
            print("MODEL    :", model)
            print("="*60)
            return selected_provider.generate(
                model=model,
                prompt=prompt,
                image_ref=image_ref,
                max_tokens=max_tokens
            )

        except Exception as e:
            print(f"[MODEL GATEWAY ERROR] Provider '{provider}' failed with error: {e}")
            if provider != "vllm" and "vllm" in self.providers:
                print(f"[MODEL GATEWAY] Falling back to primary 'vllm' provider...")
                try:
                    return self.providers["vllm"].generate(
                        model=settings.DEFAULT_LLM,
                        prompt=prompt,
                        image_ref=image_ref,
                        max_tokens=max_tokens
                    )
                except Exception as fallback_err:
                    print(f"[MODEL GATEWAY FALLBACK ERROR] Primary vllm also failed: {fallback_err}")
            handle_llm_error(e)

    # =====================================
    # STREAM RESPONSE
    # =====================================
    def stream_response(
        self,
        prompt: str,
        model: str = None,
        provider: str = None,
        image_ref: str = None,
        max_tokens: int = None
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
                prompt=prompt,
                image_ref=image_ref,
                max_tokens=max_tokens
            )

        except Exception as e:
            print(f"[MODEL GATEWAY ERROR] Provider '{provider}' stream failed with error: {e}")
            handle_llm_error(e)

gateway = ModelGateway()
