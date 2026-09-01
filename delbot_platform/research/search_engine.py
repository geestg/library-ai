from delbot_platform.research.retrieval.thesis_hybrid_search import hybrid_search
from delbot_platform.research.retrieval.reranker import rerank
from delbot_platform.research.utils.query_utils import normalize_research_query, detect_prodi_from_query
from delbot_platform.research.extractors.thesis_evidence_extractor import extract_thesis_evidence
from delbot_platform.research.utils.diversity import apply_diversity_filter
from delbot_platform.research.models.research_models import ResearchContext

def build_thesis_object(item: dict):
    payload = item.get("payload", {})
    thesis = {
        "score": item.get("rerank_score", 0),
        "title": payload.get("title"),
        "author": payload.get("author"),
        "year": payload.get("year"),
        "prodi": payload.get("prodi"),
        "abstract": payload.get("abstract"),
        "chunk": payload.get("chunk"),
        "source_bab": payload.get("source_bab"),
        "url": payload.get("url")
    }
    thesis.update(extract_thesis_evidence(thesis))
    return thesis

def clean_author_name(author: str) -> str:
    if not author:
        return "Unknown"
    author = author.strip()
    if "," in author:
        parts = [p.strip() for p in author.split(",")]
        if len(parts) == 2:
            return f"{parts[1].title()} {parts[0].title()}"
    return author.title()

def build_citations(theses: list):
    citations = []
    for idx, thesis in enumerate(theses, start=1):
        raw_author = thesis.get("author") or ""
        citations.append({
            "source_id": idx,
            "title": thesis.get("title"),
            "author": clean_author_name(raw_author),
            "year": thesis.get("year"),
            "prodi": thesis.get("prodi"),
            "url": thesis.get("url"),
            "score": thesis.get("score", 0),
            "abstract": thesis.get("abstract"),
            "chunk": thesis.get("chunk"),
            "technologies": thesis.get("technologies", []),
            "methodologies": thesis.get("methodologies", []),
            "datasets": thesis.get("datasets", []),
            "evaluation_metrics": thesis.get("evaluation_metrics", [])
        })
    return citations

def is_allowed_item(item: dict) -> bool:
    payload = item.get("payload", {}) or {}
    year = int(payload.get("year", 0))
    prodi = (payload.get("prodi") or "").lower()
    
    # Izinkan jika tahun <= 2023
    if year <= 2023:
        return True
        
    # Khusus untuk prodi TRPL, izinkan tahun 2024 karena data historis TA TRPL di Del baru ada mulai 2024
    is_trpl = "rekayasa perangkat lunak" in prodi or "trpl" in prodi
    if is_trpl and year == 2024:
        return True
        
    return False

import re

def is_contextual_followup(query: str) -> bool:
    q = query.lower().strip()
    
    # Explicit prodi or fresh query requests are NOT follow-ups!
    prodi_keywords = [
        "informatika", "sistem informasi", "teknik elektro", "bioproses", 
        "manajemen informatika", "mekatronika", "trpl", "rekayasa perangkat lunak",
        "teknik komputer", "prodi", "jurusan", "cari ide", "rekomendasi ide"
    ]
    if any(pk in q for pk in prodi_keywords):
        return False

    patterns = [
        r"\bdari\s+(research|gap|hasil|penelitian|riset|tersebut|di\s+atas|itu|situ)\b",
        r"\bberdasarkan\s+(research|gap|hasil|penelitian|riset|tersebut|di\s+atas|itu|situ)\b",
        r"\bada\s+saran\s+lain\b",
        r"\bada\s+ide\s+lain\b",
        r"\bide\s+lain\b",
        r"\bbagaimana\s+detailnya\b",
        r"\bapa\s+novelty\s*nya\b",
        r"\blanjutkan\b",
    ]
    return any(re.search(pat, q) for pat in patterns)

