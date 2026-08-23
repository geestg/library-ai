from fastapi import APIRouter, Header
from pydantic import BaseModel

from delbot_platform.knowledge.library.agent import LibraryAcademicAgent
from delbot_platform.knowledge.librarian.agent import LibraryLibrarianAgent
from delbot_platform.core.guardrails import validate_query_safety


router = APIRouter()


# =========================================
# REQUEST MODEL
# =========================================

class ChatRequest(BaseModel):
    message: str | None = None
    query: str | None = None
    session_id: str | None = None
    history: list[dict[str, str]] = []


def sync_session_history(session, history: list[dict[str, str]]):
    if not history:
        return

    has_assistant = any(
        h.get("role", "user") == "assistant"
        for h in history
    )

    if has_assistant or not session.conversation.messages:
        session.conversation.messages = []
        for h in history:
            session.conversation.append(
                role=h.get("role", "user"),
                content=h.get("content", "")
            )
        return

    existing_messages = {
        (m.role, m.content)
        for m in session.conversation.messages
    }

    for h in history:
        role = h.get("role", "user")
        content = h.get("content", "")
        if content and (role, content) not in existing_messages:
            session.conversation.append(role=role, content=content)
            existing_messages.add((role, content))


# =========================================
# CHAT ROUTE — Library Agent & Admin Agent
# =========================================

