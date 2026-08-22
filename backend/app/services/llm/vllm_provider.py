import socket
from openai import OpenAI

from app.core.config import settings
from app.services.llm.base_provider import BaseLLMProvider


class VLLMProvider(BaseLLMProvider):
    DEFAULT_MAX_TOKENS = 4096

    def __init__(self, name: str = "VLLM", base_url: str = None, api_key: str = None):
        self.name = name
        actual_base_url = base_url or settings.VLLM_BASE_URL
        actual_api_key = api_key or settings.VLLM_API_KEY or "EMPTY"

        print(f"[{name}] Initializing provider -> {actual_base_url}")

        self.client = OpenAI(
            api_key=actual_api_key,
            base_url=actual_base_url
        )

    def generate(
        self,
        model: str,
        prompt: str,
        image_ref: str = None,
        max_tokens: int = None
    ):
        if image_ref:
            content = [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_ref}}
            ]
        else:
            content = prompt

        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": content}],
            max_tokens=max_tokens or self.DEFAULT_MAX_TOKENS,
            timeout=600.0
        )
        return response.choices[0].message.content

    def stream(
        self,
        model: str,
        prompt: str,
        image_ref: str = None,
        max_tokens: int = None
    ):
        if image_ref:
            content = [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_ref}}
            ]
        else:
            content = prompt

        stream = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": content}],
            stream=True,
            max_tokens=max_tokens or self.DEFAULT_MAX_TOKENS,
            timeout=600.0
        )
        for chunk in stream:
            if chunk.choices:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    yield delta.content