def run_search(context: ResearchContext) -> ResearchContext:
    # 0. Reuse existing session theses if query is a contextual follow-up
    try:
        from delbot_platform.research.session import session_manager
        _session = session_manager.get_or_create(context.session_id)
        existing_theses = getattr(_session, "all_theses", [])
        
        is_followup = is_contextual_followup(context.query)
        if existing_theses and is_followup:
            print(f"[SEARCH ENGINE] Contextual follow-up query detected ('{context.query}'). Reusing {len(existing_theses)} theses from active session.")
            context.theses = existing_theses
            context.citations = build_citations(existing_theses)
            return context
        else:
            # Reset followup count for fresh new query
            _session.followup_count = 0
    except Exception as e:
        print(f"[SEARCH ENGINE] Session thesis check error: {e}")

    # 1. Normalisasi Query & Hard Program Study Router
    context.normalized_query = normalize_research_query(context.query)
    print("[NORMALIZED QUERY]", context.normalized_query)

    # Hard Router: Prioritaskan context.prodi / context.requested_prodi dari State Machine Planner
    requested_prodi = getattr(context, "prodi", None) or getattr(context, "requested_prodi", None)
    if not requested_prodi:
        requested_prodi = detect_prodi_from_query(context.query)
    
    p_clean_key = None
    if requested_prodi:
        p_clean = requested_prodi.lower().replace("d4 ", "").replace("s1 ", "").replace("d3 ", "").strip()
        p_clean_key = p_clean.replace(" ", "_")
        context.requested_prodi = p_clean_key

    if p_clean_key and p_clean_key.startswith("bukan_del:"):
        print(f"[SEARCH ENGINE] Non-DEL prodi requested '{p_clean_key}'. Bypassing DB search & setting empty sources/citations.")
        context.theses = []
        context.citations = []
        return context

    prodi_names_db = None
    if p_clean_key or requested_prodi:
        print(f"[PRODI FILTER] Detected prodi request: {requested_prodi} (key: {p_clean_key})")
        MAP_PRODI_DB = {
            "sistem_informasi": ["Sistem Informasi", "S1 Sistem Informasi"],
            "informatika": ["Informatika", "S1 Informatika", "Teknik Informatika"],
            "trpl": ["Teknologi Rekayasa Perangkat Lunak", "TRPL", "Sarjana Terapan Teknologi Rekayasa Perangkat Lunak", "D4 TRPL"],
            "teknologi_rekayasa_perangkat_lunak": ["Teknologi Rekayasa Perangkat Lunak", "TRPL", "Sarjana Terapan Teknologi Rekayasa Perangkat Lunak", "D4 TRPL"],
            "teknologi_informasi": ["TI D3", "Teknologi Informasi", "D3 TI"],
            "teknologi_komputer": ["TK D3", "Teknologi Komputer", "D3 TK"],
            "teknik_elektro": ["Teknik Elektro", "S1 Teknik Elektro"],
            "manajemen_rekayasa": ["Manajemen Rekayasa", "S1 Manajemen Rekayasa"],
            "teknik_metalurgi": ["Teknik Metalurgi", "S1 Teknik Metalurgi"],
            "teknik_bioproproses": ["Teknologi Bioproses", "Teknik Bioproses", "S1 Teknik Bioproses"],
            "teknologi_bioproses": ["Teknologi Bioproses", "Teknik Bioproses", "S1 Teknik Bioproses"],
            "bioteknologi": ["Bioteknologi", "S1 Bioteknologi"],
        }
        prodi_names_db = MAP_PRODI_DB.get(p_clean_key)
        if not prodi_names_db and requested_prodi:
            prodi_names_db = [requested_prodi]
        print(f"[PRODI FILTER] Mapping '{requested_prodi}' to DB values: {prodi_names_db}")

    # 2. Ambil Search Offset dari Sesi Chat (untuk Follow-up)
    search_offset = 0
    try:
        from delbot_platform.research.session import session_manager
        _session = session_manager.get_or_create(context.session_id)
        search_offset = getattr(_session, "followup_count", 0) * 10
        print(f"[SEARCH ENGINE] Using search offset: {search_offset} (followup count: {getattr(_session, 'followup_count', 0)})")
    except Exception as e:
        print(f"[SEARCH ENGINE] Failed to fetch session offset: {e}")

    # 3. Multi-Query Hybrid Search ke Vector Database
    # Query primer (spesifik) + Query metode/domain (untuk cakupan komprehensif)
    search_queries = [context.normalized_query]
    
    # Deteksi anchor metode/domain untuk multi-query expansion
    q_lower = context.query.lower()
    if any(k in q_lower for k in ["cnn", "convolutional", "citra medis", "penyakit kulit"]):
        search_queries.append("convolutional neural network cnn klasifikasi")
    if any(k in q_lower for k in ["computer vision", "vision", "pengolahan citra", "citra", "hama", "tanaman", "daun"]):
        search_queries.append("computer vision cnn klasifikasi tanaman daun hama")
        search_queries.append("klasifikasi penyakit tanaman convolutional neural network")
    if any(k in q_lower for k in ["yolo", "object detection", "deteksi objek"]):
        search_queries.append("yolo object detection deteksi objek")
    if any(k in q_lower for k in ["iot", "internet of things", "monitoring kualitas air", "sensor"]):
        search_queries.append("iot internet of things sensor monitoring")
    if any(k in q_lower for k in ["microgrid", "inverter", "stabilitas daya"]):
        search_queries.append("microgrid inverter daya kontrol stabilitas")
    if any(k in q_lower for k in ["biomassa", "fermentasi", "bioetanol"]):
        search_queries.append("fermentasi biomassa bioetanol bioproses")

    # PRODI-TRACK DIVERSE EXPANSION (Untuk kueri umum per-prodi tanpa sub-topik spesifik)
    PRODI_TRACK_EXPANSIONS = {
        "informatika": [
            "machine learning deep learning neural network klasifikasi",
            "computer vision pengolahan citra convolutional",
            "natural language processing analisis sentimen text mining",
            "software engineering perancangan sistem informasi arsitektur",
            "algoritma optimasi sistem cerdas kecerdasan buatan"
        ],
        "sistem_informasi": [
            "evaluasi sistem informasi tata kelola cobit itil",
            "enterprise architecture togaf perencanaan strategis",
            "business intelligence data warehouse dashboard analytics",
            "user experience usability testing acceptance tam ueq",
            "sistem pendukung keputusan analytical hierarchy process topsis"
        ],
        "trpl": [
            "pengembangan sistem informasi perangkat lunak agile scrum",
            "arsitektur microservices rest api cloud computing",
            "otomasi pengujian perangkat lunak software testing ci cd",
            "mobile application flutter react native android",
            "web application framework vue react laravel spring"
        ],
        "teknik_elektro": [
            "sistem kendali kontrol pid plc otomatisasi",
            "tenaga listrik transmisi distribusi proteksi",
            "energi terbarukan plts panel surya solar cell inverter",
            "embedded system internet of things mikrokontroler sensor",
            "pemrosesan sinyal elektronika daya konverter"
        ],
        "manajemen_rekayasa": [
            "manajemen rantai pasok supply chain manajemen logistik",
            "analisis kelayakan finansial investasi bisnis",
            "pengendalian kualitas six sigma statistical process control",
            "ergonomi keselamatan kerja k3 produktivitas kerja",
            "manajemen proyek evaluasi efisiensi operasional"
        ],
        "teknologi_bioproses": [
            "fermentasi bioreaktor bioetanol biomassa enzim",
            "ekstraksi senyawa bioaktif pemurnian produk hayati",
            "pengolahan limbah biologi pengolahan air limbah",
            "kinetika pertumbuhan mikroba optimasi medium",
            "formulasi bioproduk pangan farmasi bioproses"
        ],
        "bioteknologi": [
            "isolasi karakterisasi bakteri mikroorganisme kultur",
            "rekayasa genetika dna molekuler pcr sekuensing",
            "bioaktivitas metabolit sekunder uji antibakteri",
            "bioremediasi biodegradasi mikroba lingkungan",
            "kultur jaringan mikropropagasi tanaman hayati"
        ]
    }

    # Jika kueri adalah kueri umum prodi (tanpa kata kunci teknis spesifik), sertakan rumpun riset prodi
    has_specific_tech = any(k in q_lower for k in [
        "cnn", "yolo", "iot", "microgrid", "fermentasi", "vision", "citra", "nlp",
        "sentimen", "keamanan", "malware", "blockchain", "scrum", "agile", "plts",
        "kualitas air", "hama", "kulit", "jadwal", "genetik", "fuzzy", "svm", "bilstm"
    ])
    if not has_specific_tech and p_clean_key in PRODI_TRACK_EXPANSIONS:
        print(f"[PRODI TRACK EXPANSION] Expanding broad query for prodi '{p_clean_key}' across 5 diverse research tracks.")
        search_queries.extend(PRODI_TRACK_EXPANSIONS[p_clean_key])

    raw_hybrid_candidates = []
    seen_payload_hashes = set()
    for sq in search_queries:
        res = hybrid_search(
            query=sq,
            limit=40,
            prodi_names=prodi_names_db,
            offset=search_offset
        )
        for r in res:
            p = r.get("payload", {}) or {}
            uid = f"{p.get('title', '')}_{p.get('author', '')}_{p.get('year', '')}"
            if uid not in seen_payload_hashes:
                seen_payload_hashes.add(uid)
                raw_hybrid_candidates.append(r)

    # 4. Reranking Hasil Pencarian
    top_k_val = 60 if (not has_specific_tech and p_clean_key in PRODI_TRACK_EXPANSIONS) else 30
    reranked_results = rerank(
        query=context.query,
        documents=raw_hybrid_candidates,
        top_k=top_k_val
    )
    print(f"[RERANK] {len(reranked_results)} results after multi-query expansion")

    # 5. Filter Threshold Score, Hard Prodi Metadata Filter, & Strict Topical Alignment
    generic_research_terms = {
        "saya", "mau", "cari", "ide", "skripsi", "dari", "prodi", "tentang",
        "bertema", "untuk", "dengan", "dan", "atau", "yang", "pada", "di",
        "menggunakan", "sistem", "berbasis", "serta", "sebagai", "adalah",
        "butuh", "ingin", "sedang", "mencari", "topik", "judul", "penelitian",
        "tugas", "akhir", "rekomendasi", "berikan", "bagaimana", "apakah",
        "sudah", "pernah", "ada", "seberapa", "baru", "dalam", "studi", "analisis",
        "gap", "metode", "metodologi", "penerapan", "implementasi", "evaluasi",
        "pengujian", "perancangan", "pembuatan", "pengembangan", "celah", "riset",
        "algoritma", "model", "kasus", "terhadap", "tingkat", "pengaruh",
        "del", "it", "institut", "teknologi", "research", "klasifikasi", "pengukuran",
        "kualitas", "pelayanan", "jurusan", "mahasiswa", "bantu", "buatkan", "tolong",
        "informasi", "rekayasa", "case", "study", "jasa", "konsumen", "faktor", "uji",
        "informatika", "elektro", "bioproses", "bioteknologi", "metalurgi", "bisnis",
        "manajemen", "komputer", "perangkat", "lunak", "trpl", "sisfo",
        "terkait", "mengenai", "seputar", "bidang", "ranah", "fokus", "tema",
        "berjudul", "berfokus", "cabang", "kuliah"
    }
    raw_tokens = re.findall(r'\b[a-zA-Z]{3,}\b', context.query.lower())
    query_substantive_kws = [w for w in raw_tokens if w not in generic_research_terms]

    # Domain & Method specific anchor aliases
    METHOD_ANCHORS = {
        "cnn": ["cnn", "convolutional", "neural network", "deep learning", "vgg", "resnet", "xception", "mobilenet", "citra", "vision", "image"],
        "computer vision": ["vision", "citra", "cnn", "yolo", "vgg", "resnet", "deep learning", "image", "deteksi", "klasifikasi", "hama", "tanaman"],
        "vision": ["vision", "citra", "cnn", "yolo", "vgg", "resnet", "deep learning", "image", "deteksi", "klasifikasi", "hama", "tanaman"],
        "citra": ["citra", "image", "vision", "cnn", "yolo", "vgg", "resnet", "deteksi", "klasifikasi"],
        "yolo": ["yolo", "darknet", "object detection", "deteksi objek", "bounding box"],
        "iot": ["iot", "internet of things", "sensor", "arduino", "esp32", "esp8266", "microcontroller", "mikrokontroler", "lora", "monitoring"],
        "microgrid": ["microgrid", "inverter", "power", "daya", "tegangan", "frekuensi", "grid", "panel surya", "plts"],
        "fermentasi": ["fermentasi", "biomassa", "bioreaktor", "bioetanol", "glukosa", "hidrolisis", "enzim"],
        "machine_learning": ["machine learning", "svm", "random forest", "decision tree", "naive bayes", "clustering", "knn"]
    }
    required_method_aliases = []
    for k, aliases in METHOD_ANCHORS.items():
        if k in q_lower:
            required_method_aliases.extend(aliases)

    def _is_topically_aligned(item: dict) -> bool:
        score = item.get("rerank_score", -99.0)
        payload = item.get("payload", {}) or {}
        text_corpus = (
            (payload.get("title") or "") + " " +
            (payload.get("abstract") or "") + " " +
            (payload.get("chunk") or "")
        ).lower()

        # 1. Jika kueri menyebut metode teknis spesifik (e.g. CNN, YOLO, IoT, Microgrid, Fermentasi),
        # Dokumen WAJIB mengandung setidaknya 1 istilah dari famili metode tersebut!
        if required_method_aliases:
            has_method = any(alias in text_corpus for alias in required_method_aliases)
            if not has_method:
                return False

        # 2. Cek keselarasan kata kunci substantif
        if query_substantive_kws:
            has_kw = any(kw in text_corpus for kw in query_substantive_kws)
            if has_kw:
                return score > -8.5
            if required_method_aliases:
                return score > -6.0
            return False

        # 3. Untuk kueri umum per-prodi (tanpa kata kunci topik spesifik), loloskan dokumen prodi yang valid
        return score > -13.0

    filtered_results = []
    for item in reranked_results:
        payload = item.get("payload", {}) or {}
        item_prodi = (payload.get("prodi") or "").lower()
        
        # Hard Prodi Filtering: Jika prodi_names_db dispesifikasikan, WAJIB BERASAL DARI PRODI TERSEBUT
        if prodi_names_db:
            matches_prodi = any(db_p.lower() in item_prodi for db_p in prodi_names_db)
            if matches_prodi and is_allowed_item(item):
                filtered_results.append(item)
            continue

        if _is_topically_aligned(item) and is_allowed_item(item):
            filtered_results.append(item)

    # 5b. Fallback Pencarian Prodi Serumpun jika Hasil Utama Kosong
    effective_prodi_key = p_clean_key or (requested_prodi.lower().replace(" ", "_") if requested_prodi else None)
    if not filtered_results and effective_prodi_key:
        print(f"[SEARCH FALLBACK] 0 results for prodi '{effective_prodi_key}'. Expanding search to related prodis only.")
        MAP_FALLBACK_PRODI = {
            "trpl": ["Teknologi Rekayasa Perangkat Lunak", "TRPL", "Informatika", "S1 Informatika", "Sistem Informasi"],
            "teknologi_rekayasa_perangkat_lunak": ["Teknologi Rekayasa Perangkat Lunak", "TRPL", "Informatika", "S1 Informatika", "Sistem Informasi"],
            "teknologi_informasi": ["Teknologi Informasi", "TI D3", "Informatika", "S1 Informatika", "Sistem Informasi"],
            "teknologi_komputer": ["Teknologi Komputer", "TK D3", "Teknik Elektro", "S1 Teknik Elektro"],
            "sistem_informasi": ["Sistem Informasi", "S1 Sistem Informasi", "Informatika", "S1 Informatika"],
            "informatika": ["Informatika", "S1 Informatika", "Sistem Informasi", "TI D3"],
            "teknik_elektro": ["Teknik Elektro", "S1 Teknik Elektro", "Teknologi Komputer", "TK D3"],
            "teknologi_bioproses": ["Teknologi Bioproses", "Teknik Bioproses", "Bioteknologi", "S1 Bioteknologi"],
            "teknik_bioproses": ["Teknologi Bioproses", "Teknik Bioproses", "Bioteknologi", "S1 Bioteknologi"],
            "bioteknologi": ["Bioteknologi", "S1 Bioteknologi", "Teknologi Bioproses", "Teknik Bioproses"],
            "manajemen_rekayasa": ["Manajemen Rekayasa", "S1 Manajemen Rekayasa"],
            "teknik_metalurgi": ["Teknik Metalurgi", "S1 Teknik Metalurgi"],
        }
        fallback_prodi_names = MAP_FALLBACK_PRODI.get(effective_prodi_key)
        
        if fallback_prodi_names:
            fallback_hybrid_results = hybrid_search(
                query=context.normalized_query,
                limit=50,
                prodi_names=fallback_prodi_names,
                offset=search_offset
            )
            fallback_reranked = rerank(
                query=context.query,
                documents=fallback_hybrid_results,
                top_k=20
            )
            for item in fallback_reranked:
                payload = item.get("payload", {}) or {}
                item_prodi = (payload.get("prodi") or "").lower()
                matches_fallback = any(fb_p.lower() in item_prodi for fb_p in fallback_prodi_names)
                if matches_fallback and _is_topically_aligned(item) and is_allowed_item(item):
                    filtered_results.append(item)
            print(f"[SEARCH FALLBACK] Filtered fallback search returned {len(filtered_results)} strictly aligned results.")

    # 6. Prodi Soft Priority (Jika user minta prodi spesifik, prioritaskan di atas)
    if requested_prodi:
        prodi_matched = []
        prodi_others  = []
        for item in filtered_results:
            item_prodi = (item.get("payload", {}).get("prodi") or "").lower()
            item_prodi_slug = item_prodi.replace(" ", "_")
            if item_prodi_slug == requested_prodi:
                prodi_matched.append(item)
            else:
                prodi_others.append(item)
        filtered_results = prodi_matched + prodi_others
        print(f"[PRODI FILTER] {len(prodi_matched)} matched '{requested_prodi}', {len(prodi_others)} others kept as fallback")

    # 7. Soft Exclusion Paper yang Sudah Pernah Disajikan
    used_titles: set = set()
    try:
        from delbot_platform.research.session import session_manager
        _session = session_manager.get_or_create(context.session_id)
        used_titles = getattr(_session, "used_titles", set())
    except Exception:
        pass

    if used_titles:
        fresh_results = []
        seen_results  = []
        for item in filtered_results:
            item_title = (
                item.get("payload", {}).get("title") or
                item.get("title") or ""
            ).strip().lower()
            if item_title and item_title in used_titles:
                seen_results.append(item)
            else:
                fresh_results.append(item)
        filtered_results = fresh_results + seen_results
        print(f"[USED-PAPER FILTER] {len(fresh_results)} fresh, {len(seen_results)} already-seen pushed to bottom")

    print(f"[FILTERED] {len(filtered_results)} results")

    # 8. Membangun Objek Tesis (Parsing metadata RAG)
    theses = [build_thesis_object(item) for item in filtered_results]

    # 9. Terapkan Diversifikasi Hasil Pencarian
    div_year_cap = 10 if (context.intent in ["thesis_idea", "title_generation"] or context.mode in ["thesis_idea", "analysis"]) else 5
    div_topic_cap = 10 if (context.intent in ["thesis_idea", "title_generation"] or context.mode in ["thesis_idea", "analysis"]) else 5
    theses = apply_diversity_filter(theses, max_per_year=div_year_cap, max_per_title_keyword=div_topic_cap)

    # 10. Penggabungan Citations Secara Kumulatif (Mencegah Ketimpa Saat Follow-up)
    try:
        from delbot_platform.research.session import session_manager
        _session = session_manager.get_or_create(context.session_id)
        
        cumulative_theses = getattr(_session, "all_theses", [])
        if not isinstance(cumulative_theses, list):
            cumulative_theses = []
            
        existing_titles = {t.get("title", "").strip().lower() for t in cumulative_theses if t.get("title")}
        
        target_top_k = 25 if (context.intent in ["thesis_idea", "title_generation"] or context.mode in ["thesis_idea", "analysis"]) else context.top_k
        appended_count = 0
        new_valid_theses = []
        for t in theses:
            t_title = t.get("title", "").strip().lower()
            if t_title and t_title not in existing_titles:
                new_valid_theses.append(t)
                existing_titles.add(t_title)
                appended_count += 1
                if appended_count >= target_top_k:
                    break
                    
        cumulative_theses = cumulative_theses + new_valid_theses
        _session.all_theses = cumulative_theses
        context.theses = cumulative_theses
        print(f"[SEARCH ENGINE] Cumulative theses total: {len(context.theses)} (newly added: {len(new_valid_theses)}, target: {target_top_k})")
    except Exception as e:
        print(f"[SEARCH ENGINE ERROR] Cumulative theses merge failed: {e}")
        target_top_k = 25 if (context.intent in ["thesis_idea", "title_generation"] or context.mode in ["thesis_idea", "analysis"]) else context.top_k
        context.theses = theses[:target_top_k]

    # 11. Bangun Citation references
    context.citations = build_citations(context.theses)
    return context
