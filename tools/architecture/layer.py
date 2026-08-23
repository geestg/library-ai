from __future__ import annotations

from tools.architecture.graph import DependencyGraph
from tools.architecture.models import (
    LayerReport,
    LayerViolation,
)


class LayerAnalyzer:

    def analyze(
        self,
        graph: DependencyGraph,
        module_layers: dict[str, str],
        allowed_dependencies: dict[str, set[str]],
    ) -> LayerReport:

        report = LayerReport()

        for source in sorted(graph.nodes()):

            source_layer = module_layers.get(source)

            if source_layer is None:
                continue

            for target in sorted(graph.dependencies(source)):

                target_layer = module_layers.get(target)

                if target_layer is None:
                    continue

                allowed = allowed_dependencies.get(
                    source_layer,
                    set(),
                )

                if target_layer in allowed:
                    continue

                report.violations.append(
                    LayerViolation(
                        source=source,
                        target=target,
                        source_layer=source_layer,
                        target_layer=target_layer,
                        reason=(
                            f"{source_layer} "
                            f"must not depend on "
                            f"{target_layer}"
                        ),
                    )
                )

        return report
