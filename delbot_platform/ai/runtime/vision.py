from __future__ import annotations

from delbot_platform.ai.registry.model_category import ModelCategory
from delbot_platform.ai.runtime.base import (
    BaseRuntime,
)


def main() -> None:

    BaseRuntime(
        ModelCategory.VISION,
    ).run()


if __name__ == "__main__":

    main()