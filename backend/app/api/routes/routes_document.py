from fastapi import APIRouter

from pydantic import BaseModel

from app.services.document.session_store import (
    ACTIVE_DOCUMENTS
)

from app.services.llm.model_gateway import (
    gateway
)

from app.services.document.document_chunk_retriever import (
    retrieve_relevant_chunks
)

from app.services.document.document_intent import (
    detect_document_intent
)

from app.services.document.document_chat_memory import (
    get_document_history,
    append_document_history
)

router = APIRouter()


class DocumentChatRequest(
    BaseModel
):
    document_id: str
    question: str


@router.post(
    "/document/chat"
)
async def document_chat(
    request: DocumentChatRequest
):

    # =====================================
    # LOAD DOCUMENT
    # =====================================

    document = (
        ACTIVE_DOCUMENTS.get(
            request.document_id
        )
    )

    if not document:

        return {

            "answer":
            "Dokumen tidak ditemukan."
        }

    # =====================================
    # DOCUMENT CONTENT
    # =====================================

    content = document["content"]

    pages = document.get(
        "pages_data",
        []
    )

    # =====================================
    # DOCUMENT MEMORY
    # =====================================

    history = get_document_history(
        request.document_id
    )

    history_text = "\n".join([

        f"{item['role']}: {item['content']}"

        for item in history

    ])

    # =====================================
    # DETECT INTENT
    # =====================================

    intent = detect_document_intent(
        request.question
    )

    # =====================================
    # RETRIEVE RELEVANT CHUNKS
    # =====================================

    chunks = retrieve_relevant_chunks(

        pages=pages,

        query=request.question,

        top_k=8

    )

    context = "\n\n".join([

        f"[PAGE {chunk['page']}]\n"
        f"{chunk['text']}"

        for chunk in chunks

    ])

    # fallback jika pages_data kosong
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
Ekstrak seluruh file, dokumen,
proposal, presentasi, video,
atau submission yang wajib dikumpulkan.

Kelompokkan berdasarkan tahap kompetisi.
"""

    else:

        instruction = """
Jawab pertanyaan pengguna
berdasarkan isi dokumen.

Gunakan informasi yang tersedia
pada dokumen dan konteks percakapan.
"""

    # =====================================
    # SAVE USER MESSAGE
    # =====================================

    append_document_history(

        request.document_id,

        "user",

        request.question

    )

    # =====================================
    # PROMPT
    # =====================================

    prompt = f"""
Anda adalah DELBot.

Dokumen berikut sedang dibahas
oleh pengguna.

================================================

RIWAYAT PERCAKAPAN

{history_text}

================================================

KONTEN DOKUMEN RELEVAN

{context}

================================================

Intent:
{intent}

Pertanyaan:
{request.question}

================================================

Instruksi:

{instruction}

================================================

ATURAN:

1. Jawab hanya berdasarkan isi dokumen.

2. Gunakan konteks percakapan sebelumnya
jika relevan.

3. Jangan gunakan Qdrant.

4. Jangan gunakan repository skripsi.

5. Jangan mengarang informasi.

6. Jika informasi tidak ditemukan,
katakan bahwa informasi tidak ditemukan
dalam dokumen.

7. Gunakan Bahasa Indonesia.

8. Gunakan format yang rapi,
terstruktur,
dan mudah dibaca.

9. Jika pengguna meminta timeline,
gunakan tabel markdown.

10. Jika pengguna meminta checklist,
gunakan checklist markdown.

11. Jika informasi ditemukan
dalam dokumen,
cantumkan sumber halaman
dalam format:

(Halaman X)

12. Jika informasi berasal dari
beberapa halaman,
cantumkan semuanya.

Contoh:

(Halaman 3)

atau

(Halaman 3, 5, 8)

================================================
"""

    # =====================================
    # GENERATE ANSWER
    # =====================================

    answer = (
        gateway.generate_response(
            prompt=prompt
        )
    )

    # =====================================
    # SAVE ASSISTANT MESSAGE
    # =====================================

    append_document_history(

        request.document_id,

        "assistant",

        answer

    )

    # =====================================
    # RESPONSE
    # =====================================

    return {

        "answer":
        answer,

        "filename":
        document["filename"],

        "intent":
        intent,

        "retrieved_chunks":
        len(chunks),

        "memory_messages":
        len(
            get_document_history(
                request.document_id
            )
        )
    }