from __future__ import annotations

import re
from delbot_platform.ai.llm.model_gateway import gateway
from delbot_platform.research.generators.thesis_prompts import (
    build_thesis_ideas_prompt, build_concise_thesis_ideas_prompt
)
from delbot_platform.research.analysis.topic_clusterer import cluster_theses_by_topic
from delbot_platform.research.analysis.multi_doc_synthesizer import (
    synthesize_clusters, build_synthesis_prompt_section
)
from delbot_platform.research.search_engine import is_contextual_followup
from delbot_platform.research.models.research_models import ResearchContext


def validate_thesis_ideas_output(ideas: str, is_concise: bool = False) -> tuple[bool, list[str]]:
    issues = []
    if not ideas or not ideas.strip():
        issues.append("Response kosong atau tidak berisi teks ide skripsi.")
        return False, issues

    normalized = ideas.strip()
    idea_numbers = re.findall(r"(?mi)^\s*#{1,3}\s*Ide\s*([1-9])\b", normalized)
    unique_numbers = sorted(set(idea_numbers), key=lambda x: int(x))

    if len(unique_numbers) < 5:
        issues.append(f"Hanya terdeteksi {len(unique_numbers)} ide berlabel 'Ide 1' sampai 'Ide 5'.")

    if not is_concise:
        if not re.search(r"\b(novelty|kebaruan|kontribusi|inovasi|baru)\b", normalized.lower()):
            issues.append("Tidak ditemukan kata kunci novelty atau kontribusi eksplisit dalam output.")

        if not re.search(r"\b(research gap|celah riset|keterbatasan studi|batasan penelitian|kekurangan penelitian)\b", normalized.lower()):
            issues.append("Ringkasan analisis belum menyebutkan research gap secara eksplisit.")

    if re.search(r"\b(rekomendasi buku|perpustakaan|lokasi buku|koleksi buku)\b", normalized.lower()):
        issues.append("Output mengandung istilah layanan perpustakaan yang tidak relevan untuk ide skripsi.")

    return len(issues) == 0, issues


