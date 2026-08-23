from fastapi import APIRouter
from fastapi import HTTPException

from pydantic import BaseModel

from delbot_platform.research.session import (
    session_manager,
)

from delbot_platform.ai.llm.model_gateway import (
    gateway,
)

from delbot_platform.document.services.document_chunk_retriever import (
    retrieve_relevant_chunks,
)

from delbot_platform.document.services.document_intent import (
    detect_document_intent,
)
router = APIRouter()


# =====================================
# REQUEST MODEL
# =====================================
class DocumentChatRequest(
    BaseModel
):
    session_id: str = "chat_session"
    document_id: str
    question: str


# =====================================
# LIST SESSION DOCUMENTS
# =====================================
@router.get(
    "/session/{session_id}/documents"
)
async def list_session_documents(
    session_id: str,
):

    # =====================================
    # LOAD SESSION
    # =====================================
    session = session_manager.get(
        session_id
    )
    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found",

        )

    # =====================================
    # LOAD OWNED DOCUMENTS
    # =====================================
    documents = (
        session.documents.list_documents()
    )

    # =====================================
    # RESPONSE
    # =====================================
    return {
        "session_id":
            session.session_id,
        "documents": [
            {
                "document_id":
                    document.document_id,
                "filename":
                    document.filename,
                "file_type":
                    document.file_type,
                "pages":
                    document.pages,
                "chunks":
                    document.chunks,
            }
            for document in documents
        ],

        "total_documents":
            len(documents),

    }


# =====================================
# DOCUMENT CHAT
# =====================================
@router.post("/document/chat")
async def document_chat(
    request: DocumentChatRequest
):

    # =====================================
    # LOAD SESSION (AUTO-CREATE IF NOT EXISTS)
    # =====================================
    session = session_manager.get_or_create(
        request.session_id
    )

    # =====================================
    # LOAD OWNED DOCUMENT
    # =====================================
    document = (
        session.documents.get_document(
            request.document_id
        )
    )
    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    # =====================================
    # DOCUMENT CONTENT
    # =====================================
    content = (
        document.content
    )
    pages = (
        document.pages_data
    )
    filename = (
        document.filename
    )

    # =====================================
    # DETECT INTENT
    # =====================================
    intent = detect_document_intent(
        request.question
    )

    # =====================================
    # RETRIEVE CHUNKS
    # =====================================
    chunks = retrieve_relevant_chunks(
        pages=pages,
        query=request.question,
        top_k=8,
    )

    context = "\n\n".join(
        [
            f"[PAGE {chunk['page']}]\n"
            f"{chunk['text']}"
            for chunk in chunks
        ]

    )

    # =====================================
    # FALLBACK
    # =====================================
    if not context.strip():
        context = content[:15000]

    # =====================================
    # INTENT INSTRUCTION
    # =====================================
    if intent == "summary":
        instruction = """
Buat ringkasan dokumen.
Gunakan heading.
Gunakan bullet point.
Fokus pada poin penting.
Jangan menambahkan informasi yang tidak ada dalam dokumen.
"""

    elif intent == "timeline":
        instruction = """
Ekstrak seluruh timeline yang ditemukan.
Susun berdasarkan urutan tanggal.
Gunakan format tabel markdown.
Jika terdapat rentang tanggal,
tetap tampilkan secara lengkap.
"""

    elif intent == "requirements":

        instruction = """
Ekstrak seluruh syarat dan ketentuan.
Susun dalam bentuk checklist.
Kelompokkan berdasarkan kategori jika memungkinkan.
"""

    elif intent == "checklist":
        instruction = """
Buat checklist tindakan yang harus dilakukan pengguna.
Gunakan format checklist markdown.
Fokus pada hal-hal yang perlu dipersiapkan.
"""

    elif intent == "deliverables":
        instruction = """
Ekstrak seluruh file,
dokumen,
proposal,
presentasi,
video,
atau submission
yang wajib dikumpulkan.

Kelompokkan berdasarkan tahap kompetisi.
"""

    else:
        instruction = """
Jawab pertanyaan pengguna
berdasarkan isi dokumen.

Gunakan informasi yang tersedia
pada dokumen.
"""

    # =====================================
    # PROMPT
    # =====================================
    prompt = f"""
Anda adalah DELBot.
Dokumen berikut sedang dibahas.

================================================
KONTEN DOKUMEN
{context}
================================================

Intent:
{intent}

Pertanyaan:
{request.question}

================================================

Instruksi
{instruction}

================================================

ATURAN
1. Jawab hanya berdasarkan isi dokumen.
2. Jangan menggunakan Qdrant.
3. Jangan menggunakan repository skripsi.
4. Jangan mengarang informasi.
5. Bila informasi tidak ditemukan,
katakan bahwa informasi tersebut
tidak ada di dokumen.
6. Gunakan Bahasa Indonesia.
7. Gunakan format yang rapi.
8. Jika diminta timeline,
gunakan tabel markdown.
9. Jika diminta checklist,
gunakan checklist markdown.
10. Jika informasi ditemukan,
cantumkan halaman.
================================================
"""

    # =====================================
    # GENERATE
    # =====================================
    from delbot_platform.core.config import settings
    answer = gateway.generate_response(
        prompt=prompt,
        model=settings.DEFAULT_LLM,
        max_tokens=800
    )

    # =====================================
    # RESPONSE
    # =====================================
    return {
        "answer":
            answer,
        "filename":
            filename,
        "intent":
            intent,
        "retrieved_chunks":
            len(chunks),
    }