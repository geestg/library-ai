from __future__ import annotations

from delbot_platform.ai.client.llm_client import (
    LLMClient,
)

from delbot_platform.knowledge.citation.source import (
    CitationSource,
)

from delbot_platform.knowledge.rag.llm.response import (
    LLMResponse,
)


class LLMGenerator:

    def __init__(
        self,
    ) -> None:

        self.client = LLMClient()

    async def generate(
        self,
        context: str,
        citations: list[CitationSource],
        instruction: str | None = None,
    ) -> LLMResponse:

        messages = [
            {
                "role": "system",
                "content": (
                    "You are DELBot, an academic research assistant.\n"
                    "Answer ONLY from the supplied context.\n"
                    "If the context is insufficient, explicitly say so.\n"
                    "Do not fabricate facts."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Context:\n"
                    f"{context}\n\n"
                    f"Question:\n"
                    f"{instruction or ''}"
                ),
            },
        ]

        answer = self.client.chat(
            messages=messages,
            temperature=0.2,
            max_tokens=1024,
        )

        return LLMResponse(
            answer=answer,
            citations=citations,
        )
