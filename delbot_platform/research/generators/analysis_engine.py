from collections import Counter
from delbot_platform.research.models.research_models import (
    ResearchContext, ResearchProfile, TrendAnalysis, GapAnalysis,
    NoveltyAnalysis, CompetencyAnalysis, CompetencyItem, ProdiAnalysis
)
from delbot_platform.research.utils.evidence_extractor import extract_evidence
from delbot_platform.research.utils.evidence_matrix import build_evidence_matrix
from delbot_platform.research.utils.trend_engine import build_research_trends
from delbot_platform.research.utils.novelty_scorer import calculate_novelty_score
from delbot_platform.research.gap.gap_detector import detect_research_gaps

# =====================================
# COMPETENCY & PRODI DATA MAPPINGS
# =====================================
COMPETENCY_MAPPING = {
    "yolo": ["computer_vision", "object_detection", "deep_learning", "image_processing"],
    "cnn": ["computer_vision", "deep_learning", "image_processing"],
    "resnet": ["computer_vision", "deep_learning"],
    "mobilenet": ["computer_vision", "deep_learning", "edge_ai"],
    "bert": ["natural_language_processing", "transformer_models", "text_classification"],
    "transformer": ["natural_language_processing", "deep_learning", "attention_mechanism"],
    "lstm": ["sequence_modeling", "deep_learning", "natural_language_processing"],
    "gru": ["sequence_modeling", "deep_learning"],
    "svm": ["machine_learning", "classification"],
    "random_forest": ["machine_learning", "classification"],
    "xgboost": ["machine_learning", "classification", "predictive_analytics"],
    "decision_tree": ["machine_learning", "classification"],
    "laravel": ["web_development", "backend_development"],
    "php": ["web_development", "backend_development"],
    "java": ["software_engineering", "application_development"],
    "python": ["software_engineering", "data_processing"],
    "odoo": ["erp", "business_process", "enterprise_system"],
    "dashboard": ["business_intelligence", "data_visualization"],
    "iot": ["internet_of_things", "embedded_system"]
}

PRODI_PROFILES = {
    "informatika": {
        "focus_areas": ["machine_learning", "deep_learning", "computer_vision", "natural_language_processing", "software_engineering"],
        "expected_competencies": ["computer_vision", "deep_learning", "machine_learning", "classification", "text_classification", "object_detection"]
    },
    "sistem_informasi": {
        "focus_areas": ["business_intelligence", "erp", "crm", "enterprise_system", "information_governance"],
        "expected_competencies": ["business_process", "business_intelligence", "data_visualization", "erp"]
    },
    "trpl": {
        "focus_areas": ["software_engineering", "backend_development", "frontend_development", "devops", "software_architecture"],
        "expected_competencies": ["web_development", "backend_development", "software_engineering"]
    },
    "teknologi_informasi": {
        "focus_areas": ["application_development", "database", "cloud", "web_system"],
        "expected_competencies": ["application_development", "web_development", "backend_development"]
    },
    "teknologi_komputer": {
        "focus_areas": ["iot", "embedded_system", "networking", "automation"],
        "expected_competencies": ["internet_of_things", "embedded_system"]
    },
    "teknik_elektro": {
        "focus_areas": ["control_system", "power_system", "instrumentation", "energy"],
        "expected_competencies": ["control_system", "automation"]
    },
    "manajemen_rekayasa": {
        "focus_areas": ["optimization", "supply_chain", "decision_support", "risk_management"],
        "expected_competencies": ["predictive_analytics"]
    },
    "metalurgi": {
        "focus_areas": ["material", "corrosion", "mineral_processing"],
        "expected_competencies": []
    },
    "bioproses": {
        "focus_areas": ["fermentation", "bioreactor", "biomass"],
        "expected_competencies": []
    }
}

# =====================================
# LOGICAL ANALYZERS
# =====================================
def build_competencies_list(evidence: dict) -> list:
    counter = Counter()
    technologies = evidence.get("technologies", [])
    for item in technologies:
        tech_name = item["name"]
        mapped_competencies = COMPETENCY_MAPPING.get(tech_name, [])
        for comp in mapped_competencies:
            counter[comp] += item["count"]
            
    return [
        {"name": name, "count": count}
        for name, count in counter.most_common()
    ]

