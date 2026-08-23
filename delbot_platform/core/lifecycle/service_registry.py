"""
DELBot Service Registry.

Stores immutable service definitions.
"""

from __future__ import annotations

from .service_definition import ServiceDefinition


class ServiceRegistry:

    def __init__(self) -> None:

        self._services: dict[str, ServiceDefinition] = {}

    #
    # Registry
    #

    def register(
        self,
        definition: ServiceDefinition,
    ) -> None:

        self._services[definition.name] = definition

    def unregister(
        self,
        name: str,
    ) -> bool:

        return self._services.pop(
            name,
            None,
        ) is not None

    def clear(
        self,
    ) -> None:

        self._services.clear()

    #
    # Query
    #

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._services

    def get(
        self,
        name: str,
    ) -> ServiceDefinition:

        return self._services[name]

    def list(
        self,
    ) -> tuple[ServiceDefinition, ...]:

        return tuple(
            self._services.values()
        )

    def names(
        self,
    ) -> tuple[str, ...]:

        return tuple(
            self._services.keys()
        )

    def count(
        self,
    ) -> int:

        return len(
            self._services
        )
