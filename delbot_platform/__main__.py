import argparse

from delbot_platform.core.config_manager import ConfigManager
from delbot_platform.core.path_manager import PathManager
from delbot_platform.core.runtime_manager import RuntimeManager

from delbot_platform.orchestrator.startup import (
    StartupOrchestrator,
)


def cmd_status():

    cfg = ConfigManager()

    print()
    print("===================================")
    print("DELBot Platform")
    print("===================================")

    print()

    print(
        "Project :",
        cfg.setting("project")["name"],
    )

    print(
        "Version :",
        cfg.setting("project")["version"],
    )

    print()

    print("Paths")
    print("------")

    print(
        "Root     :",
        PathManager.ROOT,
    )

    print(
        "Backend  :",
        PathManager.BACKEND,
    )

    print(
        "Frontend :",
        PathManager.FRONTEND,
    )

    print(
        "Config   :",
        PathManager.CONFIG,
    )

    print(
        "Runtime  :",
        PathManager.RUNTIME,
    )

    print(
        "Models   :",
        PathManager.MODELS,
    )

    print(
        "Cache    :",
        PathManager.CACHE,
    )

    print(
        "Logs     :",
        PathManager.LOGS,
    )

    print(
        "Data     :",
        PathManager.DATA,
    )

    print()

    print("Runtime")
    print("-------")

    print(
        "PID      :",
        RuntimeManager.PID_DIR,
    )

    print(
        "Socket   :",
        RuntimeManager.SOCKET_DIR,
    )

    print(
        "State    :",
        RuntimeManager.STATE_DIR,
    )

    print(
        "Temp     :",
        RuntimeManager.TMP_DIR,
    )

    print()


def cmd_start():

    StartupOrchestrator().run()


def main():

    parser = argparse.ArgumentParser(
        prog="delbot_platform",
        description="DELBot Platform CLI",
    )

    parser.add_argument(
        "command",
        choices=[
            "start",
            "status",
        ],
    )

    args = parser.parse_args()

    if args.command == "start":

        cmd_start()

    elif args.command == "status":

        cmd_status()


if __name__ == "__main__":

    main()