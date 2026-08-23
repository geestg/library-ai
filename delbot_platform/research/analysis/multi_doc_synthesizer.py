from __future__ import annotations

from typing import List, Dict, Any


def synthesize_clusters(
    clusters: List[Dict[str, Any]],
    classified_evidences: List[Dict[str, Any]],
    query: str = "",
    query_prodi: str = ""
) -> List[Dict[str, Any]]:
    """
    Melakukan sintesis multi-dokumen lintas paper pada setiap klaster tematik
    dengan alokasi ketat 2-4 paper per ide untuk mencegah penumpukan sitasi masif.

    Jaminan keunikan global: setiap citation_id hanya bisa muncul di SATU klaster.
    query_prodi: slug prodi (misal 'sistem_informasi') untuk framing domain-spesifik.
    """
    if not clusters:
        return []

    # Map classified metadata by citation_id
    classified_map = {}
    for idx, ce in enumerate(classified_evidences, start=1):
        classified_map[idx] = ce

    synthesized_clusters = []
    # Global uniqueness guard: citation_id yang sudah dipakai di klaster sebelumnya
    # tidak boleh dipakai lagi di klaster berikutnya
    global_used_citation_ids: set = set()

    for cluster_idx, cl in enumerate(clusters, start=1):
        raw_theses = cl.get("theses", [])
        cluster_name = cl.get("cluster_name", "Klaster Tematik")

        # Sort theses by priority: DIRECT > SUPPORTING > INSPIRATION
        def get_priority(t):
            c_info = classified_map.get(t["citation_id"], {})
            cat = c_info.get("category", "SUPPORTING")
            if cat == "DIRECT":
                return 1
            elif cat == "SUPPORTING":
                return 2
            return 3

        sorted_theses = sorted(raw_theses, key=get_priority)

        # ALOKASI KETAT: Maksimal 4 paper per ide
        # + UNIQUENESS GUARD: buang paper yang sudah dipakai klaster lain
        selected_theses = []
        for t in sorted_theses:
            if t["citation_id"] not in global_used_citation_ids:
                selected_theses.append(t)
            if len(selected_theses) >= 4:
                break

        # Tandai semua citation_id klaster ini sebagai sudah dipakai
        for t in selected_theses:
            global_used_citation_ids.add(t["citation_id"])

        theses_count = len(selected_theses)

        # Kumpulkan sitasi dan metadata untuk paper terpilih
        citations_str_list = []
        direct_count = 0
        supporting_count = 0
        inspiration_count = 0
        used_methods = set()
        authors_and_years = []

        for t in selected_theses:
            cite_id = t["citation_id"]
            ce = classified_map.get(cite_id, {})
            cat = ce.get("category", "SUPPORTING")
            if cat == "DIRECT":
                direct_count += 1
            elif cat == "SUPPORTING":
                supporting_count += 1
            else:
                inspiration_count += 1

            for m in ce.get("detected_methods", []):
                used_methods.add(m)

            author = t.get("author", "Alumni")
            year = t.get("year", "-")
            authors_and_years.append(f"[{author}, {year}] [{cite_id}]")
            citations_str_list.append(f"[{cite_id}]")

        cites_formatted = ", ".join(authors_and_years)

        # ─────────────────────────────────────────────────────────────────
        # PERBAIKAN BUG 1: Threshold Gap Type yang Tepat
        #
        # SYNTHESIS GAP   → ada ≥1 DIRECT, ATAU ada ≥2 SUPPORTING
        #                   (bukti memadai untuk klaim "kelompok penelitian")
        # SINGLE-STUDY    → tepat 1 DIRECT (dan tanpa SUPPORTING lain), atau
        #                   total paper = 1 (apapun kategorinya)
        # REPO OPPORTUNITY → semua paper hanya INSPIRATION (direct=0, supporting=0)
        # ─────────────────────────────────────────────────────────────────
        has_strong_evidence = (direct_count >= 1) or (supporting_count >= 2)
        is_single_direct_only = (direct_count == 1 and supporting_count == 0)
        all_inspiration = (direct_count == 0 and supporting_count == 0)

        if has_strong_evidence and not is_single_direct_only:
            # Synthesis Gap: ≥2 DIRECT, atau 1 DIRECT + ≥1 SUPPORTING, atau ≥2 SUPPORTING
            evidence_strength = "SYNTHESIS_GAP (Multi-Document Synthesis: ≥1 DIRECT atau ≥2 SUPPORTING)"
            gap_type = "synthesis"
            synthesis_directive = (
                f"SYNTHESIS GAP (HANYA GUNAKAN {len(selected_theses)} SITASI INI: {cites_formatted}).\n"
                f"Wording Wajib: 'Berdasarkan kelompok penelitian terkait di repositori IT Del ({cites_formatted}), "
                f"penelitian terdahulu telah mengeksplorasi [metode lama/fokus], namun masih terbatas pada "
                f"[pola limitasi bersama]. Belum ditemukan pada penelitian relevan yang dianalisis evaluasi "
                f"pendekatan [metode baru]...'\n"
                f"DILARANG KERAS MENAMBAHKAN SITASI DI LUAR KLASTER INI ({', '.join(citations_str_list)})!\n"
                f"DILARANG menggunakan sitasi ini di bagian Solusi & Kebaruan kecuali sudah disebut di Research Gap!"
            )
        elif (direct_count == 1 and supporting_count == 0) or theses_count == 1:
            # Single-Study Gap: tepat 1 paper DIRECT atau hanya 1 paper apapun
            evidence_strength = "SINGLE_STUDY_GAP (Single-Paper Limitation: 1 Paper)"
            gap_type = "single_study"
            anchor = authors_and_years[0] if authors_and_years else "paper repositori"
            synthesis_directive = (
                f"SINGLE-STUDY GAP (HANYA GUNAKAN 1 SITASI INI: {anchor}).\n"
                f"DILARANG sebut 'kelompok penelitian' karena hanya 1 paper DIRECT!\n"
                f"Wording Wajib: 'Berdasarkan keterbatasan penelitian {anchor}, sistem sebelumnya telah... "
                f"Namun, penelitian tersebut belum mengevaluasi...'\n"
                f"DILARANG KERAS MENAMBAHKAN SITASI DARI PAPER LAIN!\n"
                f"DILARANG menggunakan sitasi ini di bagian Solusi & Kebaruan kecuali sudah disebut di Research Gap!"
            )
        else:
            # Repository Opportunity: semua paper hanya INSPIRATION (0 DIRECT, 0–1 SUPPORTING)
            # Gunakan maksimal 2 sitasi INSPIRATION sebagai pijakan
            inspiration_anchors = authors_and_years[:2]
            anchor_str = ", ".join(inspiration_anchors) if inspiration_anchors else "paper repositori terkait"
            evidence_strength = "REPOSITORY_OPPORTUNITY (Inspiration Base: 0 DIRECT, hanya INSPIRATION)"
            gap_type = "repository_opportunity"
            synthesis_directive = (
                f"REPOSITORY OPPORTUNITY — Tidak ada paper DIRECT/SUPPORTING yang cukup kuat.\n"
                f"HANYA BOLEH menggunakan maksimal 2 sitasi INSPIRATION ini sebagai pijakan: {anchor_str}.\n"
                f"Wording Wajib: 'Belum ditemukan penelitian yang secara langsung membahas topik tersebut "
                f"pada dokumen repositori yang dianalisis. Oleh karena itu, ide berikut diposisikan sebagai "
                f"peluang eksploratif berbasis rujukan {anchor_str}...'\n"
                f"DILARANG mengklaim 4 paper sebagai bukti setelah membuka dengan 'Belum ditemukan...'. "
                f"Jika menyebut paper, maksimal 2 sitasi dan hanya sebagai analogi metodologis!\n"
                f"DILARANG KERAS MENAMBAHKAN SITASI DARI PAPER LAIN DI LUAR {anchor_str}!"
            )

        # ─────────────────────────────────────────────────────────────────
        # PRODI-SPECIFIC FRAMING MANDATE
        # Jika prodi terdeteksi, tambahkan arahan domain ke synthesis_directive
        # agar LLM tidak menghasilkan ide dari domain prodi lain
        # ─────────────────────────────────────────────────────────────────
        PRODI_FRAMING = {
            # ── Informatika ──────────────────────────────────────────────
            "informatika": (
                "\n[PRODI IF FRAMING MANDATE] Ide skripsi WAJIB dalam ranah Computer Science murni: "
                "Machine Learning, Deep Learning, Computer Vision, NLP, Software Engineering, "
                "Keamanan Siber, atau Algoritma & Struktur Data. "
                "Boleh memakai dataset lokal/organisasi HANYA sebagai bahan evaluasi, bukan sebagai tujuan utama. "
                "DILARANG menghasilkan ide yang murni bersifat manajerial tanpa kontribusi teknis algoritma!"
            ),
            # ── Sistem Informasi ─────────────────────────────────────────
            "sistem_informasi": (
                "\n[PRODI SI FRAMING MANDATE] Ide skripsi WAJIB dibingkai sebagai solusi "
                "Sistem Informasi yang berorientasi pada nilai organisasi, bukan algoritma murni. "
                "Contoh framing SI yang benar: "
                "Actionable BI Dashboard, Learning Analytics Dashboard, Decision Support System (DSS) berbasis AI, "
                "AI-Powered Process Mining, Evaluasi Adopsi Sistem (TAM/UTAUT), IT Governance (COBIT/ITIL), "
                "atau Enterprise Content Management. "
                "DILARANG menghasilkan ide yang murni membahas tuning algoritma ML/DL tanpa luaran SI organisasional!"
            ),
            # ── TRPL (alias ganda) ───────────────────────────────────────
            "trpl": (
                "\n[PRODI TRPL FRAMING MANDATE] Ide skripsi WAJIB dalam ranah rekayasa perangkat lunak terapan: "
                "Microservices/REST API, Mobile App (Flutter/React Native), CI/CD & DevOps, "
                "Software Testing Otomatis, atau Web App berbasis framework modern. "
                "Luaran wajib berupa sistem/aplikasi yang bisa dijalankan, bukan model ML tanpa antarmuka. "
                "DILARANG menghasilkan ide pure data science tanpa produk software!"
            ),
            "teknologi_rekayasa_perangkat_lunak": (
                "\n[PRODI TRPL FRAMING MANDATE] Ide skripsi WAJIB dalam ranah rekayasa perangkat lunak terapan: "
                "Microservices/REST API, Mobile App (Flutter/React Native), CI/CD & DevOps, "
                "Software Testing Otomatis, atau Web App berbasis framework modern. "
                "Luaran wajib berupa sistem/aplikasi yang bisa dijalankan, bukan model ML tanpa antarmuka. "
                "DILARANG menghasilkan ide pure data science tanpa produk software!"
            ),
            # ── Teknik Elektro ───────────────────────────────────────────
            "teknik_elektro": (
                "\n[PRODI TE FRAMING MANDATE] Ide skripsi WAJIB dalam ranah Teknik Elektro: "
                "Sistem Kendali (PID/fuzzy/MPC), Konversi Energi (PLTS/inverter/konverter), "
                "Proteksi & Distribusi Daya, Embedded Systems (Arduino/ESP32/FPGA), "
                "atau Pemrosesan Sinyal. "
                "DILARANG menghasilkan ide pure software tanpa komponen elektronika/hardware!"
            ),
            # ── Manajemen Rekayasa ───────────────────────────────────────
            "manajemen_rekayasa": (
                "\n[PRODI MR FRAMING MANDATE] Ide skripsi WAJIB dibingkai sebagai solusi Manajemen Rekayasa: "
                "SCM/Logistik, Lean/Six Sigma, Techno-Economic Analysis, Kelayakan Finansial (NPV/IRR/BCR), "
                "PPIC, Ergonomi & K3, atau Operations Research. "
                "DILARANG menghasilkan ide koding software murni atau skripsi mikrokontroler!"
            ),
            # ── Teknik Metalurgi ─────────────────────────────────────────
            "teknik_metalurgi": (
                "\n[PRODI TM FRAMING MANDATE] Ide skripsi WAJIB dalam ranah Teknik Metalurgi: "
                "Karakterisasi material (XRD/SEM/FTIR), Korosi & proteksi, Pengolahan mineral, "
                "Heat treatment & sifat mekanik, atau Metalurgi ekstraksi. "
                "DILARANG membajak ke skripsi software atau bioproses!"
            ),
            # ── Teknologi Bioproses (alias ganda) ────────────────────────
            "teknologi_bioproses": (
                "\n[PRODI BIOPROSES FRAMING MANDATE] Ide skripsi WAJIB berfokus pada substansi biokimia: "
                "kinetika reaksi (Monod/Haldane), konfigurasi bioreaktor (CSTR/ABR/MBBR/MBR), "
                "biodegradasi polutan (COD/BOD/TSS), fermentasi, atau optimasi parameter proses biologis. "
                "DILARANG membajak ke skripsi mikrokontroler hardware murni!"
            ),
            "teknik_bioproproses": (
                "\n[PRODI BIOPROSES FRAMING MANDATE] Ide skripsi WAJIB berfokus pada substansi biokimia: "
                "kinetika reaksi (Monod/Haldane), konfigurasi bioreaktor (CSTR/ABR/MBBR/MBR), "
                "biodegradasi polutan (COD/BOD/TSS), fermentasi, atau optimasi parameter proses biologis. "
                "DILARANG membajak ke skripsi mikrokontroler hardware murni!"
            ),
            # ── Bioteknologi ─────────────────────────────────────────────
            "bioteknologi": (
                "\n[PRODI BIOTEK FRAMING MANDATE] Ide skripsi WAJIB berfokus pada substansi bioteknologi: "
                "rekayasa genetika/DNA/PCR, kultur jaringan/mikropropagasi, bioremediasi, "
                "metabolit sekunder & bioaktivitas, atau bioprospeksi mikroorganisme. "
                "DILARANG membajak ke skripsi software atau hardware elektronika murni!"
            ),
            # ── Teknologi Informasi D3 ───────────────────────────────────
            "teknologi_informasi": (
                "\n[PRODI TI D3 FRAMING MANDATE] Ide skripsi WAJIB dalam ranah Teknologi Informasi terapan: "
                "Jaringan komputer, Keamanan jaringan, Administrasi sistem, "
                "Aplikasi web/mobile ringan, atau Database administration. "
                "Luaran harus bersifat terapan dan langsung dapat diimplementasikan. "
                "DILARANG menghasilkan ide penelitian fundamental tanpa aplikasi nyata!"
            ),
            # ── Teknologi Komputer D3 ────────────────────────────────────
            "teknologi_komputer": (
                "\n[PRODI TK D3 FRAMING MANDATE] Ide skripsi WAJIB dalam ranah Teknologi Komputer terapan: "
                "Embedded systems, Mikrokontroler (Arduino/ESP32/Raspberry Pi), "
                "Otomasi & instrumentasi, Sistem monitoring berbasis IoT, atau Jaringan sensor. "
                "Luaran wajib berupa prototipe hardware/firmware yang dapat didemonstrasikan. "
                "DILARANG menghasilkan ide pure software tanpa komponen hardware!"
            ),
        }

        prodi_framing_str = ""
        if query_prodi:
            prodi_slug = query_prodi.lower().replace(" ", "_").replace("-", "_")
            prodi_framing_str = PRODI_FRAMING.get(prodi_slug, "")

        if prodi_framing_str:
            synthesis_directive += prodi_framing_str

        synthesized_clusters.append({

            "cluster_index": cluster_idx,
            "cluster_name": cluster_name,
            "theses_count": theses_count,
            "citation_ids": [t["citation_id"] for t in selected_theses],
            "citations_formatted": cites_formatted,
            "evidence_strength": evidence_strength,
            "gap_type": gap_type,
            "direct_count": direct_count,
            "supporting_count": supporting_count,
            "inspiration_count": inspiration_count,
            "used_methods": list(used_methods),
            "theses": selected_theses,
            "synthesis_directive": synthesis_directive
        })

    return synthesized_clusters



