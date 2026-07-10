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
# ANSWERABILITY STATUS
# =====================================

ANSWERABLE = "ANSWERABLE"

NOT_FOUND = "NOT_FOUND"


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
# BUILD CHUNK CONTEXT
# =====================================

def build_chunk_context(

    chunk: dict,

    document_name_map: dict,

    evidence_index: int = 1,

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

    return f"""
[EVIDENCE {evidence_index}]

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


# =====================================
# BUILD CONTEXT FROM CHUNKS
# =====================================

def build_context_from_chunks(

    chunks: list,

    documents: list,

):

    if not chunks:

        return ""

    document_name_map = {

        document["document_id"]:
            document["filename"]

        for document in documents

    }

    contexts = []

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):

        contexts.append(

            build_chunk_context(

                chunk=chunk,

                document_name_map=(
                    document_name_map
                ),

                evidence_index=index,

            )

        )

    return "\n\n".join(
        contexts
    )


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
    # BUILD GROUNDED CONTEXT
    # =================================

    document_context = (

        build_context_from_chunks(

            chunks=chunks,

            documents=documents,

        )

    )

    return {

        "documents":
            documents,

        "chunks":
            chunks,

        "context":
            document_context,

    }


# =====================================
# BUILD SINGLE CHUNK VERIFIER PROMPT
# =====================================

def build_chunk_answerability_prompt(

    query: str,

    chunk_context: str,

):

    return f"""
Anda adalah verifier evidence dokumen.

Tugas Anda hanya menentukan apakah SATU evidence
di bawah ini mengandung informasi yang dapat
digunakan untuk menjawab pertanyaan user.

==================================================
EVIDENCE
==================================================

{chunk_context}

==================================================
PERTANYAAN USER
==================================================

{query}

==================================================
ATURAN VERIFIKASI
==================================================

1. Pilih ANSWERABLE jika evidence secara eksplisit
mengandung jawaban, nilai, fakta, syarat, nama,
langkah, atau informasi yang diminta user.

2. Jawaban tidak harus menggunakan susunan kata
yang sama persis dengan pertanyaan.

3. Perbedaan format karakter, simbol, tanda baca,
atau encoding tidak membatalkan evidence jika
makna informasinya tetap jelas.

4. Jika user meminta angka atau nilai dan angka
tersebut terdapat dalam evidence bersama konteks
yang sesuai, pilih ANSWERABLE.

5. Kesamaan topik saja tidak cukup.

6. Jangan menggunakan pengetahuan eksternal.

7. Jangan membuat asumsi.

8. Pilih NOT_FOUND hanya jika evidence benar-benar
tidak mengandung informasi yang dapat menjawab
pertanyaan user.

==================================================
CONTOH KEPUTUSAN
==================================================

Pertanyaan:
"Berapa kuota internet minimum?"

Evidence:
"Koneksi internet dengan kuota minimal 5-7 GB"

Output:
ANSWERABLE

Pertanyaan:
"Berapa kapasitas baterai minimum?"

Evidence:
"Koneksi internet dengan kuota minimal 5-7 GB"

Output:
NOT_FOUND

==================================================
OUTPUT
==================================================

Jawab tepat dengan salah satu nilai berikut:

ANSWERABLE

atau

NOT_FOUND

Jangan menambahkan teks lain.
"""


# =====================================
# BUILD COLLECTIVE VERIFIER PROMPT
# =====================================

def build_collective_answerability_prompt(

    query: str,

    document_context: str,

):

    return f"""
Anda adalah verifier evidence dokumen.

Tugas Anda menentukan apakah kumpulan evidence
di bawah ini secara bersama-sama mengandung
informasi yang cukup untuk menjawab pertanyaan
user.

Gunakan verifikasi kolektif ini terutama untuk
pertanyaan yang membutuhkan beberapa bagian
dokumen, seperti ringkasan, perbandingan,
daftar, hubungan antar informasi, atau sintesis.

==================================================
EVIDENCE
==================================================

{document_context}

==================================================
PERTANYAAN USER
==================================================

{query}

==================================================
ATURAN VERIFIKASI
==================================================

1. Pilih ANSWERABLE jika jawaban dapat dibangun
secara langsung dari satu atau beberapa evidence.

2. Semua fakta yang dibutuhkan untuk menjawab
harus terdapat dalam evidence.

3. Jangan menggunakan pengetahuan eksternal.

4. Jangan membuat asumsi.

5. Jangan menolak hanya karena jawaban tersebar
di beberapa evidence.

6. Perbedaan format karakter, simbol, tanda baca,
atau encoding tidak membatalkan evidence jika
makna informasinya tetap jelas.

7. Pilih NOT_FOUND hanya jika evidence secara
kolektif tetap tidak cukup untuk menjawab
pertanyaan user.

==================================================
OUTPUT
==================================================

Jawab tepat dengan salah satu nilai berikut:

ANSWERABLE

atau

NOT_FOUND

Jangan menambahkan teks lain.
"""


# =====================================
# NORMALIZE ANSWERABILITY
# =====================================

def normalize_answerability(

    verification_result,

) -> str:

    if verification_result is None:

        return NOT_FOUND

    normalized = str(
        verification_result
    ).strip().upper()

    # =================================
    # EXACT ANSWERABLE
    # =================================

    if normalized == ANSWERABLE:

        return ANSWERABLE

    # =================================
    # EXACT NOT FOUND
    # =================================

    if normalized == NOT_FOUND:

        return NOT_FOUND

    # =================================
    # HANDLE WRAPPED MODEL OUTPUT
    # =================================

    lines = [

        line.strip()

        for line in normalized.splitlines()

        if line.strip()

    ]

    for line in lines:

        if line == ANSWERABLE:

            return ANSWERABLE

        if line == NOT_FOUND:

            return NOT_FOUND

    # =================================
    # CONSERVATIVE FALLBACK
    # =================================

    return NOT_FOUND


# =====================================
# VERIFY SINGLE CHUNK
# =====================================

def verify_single_chunk(

    query: str,

    chunk_context: str,

    model: str | None = None,

    provider: str | None = None,

) -> str:

    prompt = (

        build_chunk_answerability_prompt(

            query=query,

            chunk_context=chunk_context,

        )

    )

    verification_result = (

        gateway.generate_response(

            prompt=prompt,

            model=model,

            provider=provider,

        )

    )

    return normalize_answerability(
        verification_result
    )


# =====================================
# VERIFY COLLECTIVE CONTEXT
# =====================================

def verify_collective_context(

    query: str,

    document_context: str,

    model: str | None = None,

    provider: str | None = None,

) -> str:

    prompt = (

        build_collective_answerability_prompt(

            query=query,

            document_context=(
                document_context
            ),

        )

    )

    verification_result = (

        gateway.generate_response(

            prompt=prompt,

            model=model,

            provider=provider,

        )

    )

    return normalize_answerability(
        verification_result
    )


# =====================================
# VERIFY ANSWERABILITY
# =====================================

def verify_answerability(

    query: str,

    chunks: list,

    documents: list,

    model: str | None = None,

    provider: str | None = None,

):

    if not chunks:

        return {

            "status":
                NOT_FOUND,

            "answerable_chunks":
                [],

            "verification_mode":
                "none",

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
    # VERIFY EACH RETRIEVED CHUNK
    # =================================

    answerable_chunks = []

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):

        chunk_context = (

            build_chunk_context(

                chunk=chunk,

                document_name_map=(
                    document_name_map
                ),

                evidence_index=index,

            )

        )

        chunk_status = (

            verify_single_chunk(

                query=query,

                chunk_context=(
                    chunk_context
                ),

                model=model,

                provider=provider,

            )

        )

        if chunk_status == ANSWERABLE:

            answerable_chunks.append(
                chunk
            )

    # =================================
    # DIRECT EVIDENCE FOUND
    # =================================

    if answerable_chunks:

        return {

            "status":
                ANSWERABLE,

            "answerable_chunks":
                answerable_chunks,

            "verification_mode":
                "per_chunk",

        }

    # =================================
    # COLLECTIVE FALLBACK
    # =================================

    document_context = (

        build_context_from_chunks(

            chunks=chunks,

            documents=documents,

        )

    )

    collective_status = (

        verify_collective_context(

            query=query,

            document_context=(
                document_context
            ),

            model=model,

            provider=provider,

        )

    )

    if collective_status == ANSWERABLE:

        return {

            "status":
                ANSWERABLE,

            "answerable_chunks":
                chunks,

            "verification_mode":
                "collective",

        }

    # =================================
    # NOT FOUND
    # =================================

    return {

        "status":
            NOT_FOUND,

        "answerable_chunks":
            [],

        "verification_mode":
            "none",

    }


# =====================================
# BUILD NOT FOUND RESPONSE
# =====================================

def build_not_found_response(

    query: str,

    documents: list,

    chunks: list,

):

    return {

        "query":
            query,

        "mode":
            "document_retrieval",

        "response_type":
            "static",

        "answerability":
            NOT_FOUND,

        "analysis": (
            "Informasi yang diminta tidak ditemukan "
            "dalam bagian dokumen aktif yang relevan."
        ),

        # Retrieved chunks remain available
        # for execution diagnostics only.
        "retrieved_chunks":
            chunks,

        # Unrelated chunks must not become
        # answer citations.
        "citation_chunks":
            [],

        "citations":
            [],

        "sources":
            [],

        "evidence": {

            "retrieved_chunks":
                chunks,

        },

        "evidence_matrix":
            {},

        "documents":
            documents,

    }


# =====================================
# BUILD DOCUMENT PROMPT
# =====================================

def build_document_prompt(

    query: str,

    document_context: str,

):

    return f"""
Anda adalah DELBot.

Anda menjawab pertanyaan hanya berdasarkan
evidence yang telah diverifikasi dari dokumen
aktif user.

==================================================
VERIFIED DOCUMENT EVIDENCE
==================================================

{document_context}

==================================================
PERTANYAAN USER
==================================================

{query}

==================================================
PRINSIP UTAMA
==================================================

Evidence adalah satu-satunya sumber kebenaran.

Jangan menggunakan pengetahuan eksternal,
asumsi, tebakan, atau informasi yang tidak
tertulis dalam evidence.

==================================================
ATURAN JAWABAN
==================================================

1. Jawab hanya informasi yang secara eksplisit
didukung oleh evidence.

2. Jangan menyimpulkan fakta yang tidak dapat
ditelusuri kembali ke evidence.

3. Jangan menambahkan informasi hanya untuk
membuat jawaban terlihat lebih lengkap.

4. Jangan menggunakan pengetahuan umum atau
pengetahuan model untuk mengisi kekurangan
informasi dalam evidence.

5. Jawab pertanyaan user secara langsung dan fokus.

6. Jika informasi berasal dari dokumen tertentu,
sebutkan nama file yang relevan.

7. Jika nomor halaman tersedia dan relevan,
sebutkan halaman tersebut.

8. Jika terdapat informasi yang berbeda antar
dokumen, jelaskan perbedaannya hanya berdasarkan
evidence.

9. Jika user meminta perbandingan dan evidence
mendukungnya, gunakan tabel Markdown.

10. Jika user meminta ringkasan, buat ringkasan
terstruktur hanya dari evidence yang tersedia.

==================================================
FORMAT
==================================================

1. Gunakan Bahasa Indonesia.

2. Gunakan Markdown murni.

3. Jangan gunakan tag HTML.

4. Jangan menghasilkan teks dalam bahasa lain
kecuali istilah asli yang memang terdapat dalam
evidence.

5. Jangan membuat heading atau tabel jika jawaban
cukup disampaikan dalam satu atau dua kalimat.

6. Pastikan seluruh isi jawaban dapat ditelusuri
kembali ke evidence yang diberikan.
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

    documents = (
        document_result["documents"]
    )

    chunks = (
        document_result["chunks"]
    )

    # =====================================
    # VALIDATE DOCUMENT CONTEXT
    # =====================================

    if not chunks:

        return None

    # =====================================
    # VERIFY ANSWERABILITY
    # =====================================

    emit_progress(

        progress_callback,

        phase=(
            "verifying_document_evidence"
        ),

        label=(
            "Memverifikasi kecukupan evidence"
        ),

    )

    verification = verify_answerability(

        query=query,

        chunks=chunks,

        documents=documents,

        model=model,

        provider=provider,

    )

    answerability = verification.get(

        "status",

        NOT_FOUND,

    )

    citation_chunks = verification.get(

        "answerable_chunks",

        [],

    )

    verification_mode = verification.get(

        "verification_mode",

        "none",

    )

    # =====================================
    # NOT FOUND
    # =====================================

    if answerability == NOT_FOUND:

        emit_progress(

            progress_callback,

            phase=(
                "document_information_not_found"
            ),

            label=(
                "Informasi tidak ditemukan "
                "dalam dokumen"
            ),

        )

        return build_not_found_response(

            query=query,

            documents=documents,

            chunks=chunks,

        )

    # =====================================
    # BUILD VERIFIED ANSWER CONTEXT
    # =====================================

    verified_document_context = (

        build_context_from_chunks(

            chunks=citation_chunks,

            documents=documents,

        )

    )

    # =====================================
    # PREPARE ANSWER
    # =====================================

    emit_progress(

        progress_callback,

        phase=(
            "preparing_document_analysis"
        ),

        label=(
            "Menyiapkan evidence terverifikasi"
        ),

    )

    prompt = build_document_prompt(

        query=query,

        document_context=(
            verified_document_context
        ),

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

            "response_type":
                "stream",

            "answerability":
                ANSWERABLE,

            "verification_mode":
                verification_mode,

            "prompt":
                prompt,

            "llm_stream":
                llm_stream,

            "documents":
                documents,

            "retrieved_chunks":
                chunks,

            "citation_chunks":
                citation_chunks,

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

        "response_type":
            "static",

        "answerability":
            ANSWERABLE,

        "verification_mode":
            verification_mode,

        "analysis":
            answer,

        "citations":
            citation_chunks,

        "sources":
            citation_chunks,

        "evidence": {

            "retrieved_chunks":
                chunks,

            "answerable_chunks":
                citation_chunks,

        },

        "evidence_matrix":
            {},

        "documents":
            documents,

        "retrieved_chunks":
            chunks,

        "citation_chunks":
            citation_chunks,

    }