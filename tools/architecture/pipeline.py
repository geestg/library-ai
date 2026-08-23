from __future__ import annotations

from pathlib import Path

from tools.architecture.circular import CircularAnalyzer
from tools.architecture.dependency import DependencyAnalyzer
from tools.architecture.graph import DependencyGraphBuilder
from tools.architecture.graph_filter import DependencyGraphFilter
from tools.architecture.layer import LayerAnalyzer
from tools.architecture.metrics import MetricsAnalyzer
from tools.architecture.models import (
    ArchitectureReport,
)


class ArchitecturePipeline:

    def analyze(
        self,
        root: Path,
        module_layers: dict[str, str] | None = None,
        allowed_dependencies: dict[str, set[str]] | None = None,
    ) -> ArchitectureReport:

        module_layers = module_layers or {}
        allowed_dependencies = allowed_dependencies or {}

        dependency = DependencyAnalyzer().analyze(
            root,
        )

        graph = DependencyGraphBuilder().build(
            dependency,
        )

        graph = DependencyGraphFilter().internal(
            graph,
        )

        circular = CircularAnalyzer().analyze(
            graph,
        )

        metrics = MetricsAnalyzer().analyze(
            graph,
        )

        layer = LayerAnalyzer().analyze(
            graph=graph,
            module_layers=module_layers,
            allowed_dependencies=allowed_dependencies,
        )

        return ArchitectureReport(
            dependency=dependency,
            graph=graph,
            circular=circular,
            metrics=metrics,
            layer=layer,
        )