@router.post("/chat")
@router.post("/api/chat")
@router.post("/api/v1/chat")
def chat(req: ChatRequest, x_user_role: str = Header(default="student")):
    """
    Endpoint chat utama.
    Mendukung perutean peran (Student vs Admin) dan Global Guardrail.
    """
    user_text = (req.message or req.query or "").strip()
    from delbot_platform.research.session import session_manager
    s_id = req.session_id.strip() if req.session_id else "chat_session"
    session = session_manager.get_or_create(s_id)

    # Sync history from frontend to session manager
    sync_session_history(session, req.history)

    # Build history list from backend session messages
    history_list = []
    if session and session.conversation.messages:
        for msg in session.conversation.messages:
            history_list.append({
                "role": msg.role,
                "content": msg.content
            })

    # 1. Global Guardrail Check (Satpam di Lobi Utama API)
    is_safe, warning_msg = validate_query_safety(user_text)
    if not is_safe:
        return {
            "status": "success",
            "intent": "security_block",
            "response": warning_msg,
            "citations": [],
            "sources": [],
        }

    # 2. Guardrail Peran: Cegah tamu/mahasiswa mengakses perintah admin sensitif
    role = x_user_role.lower().strip()
    msg_clean = user_text.lower().strip()
    
    if role == "guest":
        admin_keywords = ["laporan denda", "laporan sirkulasi", "generate laporan", "sync", "sinkron", "koleksi baru"]
        if any(kw in msg_clean for kw in admin_keywords):
            return {
                "status": "success",
                "intent": "security_block",
                "response": "Maaf, tugas administratif perpustakaan hanya dapat diakses oleh pustakawan IT Del yang telah terverifikasi via CIS.",
                "citations": [],
                "sources": [],
            }

    if role == "student" or role == "guest":
        admin_keywords = ["laporan denda", "laporan sirkulasi", "generate laporan", "sync", "sinkron", "koleksi baru"]
        if any(kw in msg_clean for kw in admin_keywords):
            return {
                "status": "success",
                "intent": "security_block",
                "response": "Maaf, Anda tidak memiliki hak akses untuk memicu tugas atau laporan administratif perpustakaan.",
                "citations": [],
                "sources": [],
            }
        
        # 3. Rute Penelitian / Skripsi: Jika kueri mencari ide skripsi/penelitian, atau percakapan sedang aktif di topik penelitian
        research_keywords = [
            "skripsi", "skirpsi", "skipsi", "sekripsi", "sripsi", "skripis", "tugas akhir", 
            "ide skripsi", "ide skirpsi", "judul skripsi", "penelitian", "thesis", 
            "ide penelitian", "judul penelitian", "topik skripsi", "topik penelitian", 
            "rekomendasi judul", "rekomendasi topik", "buat ide", "cari ide", "minta ide", "ide skripsi prodi"
        ]
        
        is_active_research = False
        
        # Kata kunci umum perpustakaan (administrasi, jam buka, peminjaman, pencarian & follow-up buku)
        # yang harus memotong/mem-bypass mode riset agar tidak terperangkap
        general_library_keywords = [
            "jam buka", "jam tutup", "buka jam", "tutup jam", "kapan buka", "kapan tutup",
            "jadwal perpus", "jadwal buka", "operasional", "buka perpus", "hari apa",
            "pinjam", "meminjam", "kembali", "pengembalian", "denda", "bayar denda",
            "kartu perpus", "anggota", "lokasi", "alamat", "gedung", "fasilitas", "kontak",
            "buku apa", "cari buku", "carikan buku", "rekomendasi buku", "rekomendasikan buku",
            "daftar buku", "ada buku", "buku tentang", "buku karangan", "buku karya", "buku terbitan",
            "letak buku", "lokasi buku", "rak buku", "referensi buku", "bacaan", "jam berapa",
            "buku lain", "buku lainnya"
        ]
        
        import re

        def _has_research_kw(text: str) -> bool:
            t_clean = text.lower()
            # Explicit multi-word research terms & follow-up prompts
            multi_words = [
                "ide skripsi", "judul skripsi", "topik skripsi", "ide penelitian", 
                "judul penelitian", "topik penelitian", "tugas akhir", "research gap", 
                "novelty", "ada ide lain", "ide lain", "ide lainnya", "topik lain", 
                "judul lain", "opsi lain", "contoh lain", "prodi lain", "berikan lagi", 
                "tambah lagi", "ide lain?", "ada lagi", "draf", "bab 1", "bab 3",
                "ide skripsi prodi", "judul skripsi prodi", "tugas akhir prodi"
            ]
            if any(mw in t_clean for mw in multi_words):
                return True
            # Exact single word boundary match (pastikan bukan sekadar kata umum)
            single_words = ["skripsi", "skirpsi", "skipsi", "sekripsi", "sripsi", "thesis"]
            for sw in single_words:
                if re.search(r'\b' + re.escape(sw) + r'\b', t_clean):
                    return True
            if "penelitian" in t_clean and not any(bw in t_clean for bw in ["buku", "katalog", "pustaka"]):
                return True
            return False

        from delbot_platform.research.session import session_manager
        s_id = req.session_id.strip() if req.session_id else "chat_session"
        session = session_manager.get_or_create(s_id)

        # Cek apakah pesan sebelumnya dari assistant merupakan pertanyaan klarifikasi riset
        last_asst_msg = ""
        for h in reversed(req.history):
            if h.get("role") == "assistant":
                last_asst_msg = h.get("content", "").lower()
                break
        if not last_asst_msg and session.conversation.messages:
            for m in reversed(session.conversation.messages):
                if m.role == "assistant":
                    last_asst_msg = m.content.lower()
                    break

        clarification_prompts = [
            "boleh tahu program studi anda",
            "pilihan mana yang anda minati",
            "spesifik jurusan atau topiknya",
            "kategori",
            "sebutkan mata kuliah"
        ]
        is_clarification_response = any(cp in last_asst_msg for cp in clarification_prompts)

        menu_selection_pattern = re.match(r'^\s*(?:nomor\s*)?[1-5]\s*(?:\.|$)', msg_clean)
        
        # Pengecekan prioritas: Jika user eksplisit mencari buku, JANGAN masukkan ke research mode
        is_explicit_book_query = any(bw in msg_clean for bw in [
            "cari buku", "carikan buku", "rekomendasi buku", "rekomendasikan buku",
            "buku tentang", "buku karangan", "buku karya", "buku terbitan", "ada buku",
            "letak buku", "lokasi buku", "rak buku", "buku fisika", "buku matematika",
            "buku algoritma", "buku pemrograman", "buku jaringan", "buku sistem", "buku iot", "buku manajemen"
        ]) and not any(rw in msg_clean for rw in ["skripsi", "tugas akhir", "research gap", "novelty", "ide skripsi", "judul skripsi"])

        if is_explicit_book_query:
            is_active_research = False
        elif _has_research_kw(msg_clean) or (is_clarification_response and menu_selection_pattern):
            is_active_research = True
        elif any(kw in msg_clean for kw in general_library_keywords):
            is_active_research = False
        else:
            # Pengecekan konteks percakapan di riwayat chat (HANYA dari USER, bukan Assistant)
            for h in req.history:
                if h.get("role") == "user":
                    if _has_research_kw(h.get("content", "")):
                        is_active_research = True
                        break

        if is_active_research:
            if role == "guest":
                return {
                    "status": "success",
                    "intent": "security_block",
                    "response": (
                        "Maaf, fitur analisis skripsi dan riset akademis hanya dapat diakses oleh "
                        "sivitas akademika IT Del.\n\n"
                        "Silakan masuk menggunakan akun CIS Del Anda melalui tombol login di pojok kiri bawah "
                        "untuk membuka akses penuh."
                    ),
                    "citations": [],
                    "sources": [],
                }

            from delbot_platform.research.research_service import research_analysis
            from delbot_platform.research.research_engine import extract_assistant_content
            
            session.conversation.append(role="user", content=req.message)

            result = research_analysis(
                query=req.message,
                session_id=s_id,
                top_k=25,
                mode="analysis"
            )
            response_text = result if isinstance(result, str) else extract_assistant_content(result)
            
            # Simpan judul paper yang sudah digunakan ke session
            citations = []
            if isinstance(result, dict):
                citations = result.get("citations") or result.get("sources") or []

            if not citations and hasattr(session, "all_theses") and session.all_theses:
                from delbot_platform.research.search_engine import build_citations
                citations = build_citations(session.all_theses)
            elif not citations and hasattr(session, "execution") and getattr(session.execution, "serialized_context", None):
                citations = session.execution.serialized_context.get("citations", []) or session.execution.serialized_context.get("sources", [])

            session.conversation.append(
                role="assistant",
                content=response_text,
                citations=citations,
                sources=citations
            )
            if citations:
                session.all_theses = citations

            for c in citations:
                title = (c.get("title") or c.get("judul") or "").strip().lower()
                if title:
                    session.used_titles.add(title)
                    
            print(f"[CHAT_ROUTE] Session used_titles count: {len(session.used_titles)}, Citations count: {len(citations)}")
            
            return {
                "status": "success",
                "intent": "research",
                "response": response_text,
                "citations": citations,
                "sources": citations,
            }
        
        # Dapatkan nama hari & tanggal lokal Bahasa Indonesia untuk pencocokan FAQ operasional perpustakaan
        import datetime
        
        DAYS_INDO = {
            "Monday": "Senin",
            "Tuesday": "Selasa",
            "Wednesday": "Rabu",
            "Thursday": "Kamis",
            "Friday": "Jumat",
            "Saturday": "Sabtu",
            "Sunday": "Minggu"
        }
        
        MONTHS_INDO = {
            1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
            5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
            9: "September", 10: "Oktober", 11: "November", 12: "Desember"
        }
        
        now = datetime.datetime.now()
        day_name = DAYS_INDO.get(now.strftime("%A"), now.strftime("%A"))
        month_name = MONTHS_INDO.get(now.month, now.strftime("%B"))
        
        formatted_time = f"{day_name}, {now.day} {month_name} {now.year}, Pukul {now.strftime('%H:%M')} WIB"
        print(f"[CHAT_ROUTE] Injected local time: {formatted_time}")

        # Jalankan Academic Agent (LibraryAcademicAgent)
        agent = LibraryAcademicAgent()
        result = agent.run(req.message, history_list, current_time=formatted_time, user_role=role)
    else:
        # Jalankan Librarian Agent (LibraryLibrarianAgent)
        agent = LibraryLibrarianAgent()
        result = agent.run(req.message, history_list)

    resp_text = result.get("response", "")
    session.conversation.append(role="user", content=req.message)
    session.conversation.append(role="assistant", content=resp_text)

    return {
        "status": "success",
        "intent": result.get("intent", "recommendation"),
        "response": resp_text,
        "citations": result.get("citations", []),
        "sources": result.get("sources", []),
        "data": result.get("data", None)
    }



