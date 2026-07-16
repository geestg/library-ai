from __future__ import annotations

import time

from delbot_platform.ai.process.process_info import (
    ProcessInfo,
)
from delbot_platform.ai.process.process_manager import (
    ProcessManager,
)
from delbot_platform.boot.boot_result import (
    BootResult,
)
from delbot_platform.boot.boot_state import (
    BootState,
)
from delbot_platform.boot.service_waiter import (
    ServiceWaiter,
)
from delbot_platform.launcher.spec import (
    LaunchSpec,
)


class ServiceBoot:

    def __init__(self) -> None:

        self.pm = ProcessManager()

        self.waiter = ServiceWaiter()

    def start(
        self,
        spec: LaunchSpec,
    ) -> BootResult:

        started = time.perf_counter()

        process: ProcessInfo = self.pm.start(
            name=spec.name,
            command=spec.command,
            workdir=spec.workdir,
            host=spec.host,
            port=spec.port,
        )

        try:

            if spec.health_check:

                self.waiter.wait(
                    host=spec.host,
                    port=spec.port,
                    endpoint=spec.health_endpoint,
                )

            self.pm.mark_running(
                process.name,
            )

            return BootResult(
                service=process.name,
                state=BootState.READY,
                pid=process.pid,
                host=process.host,
                port=process.port,
                elapsed=time.perf_counter() - started,
            )

        except TimeoutError as exc:

            self.pm.mark_failed(
                process.name,
            )

            return BootResult(
                service=process.name,
                state=BootState.TIMEOUT,
                pid=process.pid,
                host=process.host,
                port=process.port,
                elapsed=time.perf_counter() - started,
                message=str(exc),
            )

        except Exception as exc:

            self.pm.mark_failed(
                process.name,
            )

            return BootResult(
                service=process.name,
                state=BootState.FAILED,
                pid=process.pid,
                host=process.host,
                port=process.port,
                elapsed=time.perf_counter() - started,
                message=str(exc),
            )