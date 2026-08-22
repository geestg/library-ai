from __future__ import annotations

from typing import List, Dict, Any
from app.services.research.analysis.topic_clusterer import cluster_theses_by_topic
from app.services.research.analysis.multi_doc_synthesizer import synthesize_clusters, build_synthesis_prompt_section


def validate_and_synthesize_gaps(
    query: str,
    classified_evidences: List[Dict[str, Any]],
    raw_theses: List[Dict[str, Any]] = None,
    query_prodi: str = ""
) -> Dict[str, Any]:
    """
    Melakukan validasi epistemik Research Gap dan menyusun arahan sintesis multi-dokumen
    berbasis klasterisasi tema 2-5 paper per ide:
    - Level A (Strong): >= 2 penelitian relevan dengan >= 1 DIRECT evidence -> Multi-Document Synthesis.
    - Level B (Moderate): >= 2 penelitian relevan (DIRECT + SUPPORTING) -> Corpus Synthesis.
    - Level C (Explicit Single Study): 1 penelitian dengan limitasi/future work spesifik -> Single-Study Gap.
    - Level D (Weak): 1 penelitian yang hanya kebetulan tidak menggunakan metode tertentu -> Ditolak sebagai gap.
    - Level E (Exploratory / Greenfield): Bukti retrieval tidak cukup -> Peluang eksploratif tanpa gap semu.
    """
    if not classified_evidences:
        return {
            "overall_status": "GREENFIELD_EXPLORATORY",
            "epistemic_level": "Level E (Exploratory / Greenfield)",
            "direct_count": 0,
            "supporting_count": 0,
            "inspiration_count": 0,
            "synthesized_clusters": [],
            "gap_strategy_directives": [
                "Repositori IT Del yang berhasil ditemukan belum memuat penelitian terdahulu yang relevan secara langsung dengan topik ini.",
                "Seluruh 5 ide skripsi WAJIB diposisikan sebagai 'Peluang Penelitian Eksploratif (Greenfield Opportunity)' berbasis kurikulum keilmuan prodi.",
                "DILARANG mengarang sitasi lokal palsu atau mengklaim ketiadaan metode sebagai research gap institusional."
            ],
            "prompt_guidance": (
                "STATUS EVIDENCE: GREENFIELD EXPLORATORY (0 Direct Evidence).\n"
                "Instruksi Khusus Wording Research Gap:\n"
                "- Pada bagian Research Gap di setiap ide, tuliskan secara jujur:\n"
                "  'Repositori IT Del yang berhasil ditemukan belum memberikan bukti yang cukup untuk menyimpulkan gap spesifik pada topik ini. Karena itu, ide ini diposisikan sebagai peluang penelitian eksploratif yang dikembangkan dari tren [Metode SOTA] untuk memecahkan [Problem]...'\n"
                "- DILARANG menulis bahwa 'penelitian di IT Del belum pernah ada' atau mengarang sitasi fiktif."
            )
        }

    direct_evidences = [e for e in classified_evidences if e.get("category") == "DIRECT"]
    supporting_evidences = [e for e in classified_evidences if e.get("category") == "SUPPORTING"]
    inspiration_evidences = [e for e in classified_evidences if e.get("category") == "INSPIRATION"]

    num_direct = len(direct_evidences)
    num_supporting = len(supporting_evidences)
    num_inspiration = len(inspiration_evidences)

    directives = []

    # Penentuan Epistemic Level Global
    if num_direct >= 1 and (num_direct + num_supporting) >= 2:
        epistemic_level = "Level A (Strong Multi-Document Synthesis)"
        directives.append("Ditemukan 2+ dokumen evidence relevan (dengan setidaknya 1 DIRECT evidence).")
        directives.append("Ide 1 dan Ide 2 WAJIB dibangun dari SINTESIS MULTI-DOKUMEN, membandingkan problem, metode, dan batasan dari paper-paper tersebut.")
    elif (num_direct + num_supporting) >= 2:
        epistemic_level = "Level B (Moderate Synthesis Gap)"
        directives.append("Ditemukan kelompok evidence pendukung (SUPPORTING/DIRECT).")
        directives.append("Gunakan formulasi gap berbasis sintesis korpus lokal dengan kehati-hatian akademik.")
    elif num_direct == 1:
        epistemic_level = "Level C (Explicit Single Study Limitation)"
        directives.append(f"Hanya ditemukan 1 DIRECT evidence: '{direct_evidences[0].get('title')}'.")
        directives.append("Formulasikan gap sebagai 'Paper-Specific Limitation' dari penelitian tersebut, bukan generalisasi korpus.")
    else:
        epistemic_level = "Level E (Exploratory / Greenfield)"
        directives.append("Seluruh dokumen retrieval berstatus INSPIRATION (hanya metode yang mirip, domain berbeda).")
        directives.append("Ide mutakhir (misal VLM, Federated Learning, Microservices) WAJIB diposisikan sebagai PELUANG EKSPLORATIF.")

    # Topic Clustering & Multi-Document Synthesis
    theses_for_clustering = raw_theses or []
    clusters = cluster_theses_by_topic(theses_for_clustering, query=query, max_clusters=5)
    synthesized_clusters = synthesize_clusters(clusters, classified_evidences, query=query)
    synthesis_prompt_section = build_synthesis_prompt_section(synthesized_clusters)

    # Deteksi Metode Eksisting pada Evidence untuk Gap Komparasi
    all_detected_methods = set()
    for e in classified_evidences:
        all_detected_methods.update(e.get("detected_methods", []))

    method_acknowledgments = []
    if "xgboost" in all_detected_methods or "svm" in all_detected_methods:
        method_acknowledgments.append(
            "- Evidence memuat penelitian yang sudah menggunakan SVM/XGBoost. Jika mengusulkan model tree-based/komparasi, "
            "AKUI bahwa metode tersebut telah diteliti pada domain sebelumnya (misal backorder), lalu bangun gap berupa komparasi terukur pada domain/fitur baru."
        )

    # Susun Prompt Guidance untuk LLM Master Prompt
    evidence_breakdown_text = []
    for idx, e in enumerate(classified_evidences, start=1):
        evidence_breakdown_text.append(
            f"[{idx}] {e.get('author')} ({e.get('year')}) - \"{e.get('title')}\" [{e.get('prodi')}]\n"
            f"    Status Hubungan: [{e.get('category')}] | {e.get('justification')}"
        )

    prompt_guidance = f"""
==================================================
EVIDENCE CLASSIFICATION & MULTI-DOCUMENT SYNTHESIS:
==================================================
Tingkat Kekuatan Bukti Global: {epistemic_level}
Statistik Evidence: {num_direct} DIRECT, {num_supporting} SUPPORTING, {num_inspiration} INSPIRATION

DAFTAR EVIDENCE TERKLASIFIKASI:
{chr(10).join(evidence_breakdown_text)}

{synthesis_prompt_section}

ATURAN FORMULASI GAP BERDASARKAN HASIL VALIDASI:
1. SINTESIS MULTI-DOKUMEN (MULTI-DOCUMENT SYNTHESIS):
   - Jika Ide didukung Klaster Multi-Dokumen (>= 2 paper):
     WAJIB sebutkan sintesis dari seluruh paper pendukungnya: 'Berdasarkan kelompok penelitian terkait di repositori IT Del ([Penulis 1] [X], [Penulis 2] [Y], dan [Penulis 3] [Z]), pendekatan sebelumnya telah mengeksplorasi [metode/fokus lama], namun masih terbatas pada [pola limitasi bersama]. Belum ditemukan pada penelitian relevan yang dianalisis evaluasi pendekatan [metode baru SOTA] pada [kasus/domain]...'
   - Jika Ide didukung 1 Direct Paper (Single Study):
     Batasi klaim hanya pada paper tersebut: 'Penelitian [Penulis, Tahun] [X] berfokus pada [aspek], namun pada penelitian tersebut masih memiliki keterbatasan pada [limitasi/future work], sehingga terbuka peluang pengembangan berupa [solusi baru]...'
   - Jika Ide berstatus INSPIRATION / Greenfield (Peluang Eksploratif):
     DILARANG MEMAKSAKAN GAP PALSU! Formulasikan secara jujur:
     'Repositori IT Del yang berhasil ditemukan belum memberikan bukti yang cukup untuk menyimpulkan gap spesifik pada topik ini. Karena itu, ide ini diposisikan sebagai peluang penelitian eksploratif yang dikembangkan dari tren [Metode SOTA] untuk memecahkan [Problem]...'

2. ATURAN INTEGRASI METODE EKSISTING:
   {chr(10).join(method_acknowledgments) if method_acknowledgments else "- Bangun keterbaruan yang proporsional terhadap metode yang ditemukan."}

3. ANTI-ASUMSI FAKTUAL IT DEL:
   - DILARANG menyatakan kondisi faktual institusi yang tidak didukung data (misal: jangan menulis 'Sistem IT Del masih monolitik' atau 'banyak mahasiswa Del bermasalah'). Gunakan latar belakang problem ilmiah umum yang relevan.

4. ELIMINASI KATA 'MELOMPAT':
   - Gunakan kata akademik elegan: 'memperluas pendekatan...', 'mengembangkan pendekatan...', 'menguji alternatif metode baru...'
"""

    return {
        "overall_status": "VALIDATED",
        "epistemic_level": epistemic_level,
        "direct_count": num_direct,
        "supporting_count": num_supporting,
        "inspiration_count": num_inspiration,
        "classified_evidences": classified_evidences,
        "synthesized_clusters": synthesized_clusters,
        "gap_strategy_directives": directives,
        "prompt_guidance": prompt_guidance.strip()
    }