# =========================================
# STREAMING CHAT ROUTER
# =========================================

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import json
import re

from delbot_platform.research.research_engine import (
    persist_assistant_response,
    persist_execution_snapshot,
    serialize_research_context,
)

from delbot_platform.research.agents import ResearchAgent

from delbot_platform.research.session import (
    session_manager,
)

# =========================================
# LIBRARY PIPELINE IMPORTS
# =========================================

from delbot_platform.orchestration.intent_classifier import (
    classify_intent,
)

from delbot_platform.orchestration.model_selector import (
    select_model,
)

from delbot_platform.research.retrieval.library_search import (
    library_hybrid_search,
)

from delbot_platform.research.retrieval.reranker import (
    rerank,
)

from delbot_platform.research.retrieval.library_context_builder import (
    build_library_book_context,
)

from delbot_platform.research.prompts.prompt_builder import (
    build_prompt,
)

from delbot_platform.ai.llm.model_gateway import (
    gateway,
)




# =========================================
# STREAM EVENT
# =========================================

def stream_event(
    event_type: str,
    data,
):
    return (
        json.dumps(
            {
                "type": event_type,

                "data": data,
            },
            ensure_ascii=False,

        )
        + "\n"
    )


# =========================================
# PERSIST STREAM ASSISTANT
# =========================================

