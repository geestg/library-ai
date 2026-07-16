from __future__ import annotations

from delbot_platform.ai.registry.model_info import (
    ModelInfo,
)


class VLLMLauncher:

    @staticmethod
    def build_command(
        model: ModelInfo,
    ) -> list[str]:

        runtime = model.runtime

        config = model.backend_config

        return [

            "python",

            "-m",

            "vllm.entrypoints.openai.api_server",

            "--model",
            model.path,

            "--host",
            runtime.host,

            "--port",
            str(runtime.port),

            "--dtype",
            config.dtype,

            "--tensor-parallel-size",
            str(
                config.tensor_parallel_size,
            ),

            "--gpu-memory-utilization",
            str(
                config.gpu_memory_utilization,
            ),

            "--max-model-len",
            str(
                config.max_context,
            ),

        ]