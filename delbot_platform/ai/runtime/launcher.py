from __future__ import annotations

from delbot_platform.ai.launcher.factory import (
    LauncherFactory,
)
from delbot_platform.ai.process.process_info import (
    ProcessInfo,
)
from delbot_platform.ai.process.process_manager import (
    ProcessManager,
)
from delbot_platform.ai.registry.model_info import (
    ModelInfo,
)
from delbot_platform.ai.runtime.monitor import (
    RuntimeMonitor,
)
from delbot_platform.core.path_manager import (
    PathManager,
)


class RuntimeLauncher:

    def __init__(self) -> None:

        self.process = ProcessManager()

        self.monitor = RuntimeMonitor(
            self.process,
        )

    def start(
        self,
        model: ModelInfo,
    ) -> ProcessInfo:

        command = LauncherFactory.build(
            model,
        )

        process = self.process.start(
            name=model.name,
            command=command,
            workdir=PathManager.ROOT,
            host="0.0.0.0",
            port=model.port,
        )

        return self.monitor.wait(
            process,
        )