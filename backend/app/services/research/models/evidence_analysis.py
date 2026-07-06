from dataclasses import dataclass
from dataclasses import field


# =====================================
# EVIDENCE ITEM
# =====================================

@dataclass
class EvidenceItem:

    name: str = ""

    count: int = 0

    def to_dict(self):

        return {

            "name": self.name,

            "count": self.count
        }

    @classmethod
    def from_dict(
        cls,
        data: dict
    ):

        if not data:

            return cls()

        return cls(

            name=data.get(
                "name",
                ""
            ),

            count=data.get(
                "count",
                0
            )
        )


# =====================================
# EVIDENCE ANALYSIS
# =====================================

@dataclass
class EvidenceAnalysis:

    technologies: list[EvidenceItem] = field(
        default_factory=list
    )

    methodologies: list[EvidenceItem] = field(
        default_factory=list
    )

    keywords: list[EvidenceItem] = field(
        default_factory=list
    )

    research_domains: list[EvidenceItem] = field(
        default_factory=list
    )

    datasets: list[EvidenceItem] = field(
        default_factory=list
    )

    evaluation_metrics: list[EvidenceItem] = field(
        default_factory=list
    )

    years: list[EvidenceItem] = field(
        default_factory=list
    )

    # =================================
    # SERIALIZATION
    # =================================

    def to_dict(self):

        return {

            "technologies": [

                item.to_dict()

                for item in self.technologies
            ],

            "methodologies": [

                item.to_dict()

                for item in self.methodologies
            ],

            "keywords": [

                item.to_dict()

                for item in self.keywords
            ],

            "research_domains": [

                item.to_dict()

                for item in self.research_domains
            ],

            "datasets": [

                item.to_dict()

                for item in self.datasets
            ],

            "evaluation_metrics": [

                item.to_dict()

                for item in self.evaluation_metrics
            ],

            "years": [

                item.to_dict()

                for item in self.years
            ]
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

            technologies=[

                EvidenceItem.from_dict(x)

                for x in data.get(
                    "technologies",
                    []
                )
            ],

            methodologies=[

                EvidenceItem.from_dict(x)

                for x in data.get(
                    "methodologies",
                    []
                )
            ],

            keywords=[

                EvidenceItem.from_dict(x)

                for x in data.get(
                    "keywords",
                    []
                )
            ],

            research_domains=[

                EvidenceItem.from_dict(x)

                for x in data.get(
                    "research_domains",
                    []
                )
            ],

            datasets=[

                EvidenceItem.from_dict(x)

                for x in data.get(
                    "datasets",
                    []
                )
            ],

            evaluation_metrics=[

                EvidenceItem.from_dict(x)

                for x in data.get(
                    "evaluation_metrics",
                    []
                )
            ],

            years=[

                EvidenceItem.from_dict(x)

                for x in data.get(
                    "years",
                    []
                )
            ]
        )