from __future__ import annotations

import requests


class LLMClient:

    def __init__(
        self,
        url="http://127.0.0.1:11435/v1/chat/completions",
        model="/workspace/Qwen3-30B-MoE"
    ):
        self.url = url
        self.model = model

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
            return "⚠️ [Koneksi GPU]: Tidak dapat terhubung ke model di port 11435. Pastikan SSH Tunnel aktif (`ssh -L 11435:localhost:11435 ...`)."
        except Exception as e:
            return f"⚠️ [LLM Request Error]: {e}"
