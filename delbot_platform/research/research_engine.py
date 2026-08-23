from __future__ import annotations

from delbot_platform.ai.client.llm_client import LLMClient
from delbot_platform.knowledge.models import (
    RAGResult,
)
from delbot_platform.knowledge.rag.rag_engine import RAGEngine
from delbot_platform.research.builders.research_result_builder import (
    ResearchResultBuilder,
)
from delbot_platform.research.memory.research_memory import (
    ResearchMemory,
)
from delbot_platform.research.models import Citation
from delbot_platform.research.models import ResearchResult
from delbot_platform.research.prompts.prompt_builder import (
    ResearchPromptBuilder,
)
from delbot_platform.workspace.session_manager import (
    SessionManager,
)


class ResearchEngine:

    def __init__(
        self,
        session_manager: SessionManager,
    ) -> None:

        self.sessions = session_manager
        self.rag = RAGEngine()
        self.llm = LLMClient()
        self.builder = ResearchPromptBuilder()
        self.result_builder = ResearchResultBuilder()
        self.memory = ResearchMemory()

    def ask(
        self,
        session_id: str,
        query: str,
        history: list[dict] | None = None,
    ) -> ResearchResult:

        history = history or []

        session = self.sessions.get_object(
            session_id
        )

        if session is None:

            raise ValueError(
                f"Session '{session_id}' not found."
            )

        state = session.research_state

        state.update_question(
            query
        )

        rag_result: RAGResult = (
            self.rag.search(
                query
            )
        )

        context = rag_result.context

        citations: list[Citation] = (
            rag_result.citations
        )

        memory = self.memory.load(
            session_id
        )

        messages = self.builder.build(
            query=query,
            context=context,
            history=history,
            previous=memory.get(
                "last_answer",
                "",
            ),
            research_state=state.export(),
        )

        answer = self.llm.chat(
            messages
        )

        state.update_answer(
            answer
        )

        for citation in citations:

            state.add_source(
                citation
            )

        self.sessions.replace_state(
            session_id,
            state,
        )

        exported_state = state.export()

        self.memory.save(
            session_id=session_id,
            query=query,
            answer=answer,
            research_state=exported_state,
            summary=exported_state.get(
                "summary",
                "",
            ),
            keywords=exported_state.get(
                "keywords",
                [],
            ),
            sources=exported_state.get(
                "sources",
                [],
            ),
            notes=exported_state.get(
                "notes",
                [],
            ),
            timeline=exported_state.get(
                "timeline",
                [],
            ),
        )

        return self.result_builder.build(
            answer=answer,
            citations=citations,
            research_state=exported_state,
        )

from delbot_platform.research.models.research_models import ResearchContext
from delbot_platform.research.session import session_manager
from delbot_platform.research.search_engine import run_search
from delbot_platform.research.generators.analysis_engine import run_analysis
from delbot_platform.research.generators.thesis_idea_generator import generate_thesis_ideas
from delbot_platform.research.generators.literature_review_generator import generate_literature_review
from delbot_platform.research.generators.research_gap_generator import generate_research_gap_report
from delbot_platform.research.generators.corpus_novelty_generator import generate_corpus_novelty_check
from delbot_platform.research.generators.method_comparison_generator import generate_method_comparison

# =====================================
# SERIALIZER RESEARCH CONTEXT
# =====================================
def serialize_research_context(context: ResearchContext) -> dict:
    profile = context.research_profile.to_dict()
    return {
        "schema": {
            "name": "research_context",
            "version": 1,
        },
        "query": context.query,
        "mode": context.mode,
        "provider": context.provider,
        "model": context.model,
        "intent": context.intent,
        "analysis": context.analysis,
        "research_profile": profile,
        "sources": context.theses,
        "citations": context.citations,
        "evidence": context.evidence,
        "evidence_matrix": context.evidence_matrix,
        "pipeline": {
            "stages": {
                "simplification": {
                    "success": True,
                    "duration_ms": 0,
                    "message": "Linear simplified pipeline executed successfully",
                    "metadata": {}
                }
            }
        }
    }

