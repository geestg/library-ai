from __future__ import annotations

import signal
import time
import sys

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from delbot_platform.ai.registry.registry import ModelRegistry


class ChatBody(BaseModel):
    model: str | None = None
    messages: list[dict]
    temperature: float = 0.7
    max_tokens: int | None = None


class BaseRuntime:


    def __init__(self, category):

        self.category = category

        self.registry = ModelRegistry()

        self.running = True

        self.app = FastAPI(
            title=f"DELBot Runtime {category}"
        )


        self.register_routes()



    def register_routes(self):

        @self.app.get("/health")
        def health():

            model = self.registry.default(
                self.category
            )

            return {
                "status": "healthy",
                "category": str(self.category),
                "model": model.name,
                "backend": model.backend.name,
            }


        @self.app.post("/v1/chat/completions")
        def chat(
            body: ChatBody
        ):

            message = body.messages[-1]["content"]


            return {

                "id": "chatcmpl-delbot",

                "object": "chat.completion",

                "model": body.model,

                "choices": [
                    {
                        "index":0,

                        "message":{
                            "role":"assistant",
                            "content":
                            f"DELBot runtime received: {message}"
                        },

                        "finish_reason":"stop"
                    }
                ]
            }



    def run(self):

        model = self.registry.default(
            self.category
        )


        print()
        print("="*60)
        print("DELBot AI Runtime")
        print("="*60)

        print(
            f"Category : {self.category}"
        )

        print(
            f"Model    : {model.name}"
        )

        print(
            f"Backend  : {model.backend}"
        )

        print(
            f"Path     : {model.path}"
        )

        print(
            f"Port     : {model.runtime.port}"
        )

        print("="*60)

        print()
        print("Runtime READY")


        uvicorn.run(
            self.app,
            host="0.0.0.0",
            port=model.runtime.port,
            log_level="info"
        )
