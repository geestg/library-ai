from fastapi import APIRouter

from pydantic import BaseModel

from app.services.document.session_store import (
    ACTIVE_DOCUMENTS
)

from app.services.llm.model_gateway import (
    gateway
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

    content = (
        document["content"]
    )

    prompt = f"""
Anda adalah DELBot.

Dokumen berikut sedang
dibahas oleh pengguna.

================================================

{content[:15000]}

================================================

Pertanyaan:

{request.question}

================================================

ATURAN:

1. Jawab hanya berdasarkan
isi dokumen.

2. Jangan gunakan
Qdrant.

3. Jangan gunakan
repository skripsi.

4. Jangan mengarang.

5. Jika informasi tidak ada
dalam dokumen, katakan bahwa
informasi tidak ditemukan.

6. Gunakan Bahasa Indonesia.

================================================
"""

    answer = (
        gateway.generate_response(
            prompt=prompt
        )
    )

    return {

        "answer":
        answer,

        "filename":
        document["filename"]
    }