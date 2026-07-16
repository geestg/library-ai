from __future__ import annotations

import sys

from delbot_platform.ai.registry.model_category import (
    ModelCategory,
)
from delbot_platform.ai.registry.registry import (
    ModelRegistry,
)
from delbot_platform.ai.runtime.launcher import (
    RuntimeLauncher,
)


class BaseRuntime:

    def __init__(
        self,
        category: ModelCategory,
    ) -> None:

        self.category = category

        self.registry = ModelRegistry()

        self.launcher = RuntimeLauncher()

    def run(
        self,
    ) -> None:

        model = self.registry.default(
            self.category,
        )

        print()

        print(
            f"Starting {self.category} Runtime"
        )

        print(
            f"Model : {model.name}"
        )

        print(
            f"Backend : {model.backend}"
        )

        print()

        try:

            process = self.launcher.start(
                model,
            )

        except Exception as exc:

            print(
                f"ERROR: {exc}"
            )

            sys.exit(1)

        print(
            f"PID : {process.pid}"
        )

        print()