def sanitize_and_enhance_ideas(ideas: str) -> str:
    if not ideas:
        return ideas

    placeholder_patterns = [
        r"\[Isi Judul[^\]]*\]",
        r"\[Judul Spesifik[^\]]*\]",
        r"\[Pengembangan Baru[^\]]*\]",
        r"\[Isi Latar Belakang[^\]]*\]",
        r"\[Isi Solusi[^\]]*\]",
        r"\[Penjelasan singkat kebaruan[^\]]*\]",
        r"\[Penulis\]",
        r"\[Tahun\]",
        r"\[Data/Parameter[^\]]*\]",
        r"\[Maksimal [^\]]*\]",
        r"\[Sebutkan spesifik[^\]]*\]",
    ]
    for pattern in placeholder_patterns:
        ideas = re.sub(pattern, "", ideas, flags=re.IGNORECASE)

    # Strip leftover placeholder title headers
    ideas = re.sub(r"(?mi)^\s*###?\s*Judul\s+Ide\s+Baru[^\n]*\n", "", ideas)
    ideas = re.sub(r"(?mi)^###\s*\[\s*(.*?)\s*\]\s*$", r"### \1", ideas)

    # Clean duplicate dataset phrasing (e.g. 'Dataset & Evaluasi: Data yang disarankan:')
    ideas = re.sub(r"(?mi)(?:Dataset & Evaluasi|Saran Data|Dataset)[:\s*]+(?:Data(?:set)?\s+yang\s+disarankan:?\s*)?", "Dataset & Evaluasi: ", ideas)

    # Clean and separate section headers with clean standard bullets (no cluttered emojis)
    ideas = re.sub(r"(?mi)^\s*(?:#{1,3}\s*)?(?:📌\s*)?(?:\*{0,2})Problem(?:\*{0,2}):?\s*(\S[^\n\r]*)", r"\n\n* **Problem:** \1", ideas)
    ideas = re.sub(r"(?mi)^\s*(?:#{1,3}\s*)?(?:🔍\s*)?(?:\*{0,2})Research Gap(?:\*{0,2}):?\s*(\S[^\n\r]*)", r"\n\n* **Research Gap:** \1", ideas)
    ideas = re.sub(r"(?mi)^\s*(?:#{1,3}\s*)?(?:🚀\s*)?(?:\*{0,2})Solusi & Kebaruan(?:\*{0,2}):?\s*(\S[^\n\r]*)", r"\n\n* **Solusi & Kebaruan:** \1", ideas)
    ideas = re.sub(r"(?mi)^\s*(?:#{1,3}\s*)?(?:📊\s*)?(?:\*{0,2})Dataset & Evaluasi(?:\*{0,2}):?\s*(?:Data(?:set)?\s+yang\s+disarankan:?\s*)?(\S[^\n\r]*)", r"\n\n* **Dataset & Evaluasi:** \1", ideas)

    # Format Idea Headers cleanly without emoji
    ideas = re.sub(r"(?mi)^\s*(?:#{1,3}\s*)?(?:💡\s*)?Ide\s*([1-9])\s*:\s*", r"\n\n### Ide \1: ", ideas)

    # Ensure difficulty badge has proper formatting
    ideas = re.sub(r"(?mi)^\s*(?:💡\s*|🎯\s*)?(?:Tingkat\s*)?Kesulitan\s*:\s*([^\n\r]+)", r"\n\n* **Tingkat Kesulitan:** `\1`\n\n---", ideas)

    # 2. Strip leftover Rating and Alasan Menarik sections if LLM outputted them
    ideas = re.sub(r"(?mi)^\s*###?\s*(?:📊\s*)?(?:Evaluasi|Rating|Novelty\s*Score|Alasan\s*Menarik)[^\n]*\n.*?(?=\n\s*#{1,3}\s*Ide|\n\s*---\s*|\n\s*💡|\Z)", "", ideas, flags=re.DOTALL)
    ideas = re.sub(r"(?m)^\s*(?:Rating|Novelty|Difficulty|Dataset Availability|Alasan Menarik):\s*.*$", "", ideas)

    ideas = re.sub(r"\bmelompat dari\b", "memperluas pendekatan", ideas, flags=re.IGNORECASE)
    ideas = re.sub(r"\bmelompat ke\b", "beralih ke", ideas, flags=re.IGNORECASE)
    ideas = re.sub(r"\btidak ada penelitian\b", "belum ditemukan pada penelitian relevan yang dianalisis", ideas, flags=re.IGNORECASE)
    ideas = re.sub(r"\bbelum ada studi\b", "masih terbatas studi", ideas, flags=re.IGNORECASE)
    ideas = re.sub(r"\bbelum pernah diterapkan\b", "masih jarang diterapkan", ideas, flags=re.IGNORECASE)
    ideas = re.sub(r"\bbelum pernah ada di it del\b", "belum ditemukan pada korpus penelitian IT Del yang ditelaah", ideas, flags=re.IGNORECASE)

    # Auto-sanitize PSO on DL/ML hyperparameter tuning & feature selection
    ideas = re.sub(r"\bPSO-optimized\b", "Optuna-optimized", ideas, flags=re.IGNORECASE)
    ideas = re.sub(r"\bParticle Swarm Optimization \(PSO\)\b", "Bayesian Optimization (Optuna)", ideas, flags=re.IGNORECASE)
    ideas = re.sub(r"\bdeng?an PSO\b", "dengan Optuna (Bayesian Optimization)", ideas, flags=re.IGNORECASE)
    ideas = re.sub(r"\bberbasis PSO\b", "berbasis Optuna (Bayesian Optimization)", ideas, flags=re.IGNORECASE)
    ideas = re.sub(r"\bdan PSO\b", "dan Bayesian Optimization (Optuna)", ideas, flags=re.IGNORECASE)
    ideas = re.sub(r"\bdioptimasi oleh PSO\b", "dioptimasi oleh Optuna (Bayesian Optimization)", ideas, flags=re.IGNORECASE)
    ideas = re.sub(r"\bPSO Convergence Rate\b", "Optimization Convergence Rate", ideas, flags=re.IGNORECASE)
    ideas = re.sub(r"\boptimasi PSO\b", "optimasi Bayesian (Optuna)", ideas, flags=re.IGNORECASE)
    ideas = re.sub(r"\bmetode PSO\b", "metode Optuna (Bayesian Optimization)", ideas, flags=re.IGNORECASE)

    # Auto-sanitize legacy ML (C4.5 / J48) & terminology precision
    ideas = re.sub(r"\bberbasis C4\.5\b", "berbasis LightGBM", ideas, flags=re.IGNORECASE)
    ideas = re.sub(r"\balgoritma C4\.5\b", "algoritma LightGBM", ideas, flags=re.IGNORECASE)
    ideas = re.sub(r"\bkecerdasan emosional\b", "indikator sentimen keterlibatan", ideas, flags=re.IGNORECASE)

    # Auto-correct common dataset hallucinations
    ideas = re.sub(r"ChestX-?ray14?\s*\([^)]*mammogram[^)]*\)", "CBIS-DDSM (Mammogram Dataset)", ideas, flags=re.IGNORECASE)

    # Normalize double horizontal rules and triple newlines
    ideas = re.sub(r"(?:\n\s*---\s*){2,}", "\n\n---", ideas)
    ideas = re.sub(r"\n{3,}", "\n\n", ideas)
    return ideas.strip()


