from __future__ import annotations

from delbot_platform.ai.client.llm_client import LLMClient


class LLMGenerator:

    def __init__(
        self,
    ) -> None:

        self.client = LLMClient()

    def generate(
        self,
        messages: list[dict],
    ) -> str:

        return self.client.chat(
            messages=messages,
        )
