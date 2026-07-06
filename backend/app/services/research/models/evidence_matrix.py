from dataclasses import dataclass
from dataclasses import field


# =====================================
# EVIDENCE MATRIX
# =====================================

@dataclass
class EvidenceMatrix:

    technology_frequency: dict = field(
        default_factory=dict
    )

    methodology_frequency: dict = field(
        default_factory=dict
    )

    keyword_frequency: dict = field(
        default_factory=dict
    )

    domain_frequency: dict = field(
        default_factory=dict
    )

    dataset_frequency: dict = field(
        default_factory=dict
    )

    evaluation_frequency: dict = field(
        default_factory=dict
    )

    year_frequency: dict = field(
        default_factory=dict
    )

    # =================================
    # SERIALIZATION
    # =================================

    def to_dict(self):

        return {

            "technology_frequency":
            self.technology_frequency,

            "methodology_frequency":
            self.methodology_frequency,

            "keyword_frequency":
            self.keyword_frequency,

            "domain_frequency":
            self.domain_frequency,

            "dataset_frequency":
            self.dataset_frequency,

            "evaluation_frequency":
            self.evaluation_frequency,

            "year_frequency":
            self.year_frequency
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

            technology_frequency=data.get(
                "technology_frequency",
                {}
            ),

            methodology_frequency=data.get(
                "methodology_frequency",
                {}
            ),

            keyword_frequency=data.get(
                "keyword_frequency",
                {}
            ),

            domain_frequency=data.get(
                "domain_frequency",
                {}
            ),

            dataset_frequency=data.get(
                "dataset_frequency",
                {}
            ),

            evaluation_frequency=data.get(
                "evaluation_frequency",
                {}
            ),

            year_frequency=data.get(
                "year_frequency",
                {}
            )
        )

    # =================================
    # HELPERS
    # =================================

    def top_technologies(
        self,
        limit: int = 5
    ):

        return sorted(

            self.technology_frequency.items(),

            key=lambda item: item[1],

            reverse=True

        )[:limit]

    def top_methodologies(
        self,
        limit: int = 5
    ):

        return sorted(

            self.methodology_frequency.items(),

            key=lambda item: item[1],

            reverse=True

        )[:limit]

    def top_domains(
        self,
        limit: int = 5
    ):

        return sorted(

            self.domain_frequency.items(),

            key=lambda item: item[1],

            reverse=True

        )[:limit]

    def top_datasets(
        self,
        limit: int = 5
    ):

        return sorted(

            self.dataset_frequency.items(),

            key=lambda item: item[1],

            reverse=True

        )[:limit]

    def latest_year(self):

        if not self.year_frequency:

            return None

        years = []

        for year in self.year_frequency:

            try:

                years.append(
                    int(year)
                )

            except ValueError:

                continue

        if not years:

            return None

        return max(years)