from __future__ import annotations

from dataclasses import dataclass

from delbot_platform.knowledge.graph.graph_edge import GraphEdge
from delbot_platform.knowledge.graph.graph_node import GraphNode
from delbot_platform.knowledge.graph.knowledge_graph import (
    KnowledgeGraph,
)
from delbot_platform.knowledge.models.knowledge_entity import (
    KnowledgeEntity,
)
from delbot_platform.knowledge.models.knowledge_relation import (
    KnowledgeRelation,
)


@dataclass(slots=True)
class GraphBuilder:

    def build(
        self,
        entities: list[KnowledgeEntity],
        relations: list[KnowledgeRelation],
    ) -> KnowledgeGraph:

        graph = KnowledgeGraph()

        for entity in entities:
            graph.add_node(
                GraphNode(
                    entity=entity,
                ),
            )

        for relation in relations:
            graph.add_edge(
                GraphEdge(
                    relation=relation,
                ),
            )

        return graph
