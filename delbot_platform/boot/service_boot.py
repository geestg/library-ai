from __future__ import annotations

from delbot_platform.ai.process.process_manager import (
    ProcessManager,
)

from delbot_platform.boot.service_waiter import (
    ServiceWaiter,
)

from delbot_platform.launcher.spec import (
    LaunchSpec,
)


class ServiceBoot:

    def __init__(self):

        self.pm = ProcessManager()

        self.waiter = ServiceWaiter()

    def start(
        self,
        spec: LaunchSpec,
    ):

        process = self.pm.start(
            name=spec.name,
            command=spec.command,
            workdir=spec.workdir,
            host=spec.host,
            port=spec.port,
        )

        if spec.health_check:

            self.waiter.wait(
                host=spec.host,
                port=spec.port,
                endpoint=spec.health_endpoint,
            )

        return process