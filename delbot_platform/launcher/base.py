from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from delbot_platform.launcher.spec import (
    LaunchSpec,
)


class BaseLauncher(ABC):

    @abstractmethod
    def build(self) -> LaunchSpec:
        """
        Build LaunchSpec for a service.
        """
        raise NotImplementedError