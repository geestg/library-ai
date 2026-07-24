"""
DELBot Service Definition.

Represents the static definition of a managed platform service.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from .boot_policy import BootPolicy
from .service_dependency import ServiceDependency


@dataclass(frozen=True, slots=True)
class ServiceDefinition:
    """
    Immutable definition of a managed platform service.

    This object is launcher-agnostic.

    A launcher may execute:

    - native python process
    - docker container
    - external executable
    - future kubernetes runtime

    without changing the public API.
    """

    #
    # Identity
    #

    name: str

    #
    # Launcher
    #

    launcher: str

    #
    # Network
    #

    host: str = "127.0.0.1"

    port: int = 0

    #
    # Lifecycle
    #

    boot_policy: BootPolicy = field(
        default_factory=BootPolicy,
    )

    dependency: ServiceDependency | None = None

    #
    # Metadata
    #

    tags: tuple[str, ...] = field(
        default_factory=tuple,
    )

    environment: dict[str, str] = field(
        default_factory=dict,
    )

    #
    # Container Runtime
    #

    image: str | None = None

    command: tuple[str, ...] = field(
        default_factory=tuple,
    )

    arguments: tuple[str, ...] = field(
        default_factory=tuple,
    )

    volumes: tuple[str, ...] = field(
        default_factory=tuple,
    )

    devices: tuple[str, ...] = field(
        default_factory=tuple,
    )

    gpus: bool = False

    restart: str = "unless-stopped"
