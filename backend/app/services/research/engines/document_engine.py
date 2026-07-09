from app.services.llm.model_gateway import (
    gateway,
)

from app.services.research.session import (
    session_manager,
)


# =====================================
# EMIT PROGRESS
# =====================================

def emit_progress(

    progress_callback,

    phase: str,

    label: str,

    stage: str = "document",

):

    if progress_callback is None:

        return

    progress_callback({

        "phase":
            phase,

        "label":
            label,

        "stage":
            stage,

    })


# =====================================
# BUILD EMPTY DOCUMENT CONTEXT
# =====================================

def build_empty_document_context():

    return {

        "documents":
            [],

        "context":
            "",

    }


# =====================================
# BUILD DOCUMENT CONTEXT
# =====================================

def build_document_context(

    session_id: str,

    active_document_ids: list,

):

    # =================================
    # RESOLVE SESSION
    # =================================

    session = session_manager.get(
        session_id
    )

    if session is None:

        return (
            build_empty_document_context()
        )

    # =================================
    # BUILD CONTEXT
    # =================================

    contexts = []

    documents = []

    for document_id in active_document_ids:

        document = (

            session.documents.get_document(
                document_id
            )

        )

        if document is None:

            continue

        documents.append({

            "document_id":
                document.document_id,

            "filename":
                document.filename,

        })

        contexts.append(

            f"""
FILE:
{document.filename}

CONTENT:
{document.content[:10000]}
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

11. Gunakan Markdown murni untuk format jawaban.

12. Jangan gunakan tag HTML seperti
<br>, <ul>, <li>, <table>, atau tag HTML lainnya.

13. Untuk tabel, gunakan sintaks tabel Markdown.

14. Untuk daftar, gunakan tanda "- " atau penomoran Markdown.

15. Pastikan setiap isi tabel ringkas dan mudah dibaca.
"""


# =====================================
# DOCUMENT ANALYSIS
# =====================================

def run_document_analysis(

    query: str,

    session_id: str,

    active_document_ids: list,

    progress_callback=None,

):

    # =====================================
    # PREPARE DOCUMENT CONTEXT
    # =====================================

    emit_progress(

        progress_callback,

        phase=(
            "preparing_document_context"
        ),

        label=(
            "Menyiapkan konteks dokumen"
        ),

    )

    document_result = (

        build_document_context(

            session_id=session_id,

            active_document_ids=(
                active_document_ids
            ),

        )

    )

    document_context = (

        document_result["context"]

    )

    documents = (

        document_result["documents"]

    )

    # =====================================
    # VALIDATE DOCUMENT CONTEXT
    # =====================================

    if not document_context:

        return None

    # =====================================
    # BUILD ANALYSIS INSTRUCTIONS
    # =====================================

    emit_progress(

        progress_callback,

        phase=(
            "preparing_document_analysis"
        ),

        label=(
            "Menyiapkan analisis dokumen"
        ),

    )

    prompt = build_document_prompt(

        query=query,

        document_context=document_context,

    )

    # =====================================
    # GENERATE DOCUMENT ANALYSIS
    # =====================================

    emit_progress(

        progress_callback,

        phase=(
            "analyzing_documents"
        ),

        label=(
            "Menganalisis isi dokumen"
        ),

    )

    answer = (

        gateway.generate_response(

            prompt=prompt

        )

    )

    # =====================================
    # FINALIZE DOCUMENT RESPONSE
    # =====================================

    emit_progress(

        progress_callback,

        phase=(
            "finalizing_document_response"
        ),

        label=(
            "Menyelesaikan jawaban"
        ),

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