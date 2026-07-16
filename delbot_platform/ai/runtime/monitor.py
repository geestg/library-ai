from __future__ import annotations

import time

from delbot_platform.ai.process.process_info import (
    ProcessInfo,
)
from delbot_platform.ai.process.process_manager import (
    ProcessManager,
)


class RuntimeMonitor:

    def __init__(
        self,
        process_manager: ProcessManager,
        startup_delay: float = 0.5,
    ) -> None:

        self.manager = process_manager

        self.startup_delay = startup_delay

    def wait(
        self,
        process: ProcessInfo,
    ) -> ProcessInfo:

        if process.process is None:

            raise RuntimeError(
                "Runtime process was not created."
            )

        time.sleep(
            self.startup_delay,
        )

        exit_code = process.process.poll()

        if exit_code is not None:

            self.manager.mark_failed(
                process.name,
            )

            raise RuntimeError(
                f"Runtime '{process.name}' exited "
                f"immediately with exit code "
                f"{exit_code}."
            )

        return self.manager.mark_running(
            process.name,
        )