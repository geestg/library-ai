from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.knowledge.graph.graph_edge import GraphEdge
from delbot_platform.knowledge.graph.graph_node import GraphNode


@dataclass(slots=True)
class KnowledgeGraph:

    nodes: dict[str, GraphNode] = field(
        default_factory=dict,
    )

    edges: dict[str, GraphEdge] = field(
        default_factory=dict,
    )

    adjacency: dict[str, set[str]] = field(
        default_factory=dict,
    )

    def add_node(
        self,
        node: GraphNode,
    ) -> None:

        self.nodes[node.node_id] = node

        self.adjacency.setdefault(
            node.node_id,
            set(),
        )

    def add_edge(
        self,
        edge: GraphEdge,
    ) -> None:

        self.edges[edge.edge_id] = edge

        self.adjacency.setdefault(
            edge.source_node_id,
            set(),
        ).add(edge.edge_id)

        self.adjacency.setdefault(
            edge.target_node_id,
            set(),
        )

    def remove_node(
        self,
        node_id: str,
    ) -> None:

        self.nodes.pop(
            node_id,
            None,
        )

        self.adjacency.pop(
            node_id,
            None,
        )

    def remove_edge(
        self,
        edge_id: str,
    ) -> None:

        edge = self.edges.pop(
            edge_id,
            None,
        )

        if edge is None:
            return

        edge_ids = self.adjacency.get(
            edge.source_node_id,
        )

        if edge_ids is not None:
            edge_ids.discard(edge_id)

    def clear(
        self,
    ) -> None:

        self.nodes.clear()
        self.edges.clear()
        self.adjacency.clear()

    @property
    def node_count(
        self,
    ) -> int:

        return len(
            self.nodes,
        )

    @property
    def edge_count(
        self,
    ) -> int:

        return len(
            self.edges,
        )

    def all_nodes(
        self,
    ) -> list[GraphNode]:

        return list(
            self.nodes.values(),
        )

    def all_edges(
        self,
    ) -> list[GraphEdge]:

        return list(
            self.edges.values(),
        )

    def has_node(
        self,
        node_id: str,
    ) -> bool:

        return node_id in self.nodes

    def has_edge(
        self,
        edge_id: str,
    ) -> bool:

        return edge_id in self.edges

    def get_node(
        self,
        node_id: str,
    ) -> GraphNode | None:

        return self.nodes.get(
            node_id,
        )

    def get_edge(
        self,
        edge_id: str,
    ) -> GraphEdge | None:

        return self.edges.get(
            edge_id,
        )

    def export(
        self,
    ) -> dict:

        return {
            "nodes": {
                node_id: node.export()
                for node_id, node in self.nodes.items()
            },
            "edges": {
                edge_id: edge.export()
                for edge_id, edge in self.edges.items()
            },
            "adjacency": {
                node_id: sorted(edge_ids)
                for node_id, edge_ids in self.adjacency.items()
            },
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "KnowledgeGraph":

        graph = cls()

        for node_id, node_data in data.get(
            "nodes",
            {},
        ).items():
            graph.nodes[node_id] = GraphNode.from_dict(
                node_data,
            )

        for edge_id, edge_data in data.get(
            "edges",
            {},
        ).items():
            graph.edges[edge_id] = GraphEdge.from_dict(
                edge_data,
            )

        graph.adjacency = {
            node_id: set(edge_ids)
            for node_id, edge_ids in data.get(
                "adjacency",
                {},
            ).items()
        }

        return graph
