from dataclasses import dataclass
from dataclasses import field


# =====================================
# NOVELTY ANALYSIS MODEL
# =====================================

@dataclass
class NoveltyAnalysis:

    novelty_score: float = 0.0

    novelty_level: str = "LOW"

    reasons: list = field(
        default_factory=list
    )

    # =================================
    # RESERVED FOR NOVELTY V2
    # =================================

    technology_score: float = 0.0

    dataset_score: float = 0.0

    methodology_score: float = 0.0

    evaluation_score: float = 0.0

    temporal_score: float = 0.0

    domain_score: float = 0.0

    # =================================
    # SERIALIZATION
    # =================================

    def to_dict(self):

        return {

            "novelty_score":
            self.novelty_score,

            "novelty_level":
            self.novelty_level,

            "reasons":
            self.reasons,

            "technology_score":
            self.technology_score,

            "dataset_score":
            self.dataset_score,

            "methodology_score":
            self.methodology_score,

            "evaluation_score":
            self.evaluation_score,

            "temporal_score":
            self.temporal_score,

            "domain_score":
            self.domain_score
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

            novelty_score=data.get(
                "novelty_score",
                0.0
            ),

            novelty_level=data.get(
                "novelty_level",
                "LOW"
            ),

            reasons=data.get(
                "reasons",
                []
            ),

            technology_score=data.get(
                "technology_score",
                0.0
            ),

            dataset_score=data.get(
                "dataset_score",
                0.0
            ),

            methodology_score=data.get(
                "methodology_score",
                0.0
            ),

            evaluation_score=data.get(
                "evaluation_score",
                0.0
            ),

            temporal_score=data.get(
                "temporal_score",
                0.0
            ),

            domain_score=data.get(
                "domain_score",
                0.0
            )
        )

