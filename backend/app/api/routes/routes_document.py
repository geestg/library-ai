from fastapi import APIRouter
from fastapi import HTTPException

from pydantic import BaseModel

from app.services.research.session import (
    session_manager,
)

from app.services.document.document_chunk_retriever import (
    retrieve_relevant_chunks,
)

from app.services.document.document_intent import (
    detect_document_intent,
)

from app.services.llm.tasks.llm_task import (
    LLMTask,
)

from app.services.prompts.models.prompt_request import (
    PromptRequest,
)

from app.services.prompts.models.prompt_type import (
    PromptType,
)


router = APIRouter()


# =====================================
# REQUEST MODEL
# =====================================

class DocumentChatRequest(
    BaseModel
):

    session_id: str

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

    session = session_manager.get(
        session_id
    )

    if session is None:

        raise HTTPException(

            status_code=404,

            detail="Session not found",

        )

    documents = (
        session.documents.list_documents()
    )

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

    session = session_manager.get(
        request.session_id
    )

    if session is None:

        raise HTTPException(

            status_code=404,

            detail="Session not found",

        )

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

    content = document.content

    pages = document.pages_data

    filename = document.filename

    intent = detect_document_intent(
        request.question
    )

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

    if not context.strip():

        context = content[:15000]

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

    llm_request = PromptRequest(

        prompt=prompt,

        prompt_type=PromptType.ANSWER,
model=None,

        provider=None,

    )

    answer = LLMTask.answer(
        llm_request
    )

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



