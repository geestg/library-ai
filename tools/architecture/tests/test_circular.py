from __future__ import annotations

from tools.architecture.circular import CircularAnalyzer
from tools.architecture.graph import DependencyGraph
from tools.architecture.models import ModuleDependency


def build_graph(
    edges: dict[str, set[str]],
) -> DependencyGraph:

    modules = {
        name: ModuleDependency(module=name)
        for name in edges
    }

    outgoing = {
        node: set(targets)
        for node, targets in edges.items()
    }

    incoming = {
        node: set()
        for node in edges
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


def cycles(
    graph: DependencyGraph,
) -> list[tuple[str, ...]]:

    report = CircularAnalyzer().analyze(
        graph,
    )

    return [
        cycle.modules
        for cycle in report.cycles
    ]


def test_no_cycle() -> None:

    graph = build_graph(
        {
            "A": {"B"},
            "B": {"C"},
            "C": set(),
        }
    )

    assert cycles(graph) == []


def test_two_node_cycle() -> None:

    graph = build_graph(
        {
            "A": {"B"},
            "B": {"A"},
        }
    )

    assert cycles(graph) == [
        ("A", "B"),
    ]


def test_three_node_cycle() -> None:

    graph = build_graph(
        {
            "A": {"B"},
            "B": {"C"},
            "C": {"A"},
        }
    )

    assert cycles(graph) == [
        ("A", "B", "C"),
    ]


def test_multiple_cycles() -> None:

    graph = build_graph(
        {
            "A": {"B"},
            "B": {"A"},
            "C": {"D"},
            "D": {"C"},
        }
    )

    assert cycles(graph) == [
        ("A", "B"),
        ("C", "D"),
    ]


def test_self_loop_ignored() -> None:

    graph = build_graph(
        {
            "A": {"A"},
        }
    )

    assert cycles(graph) == []
