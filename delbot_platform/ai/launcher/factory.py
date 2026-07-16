from __future__ import annotations

from delbot_platform.ai.launcher.infinity import (
    InfinityLauncher,
)
from delbot_platform.ai.launcher.native import (
    NativeLauncher,
)
from delbot_platform.ai.launcher.vllm import (
    VLLMLauncher,
)
from delbot_platform.ai.registry.model_backend import (
    ModelBackend,
)


class LauncherFactory:

    @staticmethod
    def build(
        model,
    ):

        match model.backend:

            case ModelBackend.VLLM:

                return VLLMLauncher.build_command(
                    model,
                )

            case ModelBackend.INFINITY:

                return InfinityLauncher.build_command(
                    model,
                )

            case ModelBackend.NATIVE:

                return NativeLauncher.build_command(
                    model,
                )

            case _:

                raise ValueError(
                    f"Unsupported backend: {model.backend}"
                )