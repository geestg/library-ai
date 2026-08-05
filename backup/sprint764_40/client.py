from __future__ import annotations

import httpx


class LLMClient:


    def __init__(self):

        self.url = (
            "http://127.0.0.1:8101/v1/chat/completions"
        )


    def chat(
        self,
        prompt:str,
    ):


        response = httpx.post(
            self.url,
            json={
                "model":"qwen3-32b",
                "messages":[
                    {
                        "role":"system",
                        "content":
                        "You are DELBot research assistant. Answer based on context."
                    },
                    {
                        "role":"user",
                        "content":prompt
                    }
                ],
                "temperature":0.2,
            },
            timeout=120,
        )


        response.raise_for_status()


        data=response.json()


        return data["choices"][0]["message"]["content"]
