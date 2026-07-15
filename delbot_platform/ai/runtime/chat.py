from __future__ import annotations

from delbot_platform.ai.launcher.factory import (
    LauncherFactory,
)
from delbot_platform.ai.registry.registry import (
    ModelRegistry,
)


def main() -> None:

    registry = ModelRegistry()

    model = registry.chat_default()

    command = LauncherFactory.build(
        model,
    )

    print()

    print(
        f"Starting Chat Runtime: {model.name}"
    )

    print()

    print("Backend :")
    print(
        f"  {model.backend}"
    )

    print()

    print("Command :")

    for arg in command:

        print(
            f"  {arg}"
        )

    print()


if __name__ == "__main__":

    main()