def persist_stream_assistant(
    context,
    response,
) -> str:
    session = session_manager.get(
        context.session_id
    )
    if session is None:
        return ""
    return persist_assistant_response(
        session=session,
        response=response,
    )


# =========================================
# PERSIST STREAM EXECUTION
# =========================================

def persist_stream_execution(
    context,
    response_content: str = "",
) -> dict:
    session = session_manager.get(
        context.session_id
    )
    if session is None:
        return {}
    return persist_execution_snapshot(
        session=session,
        context=context,
        response_content=(
            response_content
        ),
    )


# =========================================
# REQUEST MODEL
# =========================================

class StreamRequest(BaseModel):
    session_id: str | None = None
    message: str
    active_document_ids: list = []


# =========================================
# LIBRARY PIPELINE HANDLER
# =========================================

def _run_library_pipeline(req, intent: str):
    """
    Pipeline khusus rekomendasi buku perpustakaan.
    Menggunakan library_books collection di Qdrant.
    Dipanggil oleh generate() saat intent == 'recommendation'.
    """

    selected = select_model(intent)
    provider = selected["provider"]
    model    = selected["model"]

    yield stream_event(
        "metadata",
        {"provider": provider, "model": model, "intent": intent},
    )

    # Clean conversational noise from search query (e.g. "Di mana lokasi rak untuk buku...")
    noise_patterns = [
        r"(?i)^di\s+mana\s+lokasi\s+rak\s+untuk\s+buku\s+",
        r"(?i)^di\s+mana\s+lokasi\s+rak\s+buku\s+",
        r"(?i)^di\s+mana\s+lokasi\s+buku\s+",
        r"(?i)^lokasi\s+rak\s+buku\s+",
        r"(?i)^cari\s+buku\s+tentang\s+",
        r"(?i)^buku\s+tentang\s+",
        r"(?i)^rekomendasi\s+buku\s+",
        r"(?i)^buku\s+apa\s+yang\s+",
        r"(?i)^bisa\s+carikan\s+buku\s+",
    ]
    clean_query = req.message.strip()
    for pattern in noise_patterns:
        clean_query = re.sub(pattern, "", clean_query)
    clean_query = clean_query.strip(" ?!.")
    # Bilingual Query Expansion (Comprehensive IT Del Institutional Academic Dictionary)
    bilingual_terms = {
        # FITE & Vokasi (SI, IF, TI, TRPL, TK, D3 TI)
        "struktur data": "data structures",
        "algoritma": "algorithms",
        "sistem operasi": "operating systems",
        "jaringan komputer": "computer networking",
        "basis data": "database systems",
        "kecerdasan buatan": "artificial intelligence",
        "pembelajaran mesin": "machine learning",
        "pembelajaran mendalam": "deep learning",
        "rekayasa perangkat lunak": "software engineering",
        "pemrograman web": "web programming",
        "pemrograman terstruktur": "structured programming",
        "pemrograman berorientasi objek": "object oriented programming",
        "keamanan siber": "cybersecurity",
        "keamanan jaringan": "network security",
        "sistem tertanam": "embedded systems",
        "pengolahan citra": "image processing",
        "visi komputer": "computer vision",
        "pemrosesan bahasa alami": "natural language processing",
        "analisis data": "data analytics",
        "sains data": "data science",
        "penambangan data": "data mining",
        "sistem pakar": "expert systems",
        "interaksi manusia komputer": "human computer interaction",
        "komputasi awan": "cloud computing",
        "sistem terdistribusi": "distributed systems",
        "sistem informasi manajemen": "management information systems",

        # Teknik Elektro (FITE - TE)
        "teknik elektro": "electrical engineering",
        "rangkaian listrik": "electric circuits",
        "sistem kendali": "control systems",
        "pemrosesan sinyal": "signal processing",
        "mikrokontroler": "microcontrollers",
        "elektronika analog": "analog electronics",
        "elektronika digital": "digital electronics",
        "telekomunikasi": "telecommunications",
        "sistem tenaga listrik": "power systems",
        "sensor dan aktuator": "sensors and actuators",

        # FTI (Manajemen Rekayasa, Teknik Metalurgi)
        "manajemen rekayasa": "engineering management",
        "rantai pasok": "supply chain",
        "logistik": "logistics",
        "manajemen operasi": "operations management",
        "manajemen proyek": "project management",
        "manajemen kualitas": "quality management",
        "manufaktur cerdas": "smart manufacturing",
        "teknik metalurgi": "metallurgical engineering",
        "ekstraksi logam": "extractive metallurgy",
        "ilmu bahan": "materials science",
        "korosi": "corrosion",
        "rekayasa proses": "process engineering",
        "penelitian operasional": "operations research",

        # Bioteknologi & Bioproses (FITE - Biotek / TB)
        "bioteknologi": "biotechnology",
        "teknik bioproses": "bioprocess engineering",
        "biologi molekuler": "molecular biology",
        "rekayasa genetika": "genetic engineering",
        "bioinformatika": "bioinformatics",
        "mikrobiologi": "microbiology",
        "biokimia": "biochemistry",
        "fermentasi": "fermentation",
        "teknologi enzim": "enzyme technology",
        "kultur jaringan": "tissue culture"
    }

    expanded_terms = []
    clean_lower = clean_query.lower()
    for id_term, en_term in bilingual_terms.items():
        if id_term in clean_lower and en_term not in clean_lower:
            expanded_terms.append(en_term)

    # search_term: bilingual (for Qdrant hybrid search - vector + BM25)
    # rerank_query: English-ONLY (for ms-marco Cross-Encoder which is English-only trained)
    #   Using English terms ensures cross-encoder correctly ranks
    #   'Introduction to Algorithms' above 'Algoritma dan Pemrograman PHP'
    if expanded_terms:
        search_term  = f"{clean_query} {' '.join(expanded_terms)}"
        rerank_query = ' '.join(expanded_terms)  # English only → correct cross-encoder scoring
    else:
        # If no expansion (query already in English), use clean_query for both
        search_term  = clean_query
        rerank_query = clean_query
    print(f"[LIBRARY SEARCH] Raw: '{req.message}' -> Clean: '{clean_query}' -> English Search: '{rerank_query}'")

    # Use English-only query for ALL three components:
    # - nomic-embed (vector) is cross-lingual: "data structures algorithms" already
    #   retrieves Indonesian books like "Konsep Struktur Data dengan C++" semantically.
    # - Including Indonesian words ("algoritma") in vector query pulls wrong books
    #   like "Data Mining Algoritma PHP" into the candidate pool unnecessarily.
    # - BM25 and Reranker (ms-marco) are English-only by design.
    raw_results = library_hybrid_search(rerank_query, limit=20, bm25_query=rerank_query)

    documents = []
    for r in raw_results:
        payload = r.get("payload", {})
        documents.append({
            "text":    payload.get("text", ""),
            "payload": payload,
            "score":   r.get("score", 0),
        })

    # Rerank with English-only query so cross-encoder (ms-marco) correctly
    # scores English-titled books higher than false positives
    ranked_docs = rerank(rerank_query, documents)
    top_docs    = ranked_docs[:5]

    # Confidence Threshold Check (Prevent forced hallucinated recommendations)
    max_score = max([doc.get("rerank_score", -999) for doc in top_docs]) if top_docs else -999
    print(f"[LIBRARY CONFIDENCE] Max Rerank Score: {max_score:.4f}")

    if max_score < -1.0:
        context = "STATUS: RELEVANSI RENDAH (TIDAK DITEMUKAN BUKU SPESIFIK TEPAT DI KATALOG).\n" + build_library_book_context(top_docs[:3])
    else:
        context = build_library_book_context(top_docs)

    prompt = build_prompt(
        query=req.message,
        context=context,
        intent=intent,
    )

    llm_stream = gateway.stream_response(
        prompt=prompt,
        model=model,
        provider=provider,
    )

    if llm_stream is None:
        yield stream_event("error", {"message": "LLM stream gagal"})
        yield stream_event("end", {"status": "failed"})
        return

    for token in llm_stream:
        yield stream_event("token", token)

    sources = []
    for idx, doc in enumerate(top_docs, start=1):
        payload = doc.get("payload", {})
        sources.append({
            "source_id": idx,
            "title":     payload.get("title", "-"),
            "author":    payload.get("author", payload.get("penulis", "-")),
            "subject":   payload.get("subject", payload.get("subjek", "-")),
            "location":  payload.get("location", payload.get("lokasi", "-")),
            "score":     round(doc.get("rerank_score", 0), 4),
        })

    yield stream_event("context_final", {"sources": sources})
    yield stream_event("end", {"status": "completed"})


