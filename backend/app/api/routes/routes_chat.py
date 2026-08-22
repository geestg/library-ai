from fastapi import APIRouter, Header
from pydantic import BaseModel

from app.services.library.agent import LibraryAcademicAgent
from app.services.librarian.agent import LibraryLibrarianAgent
from app.core.guardrails import validate_query_safety


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
    from app.services.research.session import session_manager
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

        from app.services.research.session import session_manager
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

            from app.services.research.research_service import research_analysis
            from app.services.research.research_engine import extract_assistant_content
            
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
                from app.services.research.search_engine import build_citations
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

