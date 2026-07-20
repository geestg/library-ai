from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from delbot_platform.core.lifecycle.service_definition import (
    ServiceDefinition,
)

from delbot_platform.launcher.spec import (
    LaunchSpec,
)


class BaseLauncher(ABC):

    @abstractmethod
    def build(
        self,
        definition: ServiceDefinition,
    ) -> LaunchSpec:
        """
        Build LaunchSpec from a ServiceDefinition.
        """
        raise NotImplementedError
