from openai import OpenAI

from app.core.config import settings

from app.services.llm.base_provider import (
    BaseLLMProvider
)


class OpenRouterProvider(BaseLLMProvider):

    DEFAULT_MAX_TOKENS = 2048

    def __init__(self):

        print("[OPENROUTER] Initializing provider...")

        print(
            f"[OPENROUTER] Base URL: "
            f"{settings.OPENROUTER_BASE_URL}"
        )

        self.client = OpenAI(

            api_key=settings.OPENROUTER_API_KEY,

            base_url=settings.OPENROUTER_BASE_URL
        )

    # =====================================
    # GENERATE
    # =====================================

    def generate(
        self,
        model: str,
        prompt: str,
        image_ref: str = None,
        max_tokens: int = None
    ):

        if image_ref:
            content = [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_ref
                    }
                }
            ]
        else:
            content = prompt

        response = self.client.chat.completions.create(

            model=model,

            max_tokens=max_tokens or self.DEFAULT_MAX_TOKENS,

            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ]
        )

        return response.choices[0].message.content

    # =====================================
    # STREAM
    # =====================================

    def stream(
        self,
        model: str,
        prompt: str,
        image_ref: str = None,
        max_tokens: int = None
    ):

        if image_ref:
            content = [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_ref
                    }
                }
            ]
        else:
            content = prompt

        stream = self.client.chat.completions.create(

            model=model,

            max_tokens=max_tokens or self.DEFAULT_MAX_TOKENS,

            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ],

            stream=True
        )

        for chunk in stream:

            try:

                if not chunk.choices:

                    continue

                delta = chunk.choices[0].delta

                if not delta:

                    continue

                content = delta.content

                if content:

                    yield content

            except Exception as e:

                print(
                    f"[OPENROUTER STREAM ERROR] {e}"
                )

                continue