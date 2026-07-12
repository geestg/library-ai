import ollama

from app.core.config import settings

from app.services.embedder.base_embedder import (
    BaseEmbedder
)

# =====================================
# EMBEDDING LIMIT
# =====================================

MAX_EMBED_CHARS = 6000


class OllamaEmbedder(
    BaseEmbedder
):

    def __init__(self):

        self.client = ollama.Client(
            host=settings.OLLAMA_BASE_URL
        )

    # =================================
    # EMBED
    # =================================

    def embed(
        self,
        text: str
    ):

        if text is None:

            text = ""

        text = str(text)

        original_length = len(text)

        if original_length > MAX_EMBED_CHARS:

            print(
                f"[EMBED] truncating "
                f"{original_length} chars "
                f"to {MAX_EMBED_CHARS}"
            )

            text = text[
                :MAX_EMBED_CHARS
            ]

        try:

            response = (
                self.client.embeddings(

                    model=
                    settings.DEFAULT_EMBED_MODEL,

                    prompt=text
                )
            )

            return response[
                "embedding"
            ]

        except Exception as e:

            print(
                "\n===================================="
            )

            print(
                "OLLAMA EMBEDDING ERROR"
            )

            print(
                "===================================="
            )

            print(
                f"MODEL : "
                f"{settings.DEFAULT_EMBED_MODEL}"
            )

            print(
                f"LENGTH: "
                f"{len(text)}"
            )

            print(
                f"ERROR : {e}"
            )

            print(
                "====================================\n"
            )

            raise

