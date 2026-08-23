from __future__ import annotations

from delbot_platform.ai.process.process_manager import (
    ProcessManager,
)

from delbot_platform.core.lifecycle.orchestrator import (
    PlatformOrchestrator,
)


class ServiceController:

    def __init__(self) -> None:

        self.platform = PlatformOrchestrator()

        self.process = ProcessManager()

    ###########################################################################
    # Service
    ###########################################################################

    def start(
        self,
        name: str,
    ):

        spec = self.platform.launch_spec(name)

        return self.process.start(
            name=spec.name,
            command=spec.command,
            workdir=spec.workdir,
            host=spec.host,
            port=spec.port,
        )

    def stop(
        self,
        name: str,
    ):

        return self.process.stop(name)

    def restart(
        self,
        name: str,
    ):

        self.stop(name)

        return self.start(name)

    def status(
        self,
        name: str,
    ):

        return self.process.get(name)

    ###########################################################################
    # All Services
    ###########################################################################

    def start_all(self):

        result = []

        for definition in self.platform.definitions():

            result.append(
                self.start(
                    definition.name,
                )
            )

        return result

    def stop_all(self):

        result = []

        for definition in self.platform.definitions():

            result.append(
                self.stop(
                    definition.name,
                )
            )

        return result

    def restart_all(self):

        self.stop_all()

        return self.start_all()

    def status_all(self):

        return self.process.list()
