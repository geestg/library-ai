import unicodedata

from openai import OpenAI

from app.core.config import settings

from app.services.llm.base_provider import (
    BaseLLMProvider,
)


# =====================================
# SYSTEM INSTRUCTION
# =====================================

SYSTEM_INSTRUCTION = """
Anda adalah model bahasa yang digunakan oleh DELBot.

Ikuti instruksi berikut secara ketat:

1. Jawab menggunakan Bahasa Indonesia kecuali
   prompt secara eksplisit meminta bahasa lain.

2. Jangan mengganti bahasa jawaban ke bahasa
   Mandarin, Jepang, Korea, atau bahasa lain.

3. Pertahankan angka, nama file, istilah teknis,
   simbol, dan fakta dari evidence secara akurat.

4. Jangan menghasilkan encoding rusak,
   mojibake, atau karakter yang tidak relevan.

5. Jika prompt meminta format output tertentu,
   ikuti format tersebut secara tepat.

6. Untuk tugas klasifikasi dengan pilihan output
   terbatas, keluarkan hanya nilai yang diminta.
""".strip()


# =====================================
# NORMALIZE MODEL TEXT
# =====================================

def normalize_model_text(
    text,
):

    if text is None:

        return ""

    normalized = str(text)

    normalized = normalized.replace(
        "\r\n",
        "\n",
    )

    normalized = normalized.replace(
        "\r",
        "\n",
    )

    normalized = normalized.replace(
        "\x00",
        "",
    )

    normalized = unicodedata.normalize(
        "NFC",
        normalized,
    )

    return normalized


# =====================================
# OPENROUTER PROVIDER
# =====================================

class OpenRouterProvider(
    BaseLLMProvider
):

    def __init__(self):

        print(
            "[OPENROUTER] Initializing provider..."
        )

        print(
            f"[OPENROUTER] Base URL: "
            f"{settings.OPENROUTER_BASE_URL}"
        )

        self.client = OpenAI(

            api_key=settings.OPENROUTER_API_KEY,

            base_url=settings.OPENROUTER_BASE_URL,

        )

    # =====================================
    # BUILD MESSAGES
    # =====================================

    def build_messages(
        self,
        prompt: str,
    ):

        return [

            {
                "role": "system",

                "content": SYSTEM_INSTRUCTION,
            },

            {
                "role": "user",

                "content": prompt,
            },

        ]

    # =====================================
    # BUILD REQUEST
    # =====================================

    def build_request(

        self,

        model: str,

        prompt: str,

        temperature: float,

        max_tokens: int | None,

        stream: bool,

    ):

        request = {

            "model": model,

            "messages": self.build_messages(
                prompt
            ),

            "temperature": temperature,

            "stream": stream,

        }

        if max_tokens is not None:

            request["max_tokens"] = max_tokens

        return request

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

        response = (

            self.client
            .chat
            .completions
            .create(

                **self.build_request(

                    model=model,

                    prompt=prompt,

                    temperature=temperature,

                    max_tokens=max_tokens,

                    stream=False,

                )

            )

        )

        content = (

            response
            .choices[0]
            .message
            .content

        )

        return normalize_model_text(
            content
        )

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

        stream = (

            self.client
            .chat
            .completions
            .create(

                **self.build_request(

                    model=model,

                    prompt=prompt,

                    temperature=temperature,

                    max_tokens=max_tokens,

                    stream=True,

                )

            )

        )

        for chunk in stream:

            try:

                if not chunk.choices:

                    continue

                delta = chunk.choices[0].delta

                if delta is None:

                    continue

                content = delta.content

                if content is None:

                    continue

                if not isinstance(
                    content,
                    str,
                ):

                    content = str(
                        content
                    )

                if not content:

                    continue

                yield content

            except Exception as error:

                print(
                    "[OPENROUTER STREAM ERROR]",
                    error,
                )

                continue