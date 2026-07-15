from delbot_platform.ai.registry.model_info import ModelInfo


class VLLMLauncher:

    @staticmethod
    def build_command(
        model: ModelInfo,
    ):

        return [

            "python",

            "-m",

            "vllm.entrypoints.openai.api_server",

            "--model",
            model.path,

            "--host",
            "0.0.0.0",

            "--port",
            str(model.port),

            "--dtype",
            model.dtype,

            "--tensor-parallel-size",
            str(model.tensor_parallel_size),

            "--gpu-memory-utilization",
            str(model.gpu_memory_utilization),

            "--max-model-len",
            str(model.max_context),

        ]