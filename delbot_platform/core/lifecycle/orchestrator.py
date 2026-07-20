"""
DELBot Platform Orchestrator.

Coordinates lifecycle state transitions and launcher resolution.
"""

from __future__ import annotations

from delbot_platform.core.lifecycle.service_definition import (
    ServiceDefinition,
)
from delbot_platform.core.lifecycle.service_loader import (
    ServiceLoader,
)
from delbot_platform.core.lifecycle.service_registry import (
    ServiceRegistry,
)
from delbot_platform.core.lifecycle.service_state import (
    ServiceState,
)
from delbot_platform.core.lifecycle.state_machine import (
    StateMachine,
)

from delbot_platform.launcher.factory import (
    LauncherFactory,
)
from delbot_platform.launcher.spec import (
    LaunchSpec,
)


class PlatformOrchestrator:

    def __init__(self) -> None:

        self._registry = ServiceRegistry()

        self._states: dict[str, ServiceState] = {}

        #
        # Auto load services
        #

        for definition in ServiceLoader.load():

            self.register(
                definition,
            )

    #
    # Registry
    #

    def register(
        self,
        definition: ServiceDefinition,
    ) -> None:

        self._registry.register(
            definition,
        )

        self._states.setdefault(
            definition.name,
            ServiceState.STOPPED,
        )

    def exists(
        self,
        name: str,
    ) -> bool:

        return self._registry.exists(
            name,
        )

    def definition(
        self,
        name: str,
    ) -> ServiceDefinition:

        return self._registry.get(
            name,
        )

    def definitions(
        self,
    ) -> tuple[ServiceDefinition, ...]:

        return self._registry.list()

    #
    # Launch
    #

    def launch_spec(
        self,
        name: str,
    ) -> LaunchSpec:

        definition = self.definition(
            name,
        )

        launcher = LauncherFactory.create(
            definition,
        )

        return launcher.build(definition)

    #
    # State
    #

    def state(
        self,
        name: str,
    ) -> ServiceState:

        return self._states[name]

    def transition(
        self,
        name: str,
        target: ServiceState,
    ) -> ServiceState:

        current = self.state(
            name,
        )

        if not StateMachine.can_transition(
            current,
            target,
        ):
            raise ValueError(
                f"Invalid transition: {current.value} -> {target.value}"
            )

        self._states[name] = target

        return target

    #
    # Lifecycle
    #

    def start(
        self,
        name: str,
    ) -> ServiceState:

        return self.transition(
            name,
            ServiceState.INITIALIZING,
        )

    def stop(
        self,
        name: str,
    ) -> ServiceState:

        return self.transition(
            name,
            ServiceState.STOPPING,
        )
