from delbot_platform.ai.registry.model_info import ModelInfo


class InfinityLauncher:

    @staticmethod
    def build_command(
        model: ModelInfo,
    ):

        return [

            "infinity_emb",

            "--model-id",
            model.path,

            "--port",
            str(model.port),

        ]