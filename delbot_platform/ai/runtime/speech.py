from __future__ import annotations

from delbot_platform.ai.runtime.base import (
    BaseRuntime,
)

from delbot_platform.ai.registry.model_category import (
    ModelCategory,
)


def main() -> None:

    BaseRuntime(
        ModelCategory.SPEECH,
    ).run()


if __name__ == "__main__":

    main()