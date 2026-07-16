from __future__ import annotations

from delbot_platform.ai.process.process_info import (
    ProcessInfo,
)


class ProcessMonitor:

    def is_running(
        self,
        process: ProcessInfo,
    ) -> bool:

        if process.process is None:

            return False

        return process.process.poll() is None

    def exit_code(
        self,
        process: ProcessInfo,
    ) -> int | None:

        if process.process is None:

            return None

        return process.process.poll()

    def refresh(
        self,
        process: ProcessInfo,
    ) -> ProcessInfo:

        process.running = self.is_running(
            process,
        )

        return process

    def wait(
        self,
        process: ProcessInfo,
    ) -> int:

        if process.process is None:

            raise RuntimeError(
                "Process is not running."
            )

        return process.process.wait()

    def terminate(
        self,
        process: ProcessInfo,
    ) -> None:

        if process.process is None:

            return

        process.process.terminate()

        process.process.wait()