# =====================================
# HELPERS FOR SESSION
# =====================================
def extract_assistant_content(response) -> str:
    if isinstance(response, str):
        return response.strip()
    if not isinstance(response, dict):
        return ""
    candidates = [
        response.get("response"),
        response.get("analysis"),
        response.get("ideas"),
        response.get("answer"),
        response.get("comparison"),
    ]
    for content in candidates:
        if isinstance(content, str) and content.strip():
            return content.strip()
    return ""

def persist_assistant_response(session, response, citations=None, sources=None) -> str:
    assistant_content = extract_assistant_content(response)
    if assistant_content:
        session.conversation.append(
            role="assistant",
            content=assistant_content,
            citations=citations or [],
            sources=sources or [],
        )
    return assistant_content

def persist_execution_snapshot(session, context: ResearchContext, response_content: str = "") -> dict:
    serialized_context = serialize_research_context(context)
    session.execution.update(
        context=context,
        serialized_context=serialized_context,
        response_content=response_content
    )
    return serialized_context

# =====================================
# CORE LINIER PIPELINE ENTRYPOINT
# =====================================
def research_analysis(
    query: str,
    session_id: str = "",
    top_k: int = 10,
    mode: str = "analysis",
    active_document_ids=None,
    stream: bool = False,
):
    print("\n====================================")
    print("RESEARCH ENGINE (LINIER SIMPLIFIED)")
    print("====================================")

    # 1. Resolve Session & History
    session = session_manager.get_or_create(session_id)
    conversation_history = session.conversation.build_history()
    session.conversation.append(role="user", content=query)

    # 1b. Topic Shift & Follow-up State Management
    msg_clean = query.lower().strip()
    
    # Deteksi eksplisit apakah ini pertanyaan follow-up/lanjutan (misal: "lagi", "tambahkan ide lagi", "lanjutkan", "jelaskan ide nomor 2", "metodologi")
    followup_intent_keywords = [
        "tambahkan", "lanjutkan", "lagi", "ide lain", "ide lainnya",
        "berikan lagi", "minta lagi", "coba lagi", "buat lagi",
        "kurang relevan", "cari lagi yang lain", "opsi lain",
        "jelaskan", "detail", "metodologi", "algoritma", "ide nomor", "ide no",
        "ide 1", "ide 2", "ide 3", "ide 4", "ide 5", "uraikan", "rincian", "draf",
        "bab 1", "bab 3", "bagaimana"
    ]
    
    from delbot_platform.research.search_engine import is_contextual_followup
    is_detail_request = any(kw in msg_clean for kw in ["jelaskan", "detail", "metodologi", "algoritma", "ide nomor", "ide no", "uraikan", "rincian", "draf", "bab 1", "bab 3"])
    is_followup_query = (
        (len(msg_clean.split()) <= 15 and any(kw in msg_clean for kw in followup_intent_keywords))
        or is_detail_request
        or is_contextual_followup(query)
    )

    prior_intent = None
    clarification_markers = ["boleh tahu program studi anda", "pilihan mana yang anda minati", "spesifik jurusan atau topiknya", "kategori", "sebutkan mata kuliah"]
    last_assistant_msg = ""
    for msg in reversed(session.conversation.messages):
        if msg.role == "assistant":
            last_assistant_msg = msg.content.lower()
            break

    is_answering_clarification = any(cm in last_assistant_msg for cm in clarification_markers)

    if (is_followup_query or is_answering_clarification) and conversation_history:
        thesis_idea_markers = [
            "**judul**", "**research gap**", "**pendekatan yang disarankan**",
            "**saran data penelitian**", "ide 1", "ide 2", "ide 3", "ide 4", "ide 5",
            "research gap analysis", "celah riset", "sintesis penelitian"
        ]
        conversation_history_lc = conversation_history.lower()
        if is_answering_clarification or any(marker in conversation_history_lc for marker in thesis_idea_markers):
            prior_intent = "detail_explanation" if is_detail_request else "thesis_idea"

    if prior_intent in ["thesis_idea", "detail_explanation"] or is_contextual_followup(query):
        session.last_intent = prior_intent
        session.followup_count = getattr(session, "followup_count", 0) + 1
        print(f"[RESEARCH_ENGINE] Follow-up/Clarification response query ({prior_intent}) #{session.followup_count} detected.")
    else:
        # Kueri baru/topik baru — reset penuh counter & theses agar tidak tertimpa/tercampur
        print("[RESEARCH_ENGINE] New search query detected. Performing fresh retrieval.")
        session.last_intent = ""
        session.followup_count = 0
        if hasattr(session, "used_titles"):
            session.used_titles.clear()
        if hasattr(session, "all_theses"):
            session.all_theses = []
        if hasattr(session, "original_topic"):
            session.original_topic = ""

    # Tentukan query pencarian (jika follow-up murni, gunakan query awal; jika kueri baru, gunakan kueri baru)
    search_query = query
    is_followup = (prior_intent in ["thesis_idea", "detail_explanation"] or is_contextual_followup(query))
    if is_followup:
        original_topic = getattr(session, "original_topic", "")
        if original_topic:
            search_query = original_topic
            print(f"[RESEARCH_ENGINE] Resolved original topic from session.original_topic: {search_query!r}")
        elif session.conversation.messages:
            for msg in session.conversation.messages:
                if msg.role == "user" and msg.content != query:
                    content = msg.content
                    if not is_contextual_followup(content):
                        search_query = content
                        session.original_topic = content
                        print(f"[RESEARCH_ENGINE] Resolved original topic from history: {search_query!r}")
                        break
    else:
        session.original_topic = query
        print(f"[RESEARCH_ENGINE] Stored original topic query: {query!r}")

    # 2. Inisialisasi Context
    context = ResearchContext(
        query=search_query,  # Gunakan query pencarian asli untuk penarikan RAG
        session_id=session.session_id,
        top_k=top_k,
        mode=mode,
        active_document_ids=(active_document_ids or []),
        conversation_history=conversation_history,
    )

    # 3. Task Query Routing
    from delbot_platform.orchestration.task_router import route_query
    routing = route_query(query, session_id=session.session_id)
    context.intent = routing.get("intent", "")
    context.provider = routing.get("provider", "")
    context.model = routing.get("model", "")
    
    # Mode overrides based on intent detection & contextual follow-up
    from delbot_platform.research.search_engine import is_contextual_followup
    if is_contextual_followup(query):
        print(f"[RESEARCH ENGINE] Contextual follow-up query detected: '{query}'. Overriding intent to 'thesis_idea'.")
        context.intent = "thesis_idea"
        context.mode = "thesis_idea"
    elif context.intent in ["thesis_idea", "literature_review"]:
        context.mode = context.intent

    # 3.5. Information Completeness Check (Clarification Agent)
    is_direct_research_query = context.intent in [
        "research_gap", "literature_review", "methodology", "methodology_comparison", "technical"
    ] or any(kw in query.lower() for kw in ["research gap", "gap penelitian", "klasifikasi", "cnn", "deep learning", "penyakit kulit"])

    is_generating_ideas = (
        (context.intent in ["thesis_idea", "title_generation"] or context.mode in ["thesis_idea"])
        and not is_direct_research_query
        and not is_contextual_followup(query)
    )
    if is_generating_ideas:
        from delbot_platform.orchestration.completeness_checker import check_information_completeness
        session_prodi = getattr(session, "prodi", "")
        eval_query = f"{query} {search_query}".strip() if query != search_query else search_query
        completeness = check_information_completeness(eval_query, conversation_history, session_prodi=session_prodi)
        if not completeness.get("is_complete", True):
            print(f"[RESEARCH_ENGINE] Query incomplete. Requesting clarification.")
            clarification_text = completeness.get("clarification", "Boleh tahu spesifik jurusan atau topiknya?")
            
            # Short-circuit and return clarification directly without RAG or Ideation
            context.response = clarification_text
            
            if stream:
                def clarification_stream():
                    yield clarification_text
                return context, clarification_stream()
                
            persist_assistant_response(session=session, response=context.response)
            return context.response
        else:
            # Sticky Program Studi Binding (Bind detected prodi to ResearchContext & Session)
            meta = completeness.get("metadata", {})
            if meta.get("prodi"):
                context.prodi = meta["prodi"]
                context.requested_prodi = meta["prodi"]
                session.prodi = meta["prodi"]
                print(f"[RESEARCH_ENGINE] Sticky Prodi Bound to Context & Session: '{context.prodi}'")

    # 4. Pencarian RAG (Search Engine)
    try:
        context = run_search(context)
    except Exception as e:
        print(f"[RESEARCH_ENGINE ERROR] Search pipeline failed: {e}")
        context.theses = []
        context.citations = []
        context.evidence = ""
        context.evidence_matrix = []
        context.analysis = ""
        context.search_error = str(e)
        print("[RESEARCH_ENGINE] Continuing with thesis idea generation using fallback data.")

    # 5. Eksekusi Berdasarkan Intent
    if prior_intent == "detail_explanation":
        print("[RESEARCH_ENGINE] Executing direct detail/explanation for requested thesis idea...")
        detail_prompt = f"""
Anda adalah DELBot Academic Agent.
Pengguna meminta penjelasan lebih detail / draf penyusunan mengenai salah satu ide skripsi dari percakapan sebelumnya.

Riwayat Obrolan & Ide Skripsi Sebelumnya:
{conversation_history}

Pertanyaan/Permintaan Detail Pengguna:
"{query}"

Tugas Utama Anda:
1. Temukan ide skripsi yang dimaksud oleh pengguna (misal: Ide Nomor 1, Nomor 2, dst) dari Riwayat Obrolan di atas.
2. Rancang dan tuliskan penjelasan detail metodologi dan arsitektur yang **SPESIFIK dan RELEVAN** dengan topik ide skripsi tersebut.
3. JANGAN menggunakan arsitektur agen internal DELBot (seperti Intent Detection, Task Planner, Executor, dll) kecuali jika ide skripsi tersebut memang bertema 'Agentic AI' atau 'Multi-Agent System'.
4. Sesuaikan diagram ASCII dan poin penjelasan dengan domain penelitian (misal: jika klasifikasi citra deep learning, gunakan pipeline pengolahan citra; jika federated learning, gunakan alur desentralisasi; jika sistem perangkat lunak, gunakan diagram arsitektur sistem).

FORMAT TANGGAPAN WAJIB (MUTLAK AKADEMIS & DEFENSIP UNTUK SIDANG SKRIPSI):

---
### 📌 Penjelasan Rinci Metodologi & Algoritma untuk Ide Nomor [Nomor Ide dari Kueri Pengguna]

**Judul Skripsi:** [Tuliskan Judul Ide yang Diminta dari Riwayat Obrolan]

1. **Diagram Arsitektur Penelitian / Arsitektur Sistem (ASCII Flow Diagram)**
   Tampilkan alur logika dan data dalam bentuk diagram ASCII yang relevan dengan topik penelitian (misal: alur preprocessing citra, ekstraksi fitur model, hingga klasifikasi akhir).
   Contoh alur klasifikasi citra deep learning:
   ```text
   [Dataset] -> [Preprocessing & Normalization] -> [Data Augmentation] -> [Backbone/Feature Extractor] -> [Loss Function/Classifier] -> [Output Diagnosis]
   ```

2. **Tahap 1: Pengolahan Data & Pra-pemrosesan (Data Preparation & Preprocessing)**
   - Rincian dataset yang digunakan (misal: BraTS, ISIC, CBIS-DDSM) dan pembagian data (train/validation/test split).
   - Tahapan preprocessing yang realistis (resizing, histogram equalization, scaling intensitas piksel, atau handling imbalanced data).

3. **Tahap 2: Rincian Arsitektur Model/Algoritma & Justifikasi Teknis**
   - Bedah komponen utama model/arsitektur (misal: jika Vision Transformer, jelaskan Patch Embedding, Transformer Encoder, Multi-Head Self-Attention, MLP Head).
   - Berikan alasan teknis ilmiah pemilihan arsitektur dan komponen pendukungnya (misal: "Vision Transformer dipilih karena kemampuannya menangkap hubungan spasial jarak jauh antar wilayah piksel citra secara global...").

4. **Tahap 3: Rencana Pelatihan & Evaluasi Kinerja (Training & Evaluation)**
   - Jelaskan skenario training (optimizer, learning rate, batch size, epochs, dan loss function).
   - Tentukan metrik evaluasi teknis terukur yang relevan (misal: Accuracy, Precision, Recall, F1-Score, AUC-ROC, atau Dice Similarity Coefficient untuk segmentasi).

---
📌 **Catatan:** Penjelasan rincian metodologi dan algoritma untuk Ide Nomor [Nomor Ide] telah selesai disajikan di atas. Apakah Anda ingin saya membuatkan **Draf Bab 1 (Pendahuluan)** atau **Draf Bab 3 (Metodologi Penelitian)** secara utuh?
---
"""
        from delbot_platform.ai.llm.model_gateway import gateway
        from delbot_platform.core.config import settings
        if stream:
            context.llm_stream = gateway.stream_response(prompt=detail_prompt, model=settings.DEFAULT_LLM, max_tokens=4096)
            context.response = None
        else:
            detail_response = gateway.generate_response(prompt=detail_prompt, model=settings.DEFAULT_LLM, max_tokens=4096)
            context.response = {
                "detail_explanation": (detail_response or "").strip(),
                "theses": context.theses
            }
    elif context.intent == "novelty_check":
        # Panggil LLM Generator Status Repositori Skripsi IT Del (Novelty Check)
        context = generate_corpus_novelty_check(context)
    elif context.intent == "research_gap":
        # Panggil LLM Generator Laporan Research Gap Teragregasi (Sintesis Bukti)
        context = run_analysis(context)
        context = generate_research_gap_report(context)
        try:
            session.last_research_gap = context.response
            print(f"[RESEARCH ENGINE] Stored generated research gap report on session: {len(context.response)} chars.")
        except Exception as e:
            print(f"[RESEARCH ENGINE ERROR] Failed to store research gap on session: {e}")
    elif context.intent in ["methodology_comparison", "methodology"]:
        # Panggil LLM Generator Komparasi & Analisis Metodologi
        context = generate_method_comparison(context)
    elif context.intent == "thesis_idea" or context.mode == "thesis_idea" or context.mode == "analysis":
        # Jalankan Analisis Data (Tren, Gap, Novelty, Kompetensi)
        context = run_analysis(context)
        # Panggil LLM Generator Ide Skripsi
        context = generate_thesis_ideas(context)
    elif context.intent == "literature_review" or context.mode == "literature_review":
        # Panggil LLM Tinjauan Pustaka
        context = generate_literature_review(context)
    else:
        # Fallback default ide skripsi
        context = run_analysis(context)
        context = generate_thesis_ideas(context)

    # Simpan used_titles agar tidak duplikat di follow-up berikutnya
    try:
        used_titles = getattr(session, "used_titles", set())
        for t in context.theses:
            t_title = t.get("title", "").strip().lower()
            if t_title:
                used_titles.add(t_title)
        session.used_titles = used_titles
    except Exception as e:
        print(f"[SESSION ERROR] Failed to update used_titles: {e}")

    # 6. Stream Response Handling
    if stream:
        return context, context.llm_stream

    # 7. Persist Sesi & Simpan Snapshot
    import re
    from delbot_platform.research.search_engine import build_citations
    
    # Response text extraction
    raw_response = context.response or context.analysis
    assistant_content = extract_assistant_content(raw_response)
    if not assistant_content and isinstance(raw_response, str):
        assistant_content = raw_response.strip()
    if not assistant_content and context.analysis:
        assistant_content = context.analysis.strip()
    if not assistant_content and isinstance(context.response, str):
        assistant_content = context.response.strip()

    context.response = assistant_content

    # Extract all citation IDs referenced in assistant_content (e.g. [1], [3], [5])
    raw_citations = getattr(context, "citations", []) or build_citations(getattr(context, "theses", []))
    cited_ids = set(int(x) for x in re.findall(r"\[(\d+)\]", assistant_content))

    if cited_ids:
        citations_data = [c for c in raw_citations if c.get("source_id") in cited_ids or c.get("id") in cited_ids]
        if not citations_data:
            citations_data = raw_citations[:8]
    else:
        citations_data = raw_citations[:8]

    sources_data = citations_data

    persist_assistant_response(
        session=session,
        response=assistant_content,
        citations=citations_data,
        sources=sources_data
    )
    persist_execution_snapshot(session=session, context=context, response_content=assistant_content)

    return {
        "response": assistant_content,
        "citations": citations_data,
        "sources": sources_data,
        "theses": context.theses
    }