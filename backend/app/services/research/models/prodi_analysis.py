from dataclasses import dataclass
from dataclasses import field


# =====================================
# PRODI ANALYSIS
# =====================================

@dataclass
class ProdiAnalysis:

    prodi: str = ""

    focus_areas: list = field(
        default_factory=list
    )

    dominant_competencies: list = field(
        default_factory=list
    )

    matched_competencies: list = field(
        default_factory=list
    )

    research_alignment: float = 0.0

    # =================================
    # SERIALIZATION
    # =================================

    def to_dict(self):

        return {

            "prodi":
            self.prodi,

            "focus_areas":
            self.focus_areas,

            "dominant_competencies":
            self.dominant_competencies,

            "matched_competencies":
            self.matched_competencies,

            "research_alignment":
            self.research_alignment
        }

    @classmethod
    def from_dict(
        cls,
        data: dict
    ):

        if not data:

            return cls()

        return cls(

            prodi=data.get(
                "prodi",
                ""
            ),

            focus_areas=data.get(
                "focus_areas",
                []
            ),

            dominant_competencies=data.get(
                "dominant_competencies",
                []
            ),

            matched_competencies=data.get(
                "matched_competencies",
                []
            ),

            research_alignment=data.get(
                "research_alignment",
                0.0
            )
        )
