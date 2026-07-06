from dataclasses import dataclass
from dataclasses import field

from app.services.research.models.trend_analysis import (
    TrendAnalysis
)

from app.services.research.models.gap_analysis import (
    GapAnalysis
)

from app.services.research.models.novelty_analysis import (
    NoveltyAnalysis
)

from app.services.research.models.competency_analysis import (
    CompetencyAnalysis
)

from app.services.research.models.prodi_analysis import (
    ProdiAnalysis
)


# =====================================
# RESEARCH PROFILE
# =====================================

@dataclass
class ResearchProfile:

    trend: TrendAnalysis = field(
        default_factory=TrendAnalysis
    )

    gap: GapAnalysis = field(
        default_factory=GapAnalysis
    )

    novelty: NoveltyAnalysis = field(
        default_factory=NoveltyAnalysis
    )

    competency: CompetencyAnalysis = field(
        default_factory=CompetencyAnalysis
    )

    prodi: ProdiAnalysis = field(
        default_factory=ProdiAnalysis
    )

    # =================================
    # SERIALIZATION
    # =================================

    def to_dict(self):

        return {

            "trend":
            self.trend.to_dict(),

            "gap":
            self.gap.to_dict(),

            "novelty":
            self.novelty.to_dict(),

            "competency":
            self.competency.to_dict(),

            "prodi":
            self.prodi.to_dict()
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

            trend=TrendAnalysis.from_dict(
                data.get(
                    "trend",
                    {}
                )
            ),

            gap=GapAnalysis.from_dict(
                data.get(
                    "gap",
                    {}
                )
            ),

            novelty=NoveltyAnalysis.from_dict(
                data.get(
                    "novelty",
                    {}
                )
            ),

            competency=CompetencyAnalysis.from_dict(
                data.get(
                    "competency",
                    {}
                )
            ),

            prodi=ProdiAnalysis.from_dict(
                data.get(
                    "prodi",
                    {}
                )
            )
        )