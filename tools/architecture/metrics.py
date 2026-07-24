from __future__ import annotations

from tools.architecture.graph import DependencyGraph
from tools.architecture.models import (
    MetricsReport,
    ModuleMetrics,
)


class MetricsAnalyzer:

    def analyze(
        self,
        graph: DependencyGraph,
    ) -> MetricsReport:

        report = MetricsReport()

        for module in sorted(
            graph.nodes(),
        ):

            fan_in = graph.in_degree(
                module,
            )

            fan_out = graph.out_degree(
                module,
            )

            report.modules.append(
                ModuleMetrics(
                    module=module,
                    fan_in=fan_in,
                    fan_out=fan_out,
                    is_root=fan_in == 0,
                    is_leaf=fan_out == 0,
                    is_isolated=(
                        fan_in == 0
                        and fan_out == 0
                    ),
                )
            )

        return report
