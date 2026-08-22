from __future__ import annotations

import re
from typing import List, Dict, Any


def classify_evidence_relationship(query: str, thesis: Dict[str, Any], query_prodi: str = "") -> Dict[str, Any]:
    """
    Mengklasifikasikan hubungan sebuah karya ilmiah (evidence) terhadap kueri pengguna:
    - DIRECT: Domain dan problem yang diteliti sama atau sangat dekat dengan topik target.
    - SUPPORTING: Domain atau problem terkait/infrastruktur pendukung, namun fokus kasusnya berbeda.
    - INSPIRATION: Metode/teknologi mirip, namun domain aplikasi berbeda jauh (misal: cuaca/backorder untuk topik akademik).
    """
    q_lower = (query or "").lower()
    title = (thesis.get("title") or thesis.get("judul") or "").lower()
    abstract = (thesis.get("abstract") or thesis.get("deskripsi") or "").lower()
    thesis_prodi = (thesis.get("prodi") or "").lower()
    text_corpus = f"{title} {abstract}"

    # Ekstraksi kata kunci domain & metode dari query
    generic_stop = {
        "saya", "mau", "cari", "ide", "skripsi", "prodi", "tentang", "untuk",
        "dengan", "dan", "atau", "yang", "pada", "di", "sistem", "berbasis",
        "tugas", "akhir", "rekomendasi", "berikan", "del", "it", "institut",
        "teknologi", "analisis", "penerapan", "implementasi", "pengembangan",
        "studi", "evaluasi", "rancang", "bangun", "penelitian"
    }
    q_tokens = [w for w in re.findall(r'\b[a-zA-Z]{3,}\b', q_lower) if w not in generic_stop]

    # Ekstraksi metode populer
    known_methods = [
        "svm", "xgboost", "lightgbm", "random forest", "naive bayes", "decision tree",
        "cnn", "yolo", "resnet", "mobilenet", "transformer", "bert", "indobert",
        "lstm", "gru", "clustering", "k-means", "hierarchical", "apriori", "fp-growth",
        "genetic algorithm", "aco", "pso", "fuzzy", "pid", "blockchain", "smart contract",
        "microservices", "soa", "rest api", "federated learning", "vlm", "diffusion"
    ]
    query_methods = [m for m in known_methods if m in q_lower]
    thesis_methods = [m for m in known_methods if m in text_corpus]

    # Cek overlap kata kunci substantif
    matched_q_tokens = [tok for tok in q_tokens if tok in text_corpus]
    domain_overlap_ratio = len(matched_q_tokens) / max(len(q_tokens), 1)

    # Identifikasi domain spesifik pada tesis vs query
    domain_clusters = {
        "academic_student": ["mahasiswa", "skripsi", "tugas akhir", "kelulusan", "akademik", "jadwal", "matakuliah", "sia", "dosen", "asrama", "kantin"],
        "tourism_culture": ["wisata", "toba", "hotel", "tenun", "ulos", "batak", "aksara"],
        "weather_iot": ["cuaca", "suhu", "kelembapan", "sensor", "arduino", "esp32", "iot", "raspberry"],
        "security_network": ["keamanan", "malware", "intrusi", "ids", "firewall", "blockchain", "enkripsi", "rsa", "lsb"],
        "bioprocess_waste": ["limbah", "bioreaktor", "fermentasi", "mikroba", "biomassa", "cod", "bod", "abr", "mbbr"],
        "supply_chain_mgmt": ["rantai pasok", "supply chain", "logistik", "inventori", "gudang", "distribusi", "kopi", "karet"]
    }

    q_matched_domains = [d_name for d_name, kws in domain_clusters.items() if any(kw in q_lower for kw in kws)]
    t_matched_domains = [d_name for d_name, kws in domain_clusters.items() if any(kw in text_corpus for kw in kws)]

    shared_domains = set(q_matched_domains).intersection(set(t_matched_domains))
    shared_methods = set(query_methods).intersection(set(thesis_methods))

    # Logika Klasifikasi
    if shared_domains and (domain_overlap_ratio >= 0.4 or len(matched_q_tokens) >= 2):
        category = "DIRECT"
        justification = f"Domain dan masalah penelitian selaras erat ({', '.join(shared_domains)}), dengan kata kunci yang cocok: {', '.join(matched_q_tokens[:3])}."
    elif shared_domains or (query_prodi and query_prodi.lower() in thesis_prodi and domain_overlap_ratio >= 0.2):
        category = "SUPPORTING"
        justification = f"Mendukung konteks ekosistem/domain serumpun ({', '.join(t_matched_domains or [thesis_prodi])}), namun fokus permasalahan spesifik berbeda."
    elif shared_methods or thesis_methods:
        category = "INSPIRATION"
        found_m = shared_methods or thesis_methods
        justification = f"Hanya metode/teknologi yang relevan ({', '.join(list(found_m)[:2])}), namun domain penelitian berbeda ({', '.join(t_matched_domains or ['Umum'])})."
    else:
        if domain_overlap_ratio > 0:
            category = "SUPPORTING"
            justification = f"Memiliki irisan kata kunci pendukung ({', '.join(matched_q_tokens[:2])})."
        else:
            category = "INSPIRATION"
            justification = "Relevan secara metodologis umum pada korpus repositori IT Del."

    return {
        "title": thesis.get("title") or thesis.get("judul") or "Skripsi IT Del",
        "author": thesis.get("author") or thesis.get("penulis") or "-",
        "year": thesis.get("year") or "-",
        "prodi": thesis.get("prodi") or "-",
        "category": category,
        "justification": justification,
        "detected_methods": list(thesis_methods),
        "detected_domains": list(t_matched_domains),
        "abstract_snippet": (thesis.get("abstract") or "")[:250]
    }


def classify_all_evidences(query: str, theses: List[Dict[str, Any]], query_prodi: str = "") -> List[Dict[str, Any]]:
    """
    Mengklasifikasikan seluruh daftar evidence skripsi hasil retrieval.
    """
    classified = []
    for t in theses:
        classified.append(classify_evidence_relationship(query, t, query_prodi=query_prodi))
    return classified
