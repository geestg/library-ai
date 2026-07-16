from __future__ import annotations

from delbot_platform.ai.registry.loader import (
    RegistryLoader,
)
from delbot_platform.ai.registry.model_backend import (
    ModelBackend,
)
from delbot_platform.ai.registry.model_backend_config import (
    ModelBackendConfig,
)
from delbot_platform.ai.registry.model_info import (
    ModelInfo,
)
from delbot_platform.ai.registry.model_runtime import (
    ModelRuntime,
)
from delbot_platform.core.path_manager import (
    PathManager,
)


class ModelRegistry:

    def __init__(self) -> None:

        config_file = (
            PathManager.CONFIG
            / "models.yaml"
        )

        self.data = RegistryLoader.load(
            config_file,
        )

    def _category(
        self,
        category: str,
    ) -> dict:

        return self.data[
            category
        ]

    def _build(
        self,
        category: str,
        name: str,
    ) -> ModelInfo:

        model = self._category(
            category,
        )["models"][name]

        runtime = ModelRuntime(
            host="0.0.0.0",
            port=model["port"],
        )

        backend_config = ModelBackendConfig(
            dtype=model["dtype"],
            max_context=model["max_context"],
            tensor_parallel_size=model["tensor_parallel_size"],
            gpu_memory_utilization=model["gpu_memory_utilization"],
        )

        return ModelInfo(
            name=name,
            backend=ModelBackend(
                model["backend"],
            ),
            path=str(
                PathManager.ROOT
                / model["path"]
            ),
            runtime=runtime,
            backend_config=backend_config,
        )

    def get(
        self,
        category: str,
        name: str,
    ) -> ModelInfo:

        return self._build(
            category,
            name,
        )

    def default(
        self,
        category: str,
    ) -> ModelInfo:

        default_name = self._category(
            category,
        )["default"]

        return self.get(
            category,
            default_name,
        )

    def categories(
        self,
    ) -> list[str]:

        return list(
            self.data.keys()
        )

    def models(
        self,
        category: str,
    ) -> list[str]:

        return list(
            self._category(
                category,
            )["models"].keys()
        )