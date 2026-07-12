from dataclasses import dataclass
from dataclasses import field


# =====================================
# TREND ANALYSIS MODEL
# =====================================

@dataclass
class TrendAnalysis:

    top_technologies: list = field(
        default_factory=list
    )

    top_methods: list = field(
        default_factory=list
    )

    top_datasets: list = field(
        default_factory=list
    )

    emerging_topics: list = field(
        default_factory=list
    )

    research_trends: list = field(
        default_factory=list
    )

    # =================================
    # SERIALIZATION
    # =================================

    def to_dict(self):

        return {

            "top_technologies":
            self.top_technologies,

            "top_methods":
            self.top_methods,

            "top_datasets":
            self.top_datasets,

            "emerging_topics":
            self.emerging_topics,

            "research_trends":
            self.research_trends
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

            top_technologies=data.get(
                "top_technologies",
                []
            ),

            top_methods=data.get(
                "top_methods",
                []
            ),

            top_datasets=data.get(
                "top_datasets",
                []
            ),

            emerging_topics=data.get(
                "emerging_topics",
                []
            ),

            research_trends=data.get(
                "research_trends",
                []
            )
        )

