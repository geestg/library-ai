import ollama

from app.core.config import settings

from app.services.llm.base_provider import (
    BaseLLMProvider
)


class OllamaProvider(BaseLLMProvider):

    def __init__(self):

        self.client = ollama.Client(
            host=settings.OLLAMA_BASE_URL
        )

    # =====================================
    # GENERATE
    # =====================================

    def generate(
        self,
        model: str,
        prompt: str
    ):

        response = self.client.chat(

            model=model,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    # =====================================
    # STREAM
    # =====================================

    def stream(
        self,
        model: str,
        prompt: str
    ):

        stream = self.client.chat(

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

            yield chunk["message"]["content"]