from __future__ import annotations

from delbot_platform.ai.recovery.recovery import (
    RecoveryManager,
)
from delbot_platform.controller.service_controller import (
    ServiceController,
)
from delbot_platform.core.config_manager import (
    ConfigManager,
)
from delbot_platform.core.environment import (
    EnvironmentManager,
)
from delbot_platform.core.runtime_manager import (
    RuntimeManager,
)


class StartupOrchestrator:

    def __init__(self):

        self.config = ConfigManager()

        self.controller = ServiceController()

    def initialize(self):

        EnvironmentManager.setup()

        RuntimeManager.ensure_directories()

    def recover(self):

        return RecoveryManager.load_states()

    def start_services(self):

        self.controller.start_all()

    def run(self):

        print()

        print("===================================")
        print("DELBot Platform")
        print("===================================")

        print()

        print("Initializing environment...")

        self.initialize()

        print("Environment OK")

        print()

        print("Recovering services...")

        states = self.recover()

        if not states:

            print(
                "No previous services found."
            )

        else:

            for state in states:

                status = (
                    "RUNNING"
                    if state["running"]
                    else "STOPPED"
                )

                print(
                    f"- {state['name']} ({status})"
                )

        print()

        print("Starting services...")

        self.start_services()

        print()

        print(
            "Platform initialization complete."
        )