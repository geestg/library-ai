from app.services.document.session_store import (
    ACTIVE_DOCUMENTS
)

from app.services.llm.model_gateway import (
    gateway
)


# =====================================
# BUILD DOCUMENT CONTEXT
# =====================================

def build_document_context(
    active_document_ids: list
):

    contexts = []

    documents = []

    for doc_id in active_document_ids:

        doc = ACTIVE_DOCUMENTS.get(
            doc_id
        )

        if not doc:
            continue

        documents.append({

            "document_id":
            doc_id,

            "filename":
            doc["filename"]
        })

        contexts.append(

            f"""
FILE:
{doc["filename"]}

CONTENT:
{doc["content"][:10000]}
"""
        )

    return {

        "documents":
        documents,

        "context":
        "\n\n".join(
            contexts
        )
    }


# =====================================
# BUILD PROMPT
# =====================================

def build_document_prompt(
    query: str,
    document_context: str
):

    return f"""
Anda adalah DELBot.

Anda sedang menganalisis
beberapa dokumen sekaligus.

==================================================
DOKUMEN
==================================================

{document_context}

==================================================
PERTANYAAN USER
==================================================

{query}

==================================================
ATURAN
==================================================

1. Jawab berdasarkan dokumen yang diberikan.

2. Jika informasi berasal dari dokumen tertentu,
sebutkan nama filenya.

3. Jika terdapat informasi yang berbeda antar dokumen,
jelaskan perbedaannya.

4. Jika user meminta perbandingan,
buat tabel perbandingan.

5. Jika user meminta ringkasan,
buat ringkasan terstruktur.

6. Jika informasi tidak ditemukan,
katakan informasi tidak ditemukan.

7. Jangan gunakan Qdrant.

8. Jangan gunakan repository skripsi.

9. Jangan mengarang.

10. Gunakan Bahasa Indonesia.
"""
    

# =====================================
# DOCUMENT ANALYSIS
# =====================================

def run_document_analysis(
    query: str,
    active_document_ids: list
):

    document_result = (
        build_document_context(
            active_document_ids
        )
    )

    document_context = (
        document_result[
            "context"
        ]
    )

    documents = (
        document_result[
            "documents"
        ]
    )

    if not document_context:

        return None

    prompt = build_document_prompt(

        query=query,

        document_context=
        document_context
    )

    answer = (
        gateway.generate_response(
            prompt=prompt
        )
    )

    return {

        "query":
        query,

        "mode":
        "multi_document",

        "analysis":
        answer,

        "citations":
        [],

        "evidence":
        {},

        "documents":
        documents
    }