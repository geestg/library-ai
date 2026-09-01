from __future__ import annotations

import socket
import urllib.parse
from openai import OpenAI

from delbot_platform.core.config import settings
from delbot_platform.ai.llm.base_provider import BaseLLMProvider


class VLLMProvider(BaseLLMProvider):
    DEFAULT_MAX_TOKENS = 4096

    def __init__(self, name: str = "VLLM", base_url: str = None, api_key: str = None):
        self.name = name
        actual_base_url = base_url or settings.VLLM_BASE_URL
        actual_api_key = api_key or settings.VLLM_API_KEY or "EMPTY"

        # If running directly on Windows host (not in Docker), use 127.0.0.1
        # If running inside Docker container, keep host.docker.internal to reach Windows host tunnel
        import os
        is_in_docker = os.path.exists("/.dockerenv") or os.environ.get("DOCKER_CONTAINER") == "1"
        if not is_in_docker and "host.docker.internal" in actual_base_url:
            actual_base_url = actual_base_url.replace("host.docker.internal", "127.0.0.1")

        print(f"[{name}] Initializing provider -> {actual_base_url}")

        self.client = OpenAI(
            api_key=actual_api_key,
            base_url=actual_base_url,
            timeout=120.0,
        )

    def _trim_prompt_to_budget(self, prompt: str, max_chars: int = 32000) -> str:
        if not prompt or len(prompt) <= max_chars:
            return prompt
        half = max_chars // 2
        head = prompt[:half]
        tail = prompt[-half:]
        return head + "\n\n... [Konteks Bukti Riset Dipadatkan Otomatis Agar Sesuai Jendela Konteks GPU] ...\n\n" + tail

    def generate(
        self,
        model: str,
        prompt: str,
        image_ref: str = None,
        max_tokens: int = None
    ):
        prompt = self._trim_prompt_to_budget(prompt)
        if image_ref:
            content = [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_ref}}
            ]
        else:
            content = prompt

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": content}],
                max_tokens=max_tokens or self.DEFAULT_MAX_TOKENS,
                timeout=120.0
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[{self.name} ERROR] Failed to connect to model server: {e}")
            # Graceful fallback: return a helpful message if SSH Tunnel is not active
            return f"⚠️ [Koneksi Model GPU]: Sedang tidak dapat menghubungi GPU Model Server di {self.base_url}. (Error: {e})"

    def stream(
        self,
        model: str,
        prompt: str,
        image_ref: str = None,
        max_tokens: int = None
    ):
        prompt = self._trim_prompt_to_budget(prompt)
        if image_ref:
            content = [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_ref}}
            ]
        else:
            content = prompt

        try:
            stream = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": content}],
                stream=True,
                max_tokens=max_tokens or self.DEFAULT_MAX_TOKENS,
                timeout=20.0
            )
            for chunk in stream:
                if chunk.choices:
                    delta = chunk.choices[0].delta
                    if delta and delta.content:
                        yield delta.content
        except Exception as e:
            print(f"[{self.name} STREAM ERROR] Failed to connect: {e}")
            yield f"⚠️ [Koneksi Model GPU]: Tidak dapat terhubung ke GPU Model Server di {self.base_url}. (Detail error: {e})"
