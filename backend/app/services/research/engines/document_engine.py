from app.services.document.session_store import (
    ACTIVE_DOCUMENTS,
)

from app.services.llm.model_gateway import (
    gateway,
)


# =====================================
# BUILD DOCUMENT CONTEXT
# =====================================

def build_document_context(
    active_document_ids: list,
):

    contexts = []

    documents = []

    for document_id in active_document_ids:

        document = ACTIVE_DOCUMENTS.get(
            document_id
        )

        if not document:
            continue

        documents.append({

            "document_id":
            document_id,

            "filename":
            document["filename"],

        })

        contexts.append(

            f"""
FILE:
{document["filename"]}

CONTENT:
{document["content"][:10000]}
"""

        )

    return {

        "documents":
        documents,

        "context":
        "\n\n".join(
            contexts
        ),

    }


# =====================================
# BUILD PROMPT
# =====================================

def build_document_prompt(

    query: str,

    document_context: str,

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

    active_document_ids: list,

):

    document_result = (

        build_document_context(

            active_document_ids,

        )

    )

    document_context = (

        document_result["context"]

    )

    documents = (

        document_result["documents"]

    )

    if not document_context:

        return None

    prompt = build_document_prompt(

        query=query,

        document_context=document_context,

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

        "sources":
        [],

        "evidence":
        {},

        "evidence_matrix":
        {},

        "documents":
        documents,

    }