from delbot_platform.ai.launcher.infinity import InfinityLauncher
from delbot_platform.ai.launcher.native import NativeLauncher
from delbot_platform.ai.launcher.vllm import VLLMLauncher


class LauncherFactory:

    @staticmethod
    def build(
        model,
    ):

        if model.backend == "vllm":
            return VLLMLauncher.build_command(model)

        if model.backend == "infinity":
            return InfinityLauncher.build_command(model)

        if model.backend == "native":
            return NativeLauncher.build_command(model)

        raise ValueError(
            f"Unsupported backend: {model.backend}"
        )