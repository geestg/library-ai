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

        **generation_kwargs,

    ):

        options = dict(
            generation_kwargs
        )

        # =================================
        # OPENAI -> OLLAMA COMPATIBILITY
        # =================================

        if "max_tokens" in options:

            options["num_predict"] = (
                options.pop("max_tokens")
            )

        return options

    # =====================================
    # GENERATE
    # =====================================

    def generate(

        self,

        model: str,

        prompt: str,

        **generation_kwargs,

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

                **generation_kwargs,

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

        **generation_kwargs,

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

                **generation_kwargs,

            ),

            stream=True,

        )

        for chunk in stream:

            yield chunk[
                "message"
            ][
                "content"
            ]
