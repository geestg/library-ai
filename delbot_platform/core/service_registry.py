from __future__ import annotations

from dataclasses import dataclass

from delbot_platform.core.config_manager import (
    ConfigManager,
)


@dataclass(slots=True)
class Service:

    name: str

    host: str

    port: int

    enabled: bool = True

    @property
    def url(self) -> str:

        return f"http://{self.host}:{self.port}"


class ServiceRegistry:

    def __init__(self):

        cfg = ConfigManager()

        self._services: dict[str, Service] = {}

        settings = cfg.services

        default_host = cfg.settings["server"]["host"]

        for name, value in settings.items():

            host = value.get(
                "host",
                default_host,
            )

            service = Service(
                name=name,
                host=host,
                port=value["port"],
                enabled=value.get(
                    "enabled",
                    True,
                ),
            )

            self._services[name] = service

    #
    # Backward-compatible API
    #

    def service(
        self,
        name: str,
    ) -> Service:

        return self.get(name)

    def all(self) -> list[Service]:

        return self.services()

    #
    # New API
    #

    def get(
        self,
        name: str,
    ) -> Service:

        return self._services[name]

    def services(self) -> list[Service]:

        return list(
            self._services.values()
        )

    def enabled(self) -> list[Service]:

        return [
            service
            for service in self._services.values()
            if service.enabled
        ]

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._services

    #
    # Pythonic API
    #

    def __contains__(
        self,
        name: str,
    ) -> bool:

        return self.exists(name)

    def __iter__(self):

        return iter(
            self._services.values()
        )

    def __len__(self):

        return len(
            self._services
        )