def calculate_prodi_alignment_profile(domain: str, competencies_list: list) -> dict:
    competency_names = [item["name"] for item in competencies_list]
    alignments = {}
    matched_by_prodi = {}

    for p_name, p_profile in PRODI_PROFILES.items():
        expected = set(p_profile.get("expected_competencies", []))
        matched = [c for c in competency_names if c in expected]
        alignment = 0.0
        if expected:
            alignment = round(len(matched) / len(expected), 2)
        alignments[p_name] = alignment
        matched_by_prodi[p_name] = matched

    sorted_prodis = sorted(alignments.items(), key=lambda x: x[1], reverse=True)
    
    primary_prodi = domain
    if sorted_prodis and sorted_prodis[0][1] > 0:
        primary_prodi = sorted_prodis[0][0]
    elif domain in PRODI_PROFILES:
        primary_prodi = domain
    elif sorted_prodis:
        primary_prodi = sorted_prodis[0][0]

    profile = PRODI_PROFILES.get(primary_prodi, {})
    focus_areas = profile.get("focus_areas", [])
    primary_matched = matched_by_prodi.get(primary_prodi, [])
    primary_alignment = alignments.get(primary_prodi, 0.0)

    return {
        "prodi": primary_prodi,
        "focus_areas": focus_areas,
        "dominant_competencies": competency_names[:10],
        "matched_competencies": primary_matched,
        "research_alignment": primary_alignment,
        "prodi_alignments": alignments
    }

from delbot_platform.research.analysis.evidence_classifier import classify_all_evidences
from delbot_platform.research.analysis.gap_validator import validate_and_synthesize_gaps

# =====================================
# CORE ANALYSIS ENGINE ENTRYPOINT
# =====================================
def run_analysis(context: ResearchContext) -> ResearchContext:
    # 1. Ekstraksi Frekuensi Entitas (Evidence)
    evidence_data = extract_evidence(context.theses)
    context.evidence = evidence_data

    # 1b. Klasifikasi Hubungan Evidence (DIRECT / SUPPORTING / INSPIRATION)
    prodi_filter = context.requested_prodi or getattr(context, "prodi", "")
    classified_evidences = classify_all_evidences(
        query=context.query,
        theses=context.theses,
        query_prodi=prodi_filter
    )
    context.classified_evidences = classified_evidences

    # 1c. Validasi Gap Epistemik & Sintesis Multi-Dokumen (Gap Validator)
    gap_validation = validate_and_synthesize_gaps(
        query=context.query,
        classified_evidences=classified_evidences,
        raw_theses=context.theses,
        query_prodi=prodi_filter
    )
    context.gap_validation = gap_validation

    # 2. Bangun Evidence Matrix
    matrix_data = build_evidence_matrix(evidence_data)
    context.evidence_matrix = matrix_data

    # 3. Hitung Tren Penelitian (TrendAnalysis)
    trends_dict = build_research_trends(matrix_data)
    trend_analysis = TrendAnalysis.from_dict(trends_dict)

    # 4. Deteksi Celah Riset (GapAnalysis)
    gaps_dict = detect_research_gaps(matrix_data)
    # Suntikkan Bab 5 Kalimat Saran Qdrant ke Gap
    try:
        from delbot_platform.research.gap.bab5_extractor import extract_bab5_gaps
        bab5_list = extract_bab5_gaps(context.theses)
        gaps_dict["bab5_gaps"] = bab5_list
    except Exception as e:
        print(f"[ANALYSIS ENGINE ERROR] Failed to fetch Bab 5 gaps: {e}")
    gap_analysis = GapAnalysis.from_dict(gaps_dict)

    # 5. Hitung Skor Keunikan (NoveltyAnalysis)
    novelty_dict = calculate_novelty_score(matrix_data, gaps_dict)
    novelty_analysis = NoveltyAnalysis.from_dict(novelty_dict)

    # 6. Analisis Kompetensi & Prodi Alignment (Competency & ProdiAnalysis)
    comp_list = build_competencies_list(evidence_data)
    competency_items = [CompetencyItem(name=x["name"], count=x["count"]) for x in comp_list]
    dominant_comp = comp_list[0]["name"] if comp_list else ""
    competency_analysis = CompetencyAnalysis(
        competencies=competency_items,
        total_competencies=len(competency_items),
        dominant_competency=dominant_comp
    )

    domain_slug = context.final_domain.get("domain", "")
    prodi_data = calculate_prodi_alignment_profile(domain_slug, comp_list)
    prodi_analysis = ProdiAnalysis.from_dict(prodi_data)

    # 7. Bentuk Research Profile Terpadu
    context.research_profile = ResearchProfile(
        trend=trend_analysis,
        gap=gap_analysis,
        novelty=novelty_analysis,
        competency=competency_analysis,
        prodi=prodi_analysis
    )
    return context
