from app.services.document.document_vector_retriever import (
    retrieve_document_chunks,
)

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

        "chunks":
            [],

        "context":
            "",

    }


# =====================================
# RESOLVE ACTIVE DOCUMENTS
# =====================================

def resolve_active_documents(

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

        return []

    # =================================
    # VERIFY DOCUMENT OWNERSHIP
    # =================================

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

            "file_type":
                document.file_type,

            "pages":
                document.pages,

            "chunks":
                document.chunks,

        })

    return documents


# =====================================
# BUILD DOCUMENT CONTEXT
# =====================================

def build_document_context(

    query: str,

    session_id: str,

    active_document_ids: list,

    top_k: int = 12,

):

    # =================================
    # RESOLVE SESSION-OWNED DOCUMENTS
    # =================================

    documents = resolve_active_documents(

        session_id=session_id,

        active_document_ids=(
            active_document_ids
        ),

    )

    if not documents:

        return (
            build_empty_document_context()
        )

    # =================================
    # VERIFIED DOCUMENT IDS
    # =================================

    verified_document_ids = [

        document["document_id"]

        for document in documents

    ]

    # =================================
    # RETRIEVE RELEVANT CHUNKS
    # =================================

    chunks = retrieve_document_chunks(

        query=query,

        session_id=session_id,

        active_document_ids=(
            verified_document_ids
        ),

        top_k=top_k,

    )

    if not chunks:

        return {

            "documents":
                documents,

            "chunks":
                [],

            "context":
                "",

        }

    # =================================
    # DOCUMENT NAME MAP
    # =================================

    document_name_map = {

        document["document_id"]:
            document["filename"]

        for document in documents

    }

    # =================================
    # BUILD GROUNDED CONTEXT
    # =================================

    contexts = []

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):

        document_id = chunk.get(
            "document_id"
        )

        filename = document_name_map.get(

            document_id,

            chunk.get(
                "title"
            )

            or "Unknown Document",

        )

        page = chunk.get(
            "page"
        )

        chunk_index = chunk.get(
            "chunk_index"
        )

        score = chunk.get(
            "score",
            0,
        )

        text = chunk.get(
            "text",
            "",
        )

        contexts.append(

            f"""
[EVIDENCE {index}]

FILE:
{filename}

DOCUMENT_ID:
{document_id}

PAGE:
{page}

CHUNK_INDEX:
{chunk_index}

SIMILARITY_SCORE:
{score:.6f}

CONTENT:
{text}
""".strip()

        )

    return {

        "documents":
            documents,

        "chunks":
            chunks,

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

Anda sedang menjawab pertanyaan berdasarkan
evidence yang diambil dari dokumen aktif user.

==================================================
RETRIEVED DOCUMENT EVIDENCE
==================================================

{document_context}

==================================================
PERTANYAAN USER
==================================================

{query}

==================================================
ATURAN
==================================================

1. Jawab hanya berdasarkan evidence dokumen
yang diberikan.

2. Jangan menggunakan pengetahuan eksternal
untuk mengisi informasi yang tidak ditemukan.

3. Jika informasi berasal dari dokumen tertentu,
sebutkan nama file tersebut.

4. Jika nomor halaman tersedia,
sebutkan halaman yang relevan.

5. Jika terdapat informasi yang berbeda
antar dokumen, jelaskan perbedaannya.

6. Jika user meminta perbandingan,
buat tabel perbandingan.

7. Jika user meminta ringkasan,
buat ringkasan terstruktur.

8. Jika evidence tidak cukup untuk menjawab,
katakan bahwa informasi tidak ditemukan
dalam bagian dokumen yang relevan.

9. Jangan mengarang.

10. Gunakan Bahasa Indonesia.

11. Gunakan Markdown murni.

12. Jangan gunakan tag HTML.

13. Untuk tabel, gunakan sintaks tabel Markdown.

14. Untuk daftar, gunakan tanda "- "
atau penomoran Markdown.

15. Pastikan jawaban dapat ditelusuri kembali
ke evidence yang diberikan.
"""


# =====================================
# DOCUMENT ANALYSIS
# =====================================

def run_document_analysis(

    query: str,

    session_id: str,

    active_document_ids: list,

    model: str | None = None,

    provider: str | None = None,

    stream: bool = False,

    progress_callback=None,

):

    # =====================================
    # RETRIEVE DOCUMENT EVIDENCE
    # =====================================

    emit_progress(

        progress_callback,

        phase=(
            "retrieving_document_evidence"
        ),

        label=(
            "Mencari bagian dokumen yang relevan"
        ),

    )

    document_result = (

        build_document_context(

            query=query,

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

    chunks = (
        document_result["chunks"]
    )

    # =====================================
    # VALIDATE DOCUMENT CONTEXT
    # =====================================

    if not document_context:

        return None

    # =====================================
    # PREPARE ANALYSIS
    # =====================================

    emit_progress(

        progress_callback,

        phase=(
            "preparing_document_analysis"
        ),

        label=(
            "Menyiapkan evidence dokumen"
        ),

    )

    prompt = build_document_prompt(

        query=query,

        document_context=document_context,

    )

    # =====================================
    # ANALYSIS READY
    # =====================================

    emit_progress(

        progress_callback,

        phase=(
            "analyzing_documents"
        ),

        label=(
            "Menganalisis evidence dokumen"
        ),

    )

    # =====================================
    # STREAM MODE
    # =====================================

    if stream:

        llm_stream = (

            gateway.stream_response(

                prompt=prompt,

                model=model,

                provider=provider,

            )

        )

        return {

            "query":
                query,

            "mode":
                "document_retrieval",

            "prompt":
                prompt,

            "llm_stream":
                llm_stream,

            "documents":
                documents,

            "retrieved_chunks":
                chunks,

        }

    # =====================================
    # NORMAL MODE
    # =====================================

    answer = (

        gateway.generate_response(

            prompt=prompt,

            model=model,

            provider=provider,

        )

    )

    # =====================================
    # FINALIZE RESPONSE
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
            "document_retrieval",

        "analysis":
            answer,

        "citations":
            chunks,

        "sources":
            chunks,

        "evidence": {

            "retrieved_chunks":
                chunks,

        },

        "evidence_matrix":
            {},

        "documents":
            documents,

        "retrieved_chunks":
            chunks,

    }