def generate_thesis_ideas(context: ResearchContext) -> ResearchContext:
    """
    Generator 5 Ide Skripsi Multidisiplin IT Del berbobot akademik tinggi.
    """
    profile = context.research_profile

    # 1. Format detail dokumen bukti (theses)
    followup_count = 0
    try:
        from delbot_platform.research.session import session_manager
        _session = session_manager.get_or_create(context.session_id)
        followup_count = getattr(_session, "followup_count", 0)
    except Exception:
        pass

    classified_lookup = {}
    if hasattr(context, "classified_evidences") and context.classified_evidences:
        for idx, ce in enumerate(context.classified_evidences, start=1):
            classified_lookup[idx] = ce

    new_start_idx = (followup_count * 5) + 1 if followup_count > 0 else 1

    # ─────────────────────────────────────────────────────────────────────────
    # PER-IDEA EVIDENCE PIPELINE (Perbaikan A)
    # Fase 1: Cluster kandidat 25 paper menjadi 5 klaster tematik
    # Fase 2: Per-cluster Evidence Rerank (DIRECT > SUPPORTING > INSPIRATION)
    # Fase 3: Pilih ketat 2–4 paper per klaster
    # Fase 4: Tentukan Gap Type (Synthesis / Single-Study / Repository Opportunity)
    # Fase 5: Bangun per_cluster_evidence_str (bukan flat list!)
    # ─────────────────────────────────────────────────────────────────────────
    classified_evidences = getattr(context, "classified_evidences", []) or []
    synthesis_clusters_section = ""
    per_cluster_evidence_str = ""

    if context.theses and not (context.requested_prodi and context.requested_prodi.startswith("bukan_del:")):
        try:
            raw_clusters = cluster_theses_by_topic(
                theses=context.theses,
                query=context.query,
                max_clusters=5
            )
            synthesized = synthesize_clusters(
                clusters=raw_clusters,
                classified_evidences=classified_evidences,
                query=context.query,
                query_prodi=getattr(context, "requested_prodi", "") or ""
            )
            synthesis_clusters_section = build_synthesis_prompt_section(synthesized)
            context.synthesized_clusters = synthesized

            # Bangun per_cluster_evidence_str: setiap klaster tampil dengan paper terpilihnya
            cluster_evidence_blocks = []
            for sc in synthesized:
                c_idx = sc["cluster_index"]
                c_name = sc["cluster_name"]
                selected_theses_in_cluster = sc.get("theses", [])
                block_lines = [f"── KLASTER {c_idx}: {c_name} (untuk Ide {c_idx}) ──"]
                for t in selected_theses_in_cluster:
                    cite_id = t["citation_id"]
                    ce = (classified_evidences[cite_id - 1] if 0 < cite_id <= len(classified_evidences) else {})
                    cat = ce.get("category", "SUPPORTING") if ce else "SUPPORTING"
                    just = ce.get("justification", "") if ce else ""
                    block_lines.append(
                        f"  [{cite_id}] [{cat}] Judul: {t.get('title', '-')}\n"
                        f"      Penulis: {t.get('author', '-')} | Tahun: {t.get('year', '-')}\n"
                        f"      Relevansi: {just}\n"
                        f"      Abstrak: {t.get('abstract', '')[:250]}..."
                    )
                cluster_evidence_blocks.append("\n".join(block_lines))
            per_cluster_evidence_str = "\n\n".join(cluster_evidence_blocks)
            print(f"[THESIS IDEA GENERATOR] Per-cluster evidence built: {len(synthesized)} clusters")
        except Exception as e:
            print(f"[THESIS IDEA GENERATOR] Per-cluster pipeline error: {e}. Falling back to flat theses_str.")
            synthesis_clusters_section = ""

    # Fallback: jika per-cluster pipeline gagal, bangun theses_str flat (fallback aman)
    if not per_cluster_evidence_str:
        classified_lookup = {}
        for idx, ce in enumerate(classified_evidences, start=1):
            classified_lookup[idx] = ce
        theses_details = []
        for idx, t in enumerate(context.theses, start=1):
            ce_info = classified_lookup.get(idx, {})
            category_tag = f" [{ce_info.get('category', 'SUPPORTING')}]" if ce_info else ""
            justification_line = f"    Relevansi: {ce_info.get('justification', '')}\n" if ce_info.get("justification") else ""
            theses_details.append(
                f"[{idx}]{category_tag} Judul: {t.get('title')}\n"
                f"    Penulis: {t.get('author') or 'Unknown'} | Tahun: {t.get('year') or '-'}\n"
                f"{justification_line}"
                f"    Abstrak: {t.get('abstract') or t.get('chunk') or ''}"
            )
        per_cluster_evidence_str = "\n\n".join(theses_details)

    # 2. Deteksi relevansi data & prodi eksternal
    sliced_theses = context.theses[new_start_idx - 1:] if context.theses else []
    new_theses = sliced_theses if sliced_theses else (context.theses or [])
    has_theses = len(new_theses) > 0
    low_relevance = not has_theses

    non_del_prodi_name = None
    if context.requested_prodi and context.requested_prodi.startswith("bukan_del:"):
        non_del_prodi_name = context.requested_prodi.replace("bukan_del:", "").title()

    relevance_warning = ""
    if non_del_prodi_name:
        relevance_warning = f"""\n⚠️ PERINGATAN PRODI EKSTERNAL ({non_del_prodi_name} tidak ada di IT Del).\nSajikan 5 ide bebas dari literatur umum.\n"""
    elif low_relevance:
        relevance_warning = f"""\n⚠️ PERINGATAN RELEVANSI DATA\nDatabase perpustakaan IT Del tidak memiliki cukup skripsi yang relevan dengan topik "{context.query}".\n"""

    format_klarifikasi = ""
    if non_del_prodi_name:
        clean_name = re.sub(r'^(?:Mahasiswa|Anak|Prodi|Jurusan)\s+', '', non_del_prodi_name, flags=re.IGNORECASE).title()
        format_klarifikasi = f"**Sekadar Informasi:** Saat ini Institut Teknologi Del (IT Del) belum memiliki Program Studi **{clean_name}**. Ide skripsi dirumuskan murni dari kajian literatur umum. 😊\n\n"
    elif not has_theses:
        format_klarifikasi = f"**Catatan Repositori:** Belum ditemukan skripsi terdahulu mengenai topik spesifik ini dalam korpus repositori lokal IT Del yang ditelusuri. 5 ide berikut merupakan usulan eksploratif berbasis konteks keilmuan prodi (bukan hasil sintesis langsung dari skripsi alumni IT Del): 😊\n\n"

    last_research_gap = ""
    try:
        last_research_gap = getattr(_session, "last_research_gap", "")
    except Exception:
        pass

    gap_validation_guidance = getattr(context, "gap_validation", {}).get("prompt_guidance", "")

    # 3. Susun prompt & panggil LLM Gateway
    if is_contextual_followup(context.query) or followup_count > 0:
        print("[THESIS IDEA GENERATOR] Formatting as CONCISE THESIS IDEAS because it is a follow-up query.")
        prompt = build_concise_thesis_ideas_prompt(
            context_query=context.query,
            per_cluster_evidence_str=per_cluster_evidence_str,
            synthesis_clusters_section=synthesis_clusters_section,
            evidence_summary=context.evidence,
            evidence_matrix=context.evidence_matrix,
            trend_dict=profile.trend.to_dict(),
            gap_dict=profile.gap.to_dict(),
            novelty_dict=profile.novelty.to_dict(),
            relevance_warning=relevance_warning,
            format_klarifikasi=format_klarifikasi,
            last_research_gap_text=last_research_gap,
            conversation_history=context.conversation_history,
            gap_validation_report=gap_validation_guidance
        )
    else:
        prompt = build_thesis_ideas_prompt(
            context_query=context.query,
            per_cluster_evidence_str=per_cluster_evidence_str,
            synthesis_clusters_section=synthesis_clusters_section,
            evidence_summary=context.evidence,
            evidence_matrix=context.evidence_matrix,
            trend_dict=profile.trend.to_dict(),
            gap_dict=profile.gap.to_dict(),
            novelty_dict=profile.novelty.to_dict(),
            relevance_warning=relevance_warning,
            format_klarifikasi=format_klarifikasi,
            last_research_gap_text=last_research_gap,
            conversation_history=context.conversation_history,
            gap_validation_report=gap_validation_guidance
        )

    # Guard explicit: pastikan LLM tahu ini harus menjadi ide skripsi, bukan rekomendasi buku
    prompt += "\n\nPERINGATAN: Jawaban harus berupa 5 ide skripsi atau penelitian, bukan rekomendasi buku atau layanan perpustakaan."
    if is_contextual_followup(context.query) or followup_count > 0:
        prompt += f"\n\n⚠️ PENTING: Ini adalah kueri follow-up lanjutan untuk ide tambahan. Hasilkan 5 ide skripsi baru yang berbeda dari sebelumnya, namun tetap 100% KONSISTEN membahas topik riset asli: '{context.query}'. DILARANG keras berganti topik ke Ulos, cuaca, microservices, atau domain lain di luar '{context.query}'!"

    ideas = gateway.generate_response(prompt=prompt)

    # 3.5 Audit hasil ide untuk memastikan novelty dan struktur ide
    validated, issues = validate_thesis_ideas_output(ideas, is_concise=False)
    if not validated:
        audit_prompt = "\n\nPERBAIKAN OUTPUT: Output sebelumnya tidak memenuhi kriteria ide skripsi yang valid. "
        audit_prompt += "Perbaiki agar mencakup 5 ide berlabel 'Ide 1' sampai 'Ide 5', mencantumkan novelty/kontribusi eksplisit, dan menyebutkan research gap. "
        audit_prompt += "Hapus semua referensi perpustakaan, rekomendasi buku, atau layanan yang tidak relevan."
        audit_prompt += "\n\nISSUES:\n- " + "\n- ".join(issues) + "\n\nOUTPUT BARU:\n"

        ideas = gateway.generate_response(prompt=prompt + audit_prompt)

        validated, issues = validate_thesis_ideas_output(ideas, is_concise=False)
        if not validated:
            print(f"[THESIS IDEA AUDIT FAILED] Setelah perbaikan, masih terdapat isu: {issues}")

    final_sources = [] if non_del_prodi_name else context.theses
    final_citations = [] if non_del_prodi_name else context.citations

    context.theses = final_sources
    context.citations = final_citations

    try:
        from delbot_platform.research.session import session_manager
        _session = session_manager.get_or_create(context.session_id)
        _session.all_theses = final_sources
    except Exception:
        pass

    # Post-processing sanitizer: Remove literal brackets placeholders & reframe absolute claims
    ideas = sanitize_and_enhance_ideas(ideas)

    context.analysis = ideas
    context.response = {
        "query": context.query,
        "ideas": ideas,
        "literature_review": ideas,
        "sources": final_sources,
        "citations": final_citations,
        "research_profile": context.research_profile.to_dict() if context.research_profile else {},
        "novelty_score": context.research_profile.novelty.novelty_score if context.research_profile else 0,
        "novelty_level": context.research_profile.novelty.novelty_level if context.research_profile else "LOW",
    }
    return context