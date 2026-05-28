from openai import OpenAI

from app.core.config import settings

from app.services.llm.base_provider import (
    BaseLLMProvider
)


class OpenRouterProvider(BaseLLMProvider):

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
        prompt: str
    ):

        response = self.client.chat.completions.create(

            model=model,

            messages=[
                {
                    "role": "user",
                    "content": prompt
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
        prompt: str
    ):

        stream = self.client.chat.completions.create(

            model=model,

            messages=[
                {
                    "role": "user",
                    "content": prompt
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