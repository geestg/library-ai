from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class TrendAnalysis:
    top_technologies: list = field(default_factory=list)
    top_methods: list = field(default_factory=list)
    top_datasets: list = field(default_factory=list)
    emerging_topics: list = field(default_factory=list)
    research_trends: list = field(default_factory=list)

    def to_dict(self):
        return {
            "top_technologies": self.top_technologies,
            "top_methods": self.top_methods,
            "top_datasets": self.top_datasets,
            "emerging_topics": self.emerging_topics,
            "research_trends": self.research_trends
        }

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return cls()
        return cls(
            top_technologies=data.get("top_technologies", []),
            top_methods=data.get("top_methods", []),
            top_datasets=data.get("top_datasets", []),
            emerging_topics=data.get("emerging_topics", []),
            research_trends=data.get("research_trends", [])
        )


@dataclass
class GapAnalysis:
    dominant_topics: list = field(default_factory=list)
    emerging_topics: list = field(default_factory=list)
    rare_topics: list = field(default_factory=list)
    method_gap: list = field(default_factory=list)
    dataset_gap: list = field(default_factory=list)
    temporal_gap: list = field(default_factory=list)
    evaluation_gap: list = field(default_factory=list)
    novelty_opportunities: list = field(default_factory=list)
    bab5_gaps: list = field(default_factory=list)
    gap_score: int = 0

    def to_dict(self):
        return {
            "dominant_topics": self.dominant_topics,
            "emerging_topics": self.emerging_topics,
            "rare_topics": self.rare_topics,
            "method_gap": self.method_gap,
            "dataset_gap": self.dataset_gap,
            "temporal_gap": self.temporal_gap,
            "evaluation_gap": self.evaluation_gap,
            "novelty_opportunities": self.novelty_opportunities,
            "bab5_gaps": self.bab5_gaps,
            "gap_score": self.gap_score
        }

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return cls()
        return cls(
            dominant_topics=data.get("dominant_topics", []),
            emerging_topics=data.get("emerging_topics", []),
            rare_topics=data.get("rare_topics", []),
            method_gap=data.get("method_gap", []),
            dataset_gap=data.get("dataset_gap", []),
            temporal_gap=data.get("temporal_gap", []),
            evaluation_gap=data.get("evaluation_gap", []),
            novelty_opportunities=data.get("novelty_opportunities", []),
            bab5_gaps=data.get("bab5_gaps", []),
            gap_score=data.get("gap_score", 0)
        )


@dataclass
class NoveltyAnalysis:
    novelty_score: float = 0.0
    novelty_level: str = "LOW"
    reasons: list = field(default_factory=list)
    technology_score: float = 0.0
    dataset_score: float = 0.0
    methodology_score: float = 0.0
    evaluation_score: float = 0.0
    temporal_score: float = 0.0
    domain_score: float = 0.0

    def to_dict(self):
        return {
            "novelty_score": self.novelty_score,
            "novelty_level": self.novelty_level,
            "reasons": self.reasons,
            "technology_score": self.technology_score,
            "dataset_score": self.dataset_score,
            "methodology_score": self.methodology_score,
            "evaluation_score": self.evaluation_score,
            "temporal_score": self.temporal_score,
            "domain_score": self.domain_score
        }

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return cls()
        return cls(
            novelty_score=data.get("novelty_score", 0.0),
            novelty_level=data.get("novelty_level", "LOW"),
            reasons=data.get("reasons", []),
            technology_score=data.get("technology_score", 0.0),
            dataset_score=data.get("dataset_score", 0.0),
            methodology_score=data.get("methodology_score", 0.0),
            evaluation_score=data.get("evaluation_score", 0.0),
            temporal_score=data.get("temporal_score", 0.0),
            domain_score=data.get("domain_score", 0.0)
        )


@dataclass
class ProdiAnalysis:
    prodi: str = ""
    focus_areas: list = field(default_factory=list)
    dominant_competencies: list = field(default_factory=list)
    matched_competencies: list = field(default_factory=list)
    research_alignment: float = 0.0
    prodi_alignments: dict = field(default_factory=dict)

    def to_dict(self):
        return {
            "prodi": self.prodi,
            "focus_areas": self.focus_areas,
            "dominant_competencies": self.dominant_competencies,
            "matched_competencies": self.matched_competencies,
            "research_alignment": self.research_alignment,
            "prodi_alignments": self.prodi_alignments
        }

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return cls()
        return cls(
            prodi=data.get("prodi", ""),
            focus_areas=data.get("focus_areas", []),
            dominant_competencies=data.get("dominant_competencies", []),
            matched_competencies=data.get("matched_competencies", []),
            research_alignment=data.get("research_alignment", 0.0),
            prodi_alignments=data.get("prodi_alignments", {})
        )


@dataclass
class CompetencyItem:
    name: str
    count: int = 0
    confidence: float = 0.0
    source: str = "evidence"

    def to_dict(self):
        return {
            "name": self.name,
            "count": self.count,
            "confidence": self.confidence,
            "source": self.source
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data.get("name", ""),
            count=data.get("count", 0),
            confidence=data.get("confidence", 0.0),
            source=data.get("source", "evidence")
        )


@dataclass
class CompetencyAnalysis:
    competencies: list[CompetencyItem] = field(default_factory=list)
    total_competencies: int = 0
    dominant_competency: str = ""

    def to_dict(self):
        return {
            "competencies": [c.to_dict() for c in self.competencies],
            "total_competencies": self.total_competencies,
            "dominant_competency": self.dominant_competency
        }

    @classmethod
    def from_dict(cls, data: dict):
        competencies = [CompetencyItem.from_dict(item) for item in data.get("competencies", [])]
        return cls(
            competencies=competencies,
            total_competencies=data.get("total_competencies", len(competencies)),
            dominant_competency=data.get("dominant_competency", "")
        )


@dataclass
class ResearchProfile:
    trend: TrendAnalysis = field(default_factory=TrendAnalysis)
    gap: GapAnalysis = field(default_factory=GapAnalysis)
    novelty: NoveltyAnalysis = field(default_factory=NoveltyAnalysis)
    competency: CompetencyAnalysis = field(default_factory=CompetencyAnalysis)
    prodi: ProdiAnalysis = field(default_factory=ProdiAnalysis)

    def to_dict(self):
        return {
            "trend": self.trend.to_dict(),
            "gap": self.gap.to_dict(),
            "novelty": self.novelty.to_dict(),
            "competency": self.competency.to_dict(),
            "prodi": self.prodi.to_dict()
        }

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return cls()
        return cls(
            trend=TrendAnalysis.from_dict(data.get("trend", {})),
            gap=GapAnalysis.from_dict(data.get("gap", {})),
            novelty=NoveltyAnalysis.from_dict(data.get("novelty", {})),
            competency=CompetencyAnalysis.from_dict(data.get("competency", {})),
            prodi=ProdiAnalysis.from_dict(data.get("prodi", {}))
        )
