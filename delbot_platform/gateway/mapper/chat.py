from __future__ import annotations

from delbot_platform.gateway.openai.chat import (
    ChatCompletionChoice,
    ChatCompletionMessage,
    ChatCompletionResponse,
)


class ChatCompletionMapper:

    @staticmethod
    def from_runtime(
        data: dict,
    ) -> ChatCompletionResponse:

        choice = data["choices"][0]

        return ChatCompletionResponse(
            model=data["model"],
            id=data.get(
                "id",
                "chatcmpl-delbot",
            ),
            object=data.get(
                "object",
                "chat.completion",
            ),
            created=data.get(
                "created",
                0,
            ),
            choices=[
                ChatCompletionChoice(
                    index=choice.get(
                        "index",
                        0,
                    ),
                    finish_reason=choice.get(
                        "finish_reason",
                        "stop",
                    ),
                    message=ChatCompletionMessage(
                        role=choice["message"][
                            "role"
                        ],
                        content=choice[
                            "message"
                        ][
                            "content"
                        ],
                    ),
                )
            ],
        )