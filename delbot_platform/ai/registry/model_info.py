from __future__ import annotations

from dataclasses import dataclass

from delbot_platform.ai.registry.model_backend import (
    ModelBackend,
)
from delbot_platform.ai.registry.model_backend_config import (
    ModelBackendConfig,
)
from delbot_platform.ai.registry.model_runtime import (
    ModelRuntime,
)


@dataclass(slots=True)
class ModelInfo:

    name: str

    backend: ModelBackend

    path: str

    runtime: ModelRuntime

    backend_config: ModelBackendConfig