from __future__ import annotations

from tools.architecture.graph import DependencyGraph
from tools.architecture.metrics import MetricsAnalyzer
from tools.architecture.models import (
    ModuleDependency,
    ModuleMetrics,
)


def build_graph(
    edges: dict[str, set[str]],
) -> DependencyGraph:

    modules = {
        module: ModuleDependency(
            module=module,
        )
        for module in edges
    }

    outgoing = {
        module: set(targets)
        for module, targets in edges.items()
    }

    incoming = {
        module: set()
        for module in edges
    }

    for source, targets in outgoing.items():

        for target in targets:

            incoming.setdefault(
                target,
                set(),
            ).add(source)

    return DependencyGraph(
        modules=modules,
        outgoing=outgoing,
        incoming=incoming,
    )


def metrics(
    graph: DependencyGraph,
) -> dict[str, ModuleMetrics]:

    report = MetricsAnalyzer().analyze(
        graph,
    )

    return {
        module.module: module
        for module in report.modules
    }


def test_linear_graph() -> None:

    result = metrics(
        build_graph(
            {
                "A": {"B"},
                "B": {"C"},
                "C": set(),
            }
        )
    )

    assert result["A"].fan_in == 0
    assert result["A"].fan_out == 1
    assert result["A"].is_root
    assert not result["A"].is_leaf

    assert result["B"].fan_in == 1
    assert result["B"].fan_out == 1

    assert result["C"].fan_in == 1
    assert result["C"].fan_out == 0
    assert result["C"].is_leaf


def test_isolated_node() -> None:

    result = metrics(
        build_graph(
            {
                "A": set(),
            }
        )
    )

    assert result["A"].fan_in == 0
    assert result["A"].fan_out == 0
    assert result["A"].is_root
    assert result["A"].is_leaf
    assert result["A"].is_isolated


def test_fan_in() -> None:

    result = metrics(
        build_graph(
            {
                "A": {"C"},
                "B": {"C"},
                "C": set(),
            }
        )
    )

    assert result["C"].fan_in == 2


def test_fan_out() -> None:

    result = metrics(
        build_graph(
            {
                "A": {"B", "C"},
                "B": set(),
                "C": set(),
            }
        )
    )

    assert result["A"].fan_out == 2


def test_mixed_graph() -> None:

    result = metrics(
        build_graph(
            {
                "A": {"B", "C"},
                "B": {"D"},
                "C": set(),
                "D": set(),
                "E": set(),
            }
        )
    )

    assert result["A"].is_root
    assert result["D"].is_leaf
    assert result["E"].is_isolated
