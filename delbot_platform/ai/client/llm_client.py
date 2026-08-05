from __future__ import annotations

import requests

from delbot_platform.core.config_manager import ConfigManager


class LLMClient:

    def __init__(
        self,
        url: str | None = None,
        model: str | None = None,
    ) -> None:

        cfg = ConfigManager()

        if url is None:
            service = cfg.service("chat")
            host = service.get("host", "127.0.0.1")
            port = service["port"]
            url = f"http://{host}:{port}/v1/chat/completions"

        if model is None:
            chat_cfg = cfg.model("chat")
            model_name = chat_cfg["default"]
            model = model_name

        self.url = url
        self.model = model

    def chat(
        self,
        messages: list[dict],
        temperature: float = 0.2,
        max_tokens: int = 800,
    ) -> str:

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        print("=" * 50)
        print("[LLM REQUEST]")
        print(payload)
        print("=" * 50)

        response = requests.post(
            self.url,
            json=payload,
            timeout=900,
        )

        if response.status_code != 200:
            print(response.text)

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]
