from __future__ import annotations

from delbot_platform.ai.registry.model_info import (
    ModelInfo,
)


class InfinityLauncher:

    @staticmethod
    def build_command(
        model: ModelInfo,
    ) -> list[str]:

        runtime = model.runtime

        return [

            "infinity_emb",

            "--model-id",
            model.path,

            "--port",
            str(
                runtime.port,
            ),

        ]