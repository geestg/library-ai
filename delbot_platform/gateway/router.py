from __future__ import annotations

from delbot_platform.ai.registry.model_category import (
    ModelCategory,
)
from delbot_platform.ai.registry.registry import (
    ModelRegistry,
)


class GatewayRouter:

    def __init__(self) -> None:

        self.registry = ModelRegistry()

    def runtime(
        self,
        category: ModelCategory,
    ):

        return self.registry.default(
            category,
        ).runtime