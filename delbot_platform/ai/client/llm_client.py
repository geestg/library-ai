from __future__ import annotations

import requests
from delbot_platform.core.config import settings


class LLMClient:

    def __init__(
        self,
        url: str = None,
        model: str = None
    ):
        base_url = settings.LLM_BASE_URL.rstrip('/')
        if not base_url.endswith('/chat/completions'):
            base_url = f"{base_url}/chat/completions"
        self.url = url or base_url
        self.model = model or settings.LLM_MODEL

    def chat(
        self,
        messages: list[dict],
        temperature: float = 0.2,
        max_tokens: int = 800
    ) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            response = requests.post(
                self.url,
                json=payload,
                timeout=30
            )

            if response.status_code != 200:
                return f"⚠️ [LLM Error]: Server mengembalikan status {response.status_code} - {response.text}"

            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.exceptions.ConnectionError:
            return f"⚠️ [Koneksi GPU]: Tidak dapat terhubung ke model di {self.url}. Pastikan SSH Tunnel aktif."
        except Exception as e:
            return f"⚠️ [LLM Request Error]: {e}"

