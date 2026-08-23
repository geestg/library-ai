from __future__ import annotations

from delbot_platform.research.models.research_models import EvidenceMatrix
from delbot_platform.research.gap.gap_analyzers import (
    detect_dominant_topics, detect_emerging_topics, detect_rare_topics,
    detect_method_gap, detect_dataset_gap, detect_temporal_gap,
    detect_evaluation_gap, detect_novelty_opportunities, calculate_gap_score
)

def detect_research_gaps(evidence_matrix) -> dict:
    """
    Master entrypoint pendeteksian Research Gap & Kebaruan (Novelty)
    berdasarkan matriks bukti 41.370 chunk skripsi IT Del.
    """
    if isinstance(evidence_matrix, dict):
        evidence_matrix = EvidenceMatrix.from_dict(evidence_matrix)
        
    tech_freq = evidence_matrix.technology_frequency
    method_freq = evidence_matrix.methodology_frequency
    domain_freq = evidence_matrix.domain_frequency
    dataset_freq = evidence_matrix.dataset_frequency
    eval_freq = evidence_matrix.evaluation_frequency
    year_freq = evidence_matrix.year_frequency
    
    dominant_topics = detect_dominant_topics(tech_freq, method_freq, domain_freq)
    emerging_topics = detect_emerging_topics(tech_freq, method_freq, domain_freq)
    rare_topics = detect_rare_topics(tech_freq, method_freq, domain_freq)
    
    method_gap = detect_method_gap(method_freq)
    dataset_gap = detect_dataset_gap(dataset_freq)
    temporal_gap = detect_temporal_gap(year_freq)
    evaluation_gap = detect_evaluation_gap(eval_freq)
    
    novelty_opportunities = detect_novelty_opportunities(rare_topics, emerging_topics, dataset_freq)
    gap_score = calculate_gap_score(method_gap, dataset_gap, temporal_gap, evaluation_gap)
    
    print(f"[CONSOLIDATED GAP DETECTOR] Detected Gap Score: {gap_score}")
    
    return {
        "dominant_topics": dominant_topics,
        "emerging_topics": emerging_topics,
        "rare_topics": rare_topics,
        "method_gap": method_gap,
        "dataset_gap": dataset_gap,
        "temporal_gap": temporal_gap,
        "evaluation_gap": evaluation_gap,
        "novelty_opportunities": novelty_opportunities,
        "gap_score": gap_score
    }