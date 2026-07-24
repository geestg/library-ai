from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from tools.architecture.graph import DependencyGraph


@dataclass(slots=True)
class ImportRecord:

    kind: str

    module: str

    names: list[str] = field(
        default_factory=list,
    )

    level: int = 0


@dataclass(slots=True)
class ModuleDependency:

    module: str

    imports: list[str] = field(
        default_factory=list,
    )

    import_records: list[ImportRecord] = field(
        default_factory=list,
    )


@dataclass(slots=True)
class DependencyReport:

    modules: list[ModuleDependency] = field(
        default_factory=list,
    )

    duplicate_modules: list[str] = field(
        default_factory=list,
    )

    orphan_modules: list[str] = field(
        default_factory=list,
    )


@dataclass(slots=True)
class RepositoryFile:

    path: Path

    relative_path: Path

    extension: str

    category: str


@dataclass(slots=True)
class RepositoryInventory:

    root: Path

    files: list[RepositoryFile] = field(
        default_factory=list,
    )

    directories: list[Path] = field(
        default_factory=list,
    )


@dataclass(slots=True, frozen=True)
class CircularDependency:

    modules: tuple[str, ...]


@dataclass(slots=True)
class CircularDependencyReport:

    cycles: list[CircularDependency] = field(
        default_factory=list,
    )


@dataclass(slots=True, frozen=True)
class ModuleMetrics:

    module: str

    fan_in: int

    fan_out: int

    is_root: bool

    is_leaf: bool

    is_isolated: bool


@dataclass(slots=True)
class MetricsReport:

    modules: list[ModuleMetrics] = field(
        default_factory=list,
    )


@dataclass(slots=True, frozen=True)
class LayerViolation:

    source: str

    target: str

    source_layer: str

    target_layer: str

    reason: str


@dataclass(slots=True)
class LayerReport:

    violations: list[LayerViolation] = field(
        default_factory=list,
    )


@dataclass(slots=True)
class ArchitectureReport:

    dependency: DependencyReport

    graph: DependencyGraph

    circular: CircularDependencyReport

    metrics: MetricsReport

    layer: LayerReport


@dataclass(slots=True, frozen=True)
class ArchitectureSummary:

    module_count: int

    edge_count: int

    cycle_count: int

    layer_violation_count: int

    root_module_count: int

    leaf_module_count: int

    isolated_module_count: int
