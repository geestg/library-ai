from __future__ import annotations

from delbot_platform.ai.launcher.factory import (
    LauncherFactory,
)
from delbot_platform.ai.process.process_manager import (
    ProcessManager,
)
from delbot_platform.ai.registry.model_info import (
    ModelInfo,
)
from delbot_platform.ai.runtime.manager import (
    RuntimeManager,
)
from delbot_platform.ai.runtime.process import (
    RuntimeProcess,
)
from delbot_platform.ai.runtime.state import (
    RuntimeState,
)
from delbot_platform.core.path_manager import (
    PathManager,
)


class RuntimeLauncher:

    def __init__(self) -> None:

        self.runtime = RuntimeManager()

        self.process = RuntimeProcess()

        self.manager = ProcessManager()

    def start(
        self,
        model: ModelInfo,
    ) -> RuntimeState:

        command = LauncherFactory.build(
            model,
        )

        pid = self.process.start(
            command=command,
            cwd=PathManager.ROOT,
        )

        state = RuntimeState(
            name=model.name,
            command=command,
            workdir=PathManager.ROOT,
            host="0.0.0.0",
            port=model.port,
            pid=pid,
            running=True,
        )

        self.runtime.register(
            state,
        )

        return state