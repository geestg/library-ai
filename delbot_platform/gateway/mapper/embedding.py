from __future__ import annotations

from delbot_platform.gateway.openai.embedding import (
    EmbeddingData,
    EmbeddingResponse,
)


class EmbeddingMapper:

    @staticmethod
    def from_runtime(
        data: dict,
    ) -> EmbeddingResponse:

        embeddings = []

        for item in data["data"]:

            embeddings.append(
                EmbeddingData(
                    index=item["index"],
                    embedding=item[
                        "embedding"
                    ],
                    object=item.get(
                        "object",
                        "embedding",
                    ),
                )
            )

        return EmbeddingResponse(
            model=data["model"],
            id=data.get(
                "id",
                "emb-delbot",
            ),
            object=data.get(
                "object",
                "list",
            ),
            created=data.get(
                "created",
                0,
            ),
            data=embeddings,
        )