# =========================================
# STREAM CHAT
# =========================================

@router.post("/chat-stream")
def chat_stream(
    req: StreamRequest,
):
    def generate():
        try:

            # =====================================
            # START
            # =====================================
            yield stream_event(
                "start",
                {
                    "status":
                        "thinking",
                },
            )

            # =====================================
            # INTENT DETECTION
            # =====================================
            intent = classify_intent(req.message)
            print(f"\n[STREAM INTENT] {intent}")

            # =====================================
            # FAQ & GREETINGS PIPELINE (Instant)
            # =====================================
            if intent == "faq":
                from delbot_platform.knowledge.library.faq import answer_faq
                faq_answer = answer_faq(req.message)
                if faq_answer:
                    yield stream_event("metadata", {"provider": "knowledge", "model": "faq_engine", "intent": "faq"})
                    yield stream_event("token", faq_answer)
                    yield stream_event("end", {"status": "completed"})
                    return

            # =====================================
            # LIBRARY PIPELINE (recommendation)
            # =====================================
            if intent == "recommendation":
                yield from _run_library_pipeline(
                    req=req,
                    intent=intent,
                )
                return

            # =====================================
            # RESEARCH PIPELINE (semua intent lain)
            # =====================================
            agent = ResearchAgent()
            context, llm_stream = agent.run(
                query=req.message,
                session_id=req.session_id or "",
                active_document_ids=req.active_document_ids,
                stream=True,
            )

            # =====================================
            # METADATA
            # =====================================
            yield stream_event(
                "metadata",
                {
                    "provider":
                        context.provider,
                    "model":
                        context.model,
                    "intent":
                        context.intent,
                },

            )

            # =====================================
            # SPECIALIZED RESPONSE
            # =====================================
            if context.response is not None:
                specialized_response = context.response
                yield stream_event(
                    "context",
                    specialized_response,
                )
                if isinstance(specialized_response, str):
                    analysis = specialized_response
                elif isinstance(specialized_response, dict):
                    analysis = (
                        specialized_response.get("ideas")
                        or specialized_response.get("analysis")
                        or specialized_response.get("literature_review")
                        or specialized_response.get("gap_report")
                        or specialized_response.get("novelty_check")
                        or specialized_response.get("method_comparison")
                        or specialized_response.get("detail_explanation")
                        or ""
                    )
                else:
                    analysis = str(specialized_response)

                if analysis:
                    yield stream_event(
                        "token",
                        analysis,
                    )

                # =================================
                # PERSIST SPECIALIZED ASSISTANT
                # =================================
                assistant_content = (
                    persist_stream_assistant(
                        context=context,
                        response=(
                            specialized_response
                        ),
                    )
                )

                # =================================
                # PERSIST SPECIALIZED EXECUTION
                # =================================
                persist_stream_execution(
                    context=context,
                    response_content=(
                        assistant_content
                    ),
                )
                yield stream_event(
                    "context_final",
                    specialized_response,
                )
                yield stream_event(
                    "end",
                    {
                        "status":
                            "completed",
                    },
                )
                return

            # =====================================
            # INITIAL CONTEXT
            # =====================================
            initial_context = (
                serialize_research_context(
                    context
                )
            )
            yield stream_event(
                "context",
                initial_context,
            )

            # =====================================
            # STREAM VALIDATION
            # =====================================
            if llm_stream is None:
                raise RuntimeError(
                    "Research pipeline completed "
                    "without a response or LLM stream."
                )

            # =====================================
            # TOKEN STREAM
            # =====================================
            analysis_chunks = []
            for token in llm_stream:
                analysis_chunks.append(
                    token
                )
                yield stream_event(
                    "token",
                    token,
                )

            # =====================================
            # FINAL ANALYSIS
            # =====================================
            context.analysis = "".join(
                analysis_chunks
            )

            # =====================================
            # PERSIST STREAMED ASSISTANT
            # =====================================
            assistant_content = (
                persist_stream_assistant(
                    context=context,
                    response={
                        "analysis":
                            context.analysis,
                    },
                )
            )

            # =====================================
            # PERSIST STREAMED EXECUTION
            # =====================================
            persist_stream_execution(
                context=context,
                response_content=(
                    assistant_content
                ),
            )

            # =====================================
            # FINAL CONTEXT
            # =====================================
            final_context = (
                serialize_research_context(
                    context
                )
            )
            yield stream_event(
                "context_final",
                final_context,
            )

            # =====================================
            # END
            # =====================================
            yield stream_event(
                "end",
                {
                    "status":
                        "completed",
                },
            )
        except Exception as exc:
            yield stream_event(
                "error",
                {
                    "status":
                        "failed",
                    "message":
                        str(exc),
                    "exception_type":
                        type(exc).__name__,
                },
            )

    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson",

    )