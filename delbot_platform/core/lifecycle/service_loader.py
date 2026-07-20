from __future__ import annotations

from delbot_platform.core.config_manager import ConfigManager

from delbot_platform.core.lifecycle.service_definition import (
    ServiceDefinition,
)


class ServiceLoader:

    #
    # Services managed by PlatformOrchestrator
    #

    MANAGED = (
        "gateway",
        "research_api",
        "chat",
        "embedding",
        "reranker",
        "vision",
        "ocr",
        "speech",
    )

    @staticmethod
    def load() -> list[ServiceDefinition]:

        cfg = ConfigManager()

        default_host = cfg.setting("server")["host"]

        services: list[ServiceDefinition] = []

        for name in ServiceLoader.MANAGED:

            value = cfg.service(name)

            services.append(
                ServiceDefinition(
                    name=name,
                    launcher=value.get("launcher", name),
                    host=value.get("host", default_host),
                    port=value["port"],
                )
            )

        return services
