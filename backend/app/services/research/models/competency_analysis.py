from dataclasses import dataclass
from dataclasses import field


# =====================================
# COMPETENCY ITEM
# =====================================

@dataclass
class CompetencyItem:

    name: str

    count: int = 0

    confidence: float = 0.0

    source: str = "evidence"

    # =================================
    # SERIALIZATION
    # =================================

    def to_dict(self):

        return {

            "name":
            self.name,

            "count":
            self.count,

            "confidence":
            self.confidence,

            "source":
            self.source
        }

    @classmethod
    def from_dict(
        cls,
        data: dict
    ):

        return cls(

            name=data.get(
                "name",
                ""
            ),

            count=data.get(
                "count",
                0
            ),

            confidence=data.get(
                "confidence",
                0.0
            ),

            source=data.get(
                "source",
                "evidence"
            )
        )


# =====================================
# COMPETENCY ANALYSIS
# =====================================

@dataclass
class CompetencyAnalysis:

    competencies: list = field(
        default_factory=list
    )

    total_competencies: int = 0

    dominant_competency: str = ""

    # =================================
    # SERIALIZATION
    # =================================

    def to_dict(self):

        return {

            "competencies":[

                competency.to_dict()

                for competency

                in self.competencies
            ],

            "total_competencies":
            self.total_competencies,

            "dominant_competency":
            self.dominant_competency
        }

    @classmethod
    def from_dict(
        cls,
        data: dict
    ):

        competencies = [

            CompetencyItem.from_dict(
                item
            )

            for item

            in data.get(
                "competencies",
                []
            )
        ]

        return cls(

            competencies=
            competencies,

            total_competencies=data.get(
                "total_competencies",
                len(competencies)
            ),

            dominant_competency=data.get(
                "dominant_competency",
                ""
            )
        )