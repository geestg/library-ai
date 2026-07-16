from __future__ import annotations

import subprocess
from pathlib import Path

from delbot_platform.ai.process.process_info import (
    ProcessInfo,
)
from delbot_platform.ai.process.process_monitor import (
    ProcessMonitor,
)
from delbot_platform.ai.process.process_registry import (
    ProcessRegistry,
)


class ProcessManager:

    def __init__(self) -> None:

        self.registry = ProcessRegistry()

        self.monitor = ProcessMonitor()

    #
    # Lifecycle
    #

    def start(
        self,
        *,
        name: str,
        command: list[str],
        workdir: Path,
        host: str = "127.0.0.1",
        port: int = 0,
    ) -> ProcessInfo:

        proc = subprocess.Popen(
            command,
            cwd=workdir,
        )

        info = ProcessInfo(
            name=name,
            command=command,
            workdir=workdir,
            pid=proc.pid,
            process=proc,
            running=False,
            host=host,
            port=port,
        )

        self.registry.register(
            info,
        )

        return info

    def stop(
        self,
        name: str,
    ) -> bool:

        process = self.registry.get(
            name,
        )

        if process is None:

            return False

        self.monitor.terminate(
            process,
        )

        process.process = None
        process.pid = None
        process.running = False

        self.registry.register(
            process,
        )

        return True

    #
    # State
    #

    def mark_running(
        self,
        name: str,
    ) -> ProcessInfo:

        process = self.registry.get(
            name,
        )

        if process is None:

            raise KeyError(name)

        process.running = True

        self.registry.register(
            process,
        )

        return process

    def mark_failed(
        self,
        name: str,
    ) -> ProcessInfo:

        process = self.registry.get(
            name,
        )

        if process is None:

            raise KeyError(name)

        process.running = False

        self.registry.register(
            process,
        )

        return process

    #
    # Query
    #

    def get(
        self,
        name: str,
    ) -> ProcessInfo | None:

        process = self.registry.get(
            name,
        )

        if process is None:

            return None

        return self.monitor.refresh(
            process,
        )

    def list(
        self,
    ) -> list[ProcessInfo]:

        return [
            self.monitor.refresh(
                process,
            )
            for process in self.registry.list()
        ]

    def exists(
        self,
        name: str,
    ) -> bool:

        return self.registry.exists(
            name,
        )

    def running(
        self,
        name: str,
    ) -> bool:

        process = self.get(
            name,
        )

        if process is None:

            return False

        return process.running