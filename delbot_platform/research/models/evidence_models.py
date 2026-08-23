from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Any


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
    def from_dict(cls, data: dict):
        if not data:
            return cls()
        return cls(
            name=data.get("name", ""),
            count=data.get("count", 0)
        )


@dataclass
class EvidenceAnalysis:
    technologies: list[EvidenceItem] = field(default_factory=list)
    methodologies: list[EvidenceItem] = field(default_factory=list)
    keywords: list[EvidenceItem] = field(default_factory=list)
    research_domains: list[EvidenceItem] = field(default_factory=list)
    datasets: list[EvidenceItem] = field(default_factory=list)
    evaluation_metrics: list[EvidenceItem] = field(default_factory=list)
    years: list[EvidenceItem] = field(default_factory=list)

    def to_dict(self):
        return {
            "technologies": [item.to_dict() for item in self.technologies],
            "methodologies": [item.to_dict() for item in self.methodologies],
            "keywords": [item.to_dict() for item in self.keywords],
            "research_domains": [item.to_dict() for item in self.research_domains],
            "datasets": [item.to_dict() for item in self.datasets],
            "evaluation_metrics": [item.to_dict() for item in self.evaluation_metrics],
            "years": [item.to_dict() for item in self.years]
        }

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return cls()
        return cls(
            technologies=[EvidenceItem.from_dict(x) for x in data.get("technologies", [])],
            methodologies=[EvidenceItem.from_dict(x) for x in data.get("methodologies", [])],
            keywords=[EvidenceItem.from_dict(x) for x in data.get("keywords", [])],
            research_domains=[EvidenceItem.from_dict(x) for x in data.get("research_domains", [])],
            datasets=[EvidenceItem.from_dict(x) for x in data.get("datasets", [])],
            evaluation_metrics=[EvidenceItem.from_dict(x) for x in data.get("evaluation_metrics", [])],
            years=[EvidenceItem.from_dict(x) for x in data.get("years", [])]
        )


@dataclass
class EvidenceMatrix:
    technology_frequency: dict = field(default_factory=dict)
    methodology_frequency: dict = field(default_factory=dict)
    keyword_frequency: dict = field(default_factory=dict)
    domain_frequency: dict = field(default_factory=dict)
    dataset_frequency: dict = field(default_factory=dict)
    evaluation_frequency: dict = field(default_factory=dict)
    year_frequency: dict = field(default_factory=dict)

    def to_dict(self):
        return {
            "technology_frequency": self.technology_frequency,
            "methodology_frequency": self.methodology_frequency,
            "keyword_frequency": self.keyword_frequency,
            "domain_frequency": self.domain_frequency,
            "dataset_frequency": self.dataset_frequency,
            "evaluation_frequency": self.evaluation_frequency,
            "year_frequency": self.year_frequency
        }

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return cls()
        return cls(
            technology_frequency=data.get("technology_frequency", {}),
            methodology_frequency=data.get("methodology_frequency", {}),
            keyword_frequency=data.get("keyword_frequency", {}),
            domain_frequency=data.get("domain_frequency", {}),
            dataset_frequency=data.get("dataset_frequency", {}),
            evaluation_frequency=data.get("evaluation_frequency", {}),
            year_frequency=data.get("year_frequency", {})
        )

    def top_technologies(self, limit: int = 5):
        return sorted(self.technology_frequency.items(), key=lambda item: item[1], reverse=True)[:limit]

    def top_methodologies(self, limit: int = 5):
        return sorted(self.methodology_frequency.items(), key=lambda item: item[1], reverse=True)[:limit]

    def top_domains(self, limit: int = 5):
        return sorted(self.domain_frequency.items(), key=lambda item: item[1], reverse=True)[:limit]

    def top_datasets(self, limit: int = 5):
        return sorted(self.dataset_frequency.items(), key=lambda item: item[1], reverse=True)[:limit]

    def latest_year(self):
        if not self.year_frequency:
            return None
        years = []
        for year in self.year_frequency:
            try:
                years.append(int(year))
            except ValueError:
                continue
        return max(years) if years else None
