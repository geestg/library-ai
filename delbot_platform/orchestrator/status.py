from __future__ import annotations

from delbot_platform.ai.process.process_registry import (
    ProcessRegistry,
)


class StatusOrchestrator:

    def __init__(self) -> None:

        self.registry = ProcessRegistry()

    def services(
        self,
    ) -> list[dict]:

        return self.registry.load_runtime_states()

    def run(
        self,
    ) -> None:

        states = self.services()

        print()

        print("===================================")
        print("DELBot Platform Status")
        print("===================================")

        if not states:

            print()
            print("No services registered.")
            print()

            return

        print()

        for state in states:

            status = (
                "RUNNING"
                if state["running"]
                else "STOPPED"
            )

            print(
                f"{state['name']:<15}"
                f"{status:<10}"
                f"PID={state['pid']}"
            )

        print()