def build_synthesis_prompt_section(synthesized_clusters: List[Dict[str, Any]]) -> str:
    """
    Menyusun blok prompt terstruktur per-klaster agar LLM menghasilkan
    1 ide skripsi untuk setiap klaster tema sintesis multi-dokumen.
    """
    if not synthesized_clusters:
        return ""

    sections = [
        "==================================================",
        "KLASTER TEMA SINTESIS MULTI-DOKUMEN (THEMATIC SYNTHESIS CLUSTERS):",
        "==================================================",
        "Setiap Ide (Ide 1 sampai Ide 5) WAJIB dibangun dari Klaster Sintesisnya masing-masing:",
        ""
    ]

    for sc in synthesized_clusters:
        c_idx = sc["cluster_index"]
        c_name = sc["cluster_name"]
        papers_str = sc["citations_formatted"]
        strength = sc["evidence_strength"]
        directive = sc["synthesis_directive"]

        sections.append(f"📌 KLASTER TEMA {c_idx} (UNTUK IDE {c_idx}): {c_name}")
        sections.append(f"   - Rujukan Skripsi: {papers_str}")
        sections.append(f"   - Kekuatan Bukti: [{strength}]")
        sections.append(f"   - Arahan Sintesis Gap: {directive}")
        sections.append("")

    return "\n".join(sections)
