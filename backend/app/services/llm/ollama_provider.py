import ollama

from app.core.config import settings

from app.services.llm.base_provider import (
    BaseLLMProvider,
)


class OllamaProvider(
    BaseLLMProvider
):

    def __init__(self):

        self.client = ollama.Client(
            host=settings.OLLAMA_BASE_URL
        )

    # =====================================
    # BUILD OPTIONS
    # =====================================

    def build_options(

        self,

        temperature: float,

        max_tokens: int | None,

    ):

        options = {

            "temperature":
                temperature,

        }

        # Ollama menggunakan num_predict
        if max_tokens is not None:

            options["num_predict"] = (
                max_tokens
            )

        return options

    # =====================================
    # GENERATE
    # =====================================

    def generate(

        self,

        model: str,

        prompt: str,

        temperature: float = 0,

        max_tokens: int | None = None,

    ):

        response = self.client.chat(

            model=model,

            messages=[

                {

                    "role":
                        "user",

                    "content":
                        prompt,

                }

            ],

            options=self.build_options(

                temperature=temperature,

                max_tokens=max_tokens,

            ),

        )

        return response[
            "message"
        ][
            "content"
        ]

    # =====================================
    # STREAM
    # =====================================

    def stream(

        self,

        model: str,

        prompt: str,

        temperature: float = 0,

        max_tokens: int | None = None,

    ):

        stream = self.client.chat(

            model=model,

            messages=[

                {

                    "role":
                        "user",

                    "content":
                        prompt,

                }

            ],

            options=self.build_options(

                temperature=temperature,

                max_tokens=max_tokens,

            ),

            stream=True,

        )

        for chunk in stream:

            yield chunk[
                "message"
            ][
                "content"
            ]