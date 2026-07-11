from dataclasses import dataclass
from dataclasses import field


# =====================================
# GAP ANALYSIS MODEL
# =====================================

@dataclass
class GapAnalysis:

    dominant_topics: list = field(
        default_factory=list
    )

    emerging_topics: list = field(
        default_factory=list
    )

    rare_topics: list = field(
        default_factory=list
    )

    method_gap: list = field(
        default_factory=list
    )

    dataset_gap: list = field(
        default_factory=list
    )

    temporal_gap: list = field(
        default_factory=list
    )

    evaluation_gap: list = field(
        default_factory=list
    )

    novelty_opportunities: list = field(
        default_factory=list
    )

    gap_score: int = 0

    # =================================
    # SERIALIZATION
    # =================================

    def to_dict(self):

        return {

            "dominant_topics":
            self.dominant_topics,

            "emerging_topics":
            self.emerging_topics,

            "rare_topics":
            self.rare_topics,

            "method_gap":
            self.method_gap,

            "dataset_gap":
            self.dataset_gap,

            "temporal_gap":
            self.temporal_gap,

            "evaluation_gap":
            self.evaluation_gap,

            "novelty_opportunities":
            self.novelty_opportunities,

            "gap_score":
            self.gap_score
        }

    # =================================
    # FACTORY
    # =================================

    @classmethod
    def from_dict(
        cls,
        data: dict
    ):

        if not data:

            return cls()

        return cls(

            dominant_topics=data.get(
                "dominant_topics",
                []
            ),

            emerging_topics=data.get(
                "emerging_topics",
                []
            ),

            rare_topics=data.get(
                "rare_topics",
                []
            ),

            method_gap=data.get(
                "method_gap",
                []
            ),

            dataset_gap=data.get(
                "dataset_gap",
                []
            ),

            temporal_gap=data.get(
                "temporal_gap",
                []
            ),

            evaluation_gap=data.get(
                "evaluation_gap",
                []
            ),

            novelty_opportunities=data.get(
                "novelty_opportunities",
                []
            ),

            gap_score=data.get(
                "gap_score",
                0
            )
        )
