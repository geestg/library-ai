from app.services.document.document_vector_retriever import (
    retrieve_document_chunks,
)

from app.services.prompts.models.prompt_request import (
    PromptRequest,
)

from app.services.prompts.models.prompt_type import (
    PromptType,
)

from app.services.research.session import (
    session_manager,
)

from app.services.llm.tasks.llm_task import (
    LLMTask,
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

    payload = {

        "phase":
            phase,

        "label":
            label,

        "stage":
            stage,

    }

    print(
        "[DOCUMENT PROGRESS] Emitting",
        payload,
        flush=True,
    )

    try:

        progress_callback(
            payload
        )

    except Exception as exc:

        import traceback

        print(
            "[DOCUMENT PROGRESS ERROR]",
            {
                "phase": phase,
                "error_type": (
                    type(exc).__name__
                ),
                "error": str(exc),
            },
            flush=True,
        )

        traceback.print_exc()

        # Progress reporting must never
        # terminate document analysis.
        return

    print(
        "[DOCUMENT PROGRESS] Emitted",
        {
            "phase": phase,
        },
        flush=True,
    )

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

    print(
        "[DOCUMENT CONTEXT] Starting",
        {
            "query": query,
            "session_id": session_id,
            "active_document_ids": active_document_ids,
            "top_k": top_k,
        },
        flush=True,
    )

    # =================================
    # RESOLVE SESSION-OWNED DOCUMENTS
    # =================================

    print(
        "[DOCUMENT CONTEXT] Resolving active documents",
        flush=True,
    )

    documents = resolve_active_documents(

        session_id=session_id,

        active_document_ids=(
            active_document_ids
        ),

    )

    print(
        "[DOCUMENT CONTEXT] Documents resolved",
        {
            "count": len(documents),
            "document_ids": [
                document["document_id"]
                for document in documents
            ],
        },
        flush=True,
    )

    if not documents:

        print(
            "[DOCUMENT CONTEXT] No active documents",
            flush=True,
        )

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

    print(
        "[DOCUMENT RETRIEVAL] Starting",
        {
            "query": query,
            "document_ids": verified_document_ids,
            "top_k": top_k,
        },
        flush=True,
    )

    chunks = retrieve_document_chunks(

        query=query,

        session_id=session_id,

        active_document_ids=(
            verified_document_ids
        ),

        top_k=top_k,

    )

    print(
        "[DOCUMENT RETRIEVAL] Completed",
        {
            "chunk_count": len(chunks)
            if chunks
            else 0,
        },
        flush=True,
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

    print(
        "[DOCUMENT CONTEXT] Building context",
        flush=True,
    )

    document_context = (

        build_context_from_chunks(

            chunks=chunks,

            documents=documents,

        )

    )

    print(
        "[DOCUMENT CONTEXT] Ready",
        {
            "chunk_count": len(chunks),
            "context_length": len(document_context),
        },
        flush=True,
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
di bawah ini benar-benar mengandung informasi
substantif yang dapat digunakan untuk menjawab
pertanyaan user.

==================================================
EVIDENCE
==================================================

{chunk_context}

==================================================
PERTANYAAN USER
==================================================

{query}

==================================================
PRINSIP UTAMA
==================================================

ANSWERABLE berarti evidence benar-benar memberikan
informasi yang diminta.

Kemunculan topik, istilah, kata kunci, nama bagian,
atau pernyataan bahwa informasi akan dijelaskan
TIDAK berarti evidence mengandung jawabannya.

Bedakan dengan ketat antara:

1. evidence yang MEMBERIKAN jawaban,

dan

2. evidence yang hanya MENYEBUT topik pertanyaan.

Hanya kondisi pertama yang boleh menghasilkan
ANSWERABLE.

==================================================
ATURAN VERIFIKASI
==================================================

1. Pilih ANSWERABLE hanya jika evidence mengandung
fakta, nilai, nama, syarat, langkah, hasil,
penjelasan, atau hubungan struktural yang secara
substantif dapat digunakan untuk menjawab
pertanyaan user.

2. Evidence tidak harus menjawab seluruh pertanyaan
jika evidence memberikan bagian jawaban yang
substantif dan benar-benar relevan.

3. Jawaban tidak harus menggunakan susunan kata
yang sama persis dengan pertanyaan.

4. Perbedaan format karakter, simbol, tanda baca,
atau encoding tidak membatalkan evidence jika
makna informasinya tetap jelas.

5. Jika user meminta angka atau nilai, pilih
ANSWERABLE hanya jika angka atau nilai tersebut
terdapat bersama konteks yang menunjukkan bahwa
angka tersebut memang menjawab hal yang ditanyakan.

6. Jika user meminta tujuan, hasil, metode, dataset,
kesimpulan, alasan, atau informasi substantif lain,
evidence harus benar-benar memberikan isi informasi
tersebut.

7. Kesamaan topik saja tidak cukup.

8. Kemunculan kata yang sama dengan pertanyaan
tidak cukup.

9. Nama bab, nama subbab, judul bagian, atau daftar
isi saja tidak cukup kecuali struktur tersebut
sendiri merupakan informasi yang diminta user.

10. Pernyataan bahwa suatu informasi akan dibahas,
dijelaskan, dipaparkan, diuraikan, disajikan,
ditampilkan, atau dijelaskan pada bagian lain
bukan jawaban terhadap informasi tersebut.

11. Jangan menggunakan informasi dari chunk lain.

12. Jangan melengkapi kalimat yang terpotong dengan
asumsi tentang isi sebelum atau sesudah evidence.

13. Jangan menggunakan pengetahuan eksternal.

14. Jangan membuat asumsi.

15. Pilih NOT_FOUND jika evidence hanya relevan
secara topik tetapi tidak memberikan informasi
substantif yang diminta.

16. Pilih NOT_FOUND jika evidence hanya menunjukkan
bahwa jawaban mungkin terdapat di bagian lain
dokumen.

==================================================
UJI WAJIB SEBELUM MEMILIH ANSWERABLE
==================================================

Tanyakan:

"Jika hanya evidence ini yang tersedia, apakah saya
dapat mengambil setidaknya satu klaim substantif
yang secara langsung membantu menjawab pertanyaan?"

Jika YA:
ANSWERABLE

Jika TIDAK:
NOT_FOUND

Jangan memilih ANSWERABLE hanya karena evidence
terlihat berkaitan dengan pertanyaan.

==================================================
CONTOH KEPUTUSAN
==================================================

Pertanyaan:
"Berapa kuota internet minimum?"

Evidence:
"Koneksi internet dengan kuota minimal 5-7 GB"

Output:
ANSWERABLE

--------------------------------------------------

Pertanyaan:
"Berapa kapasitas baterai minimum?"

Evidence:
"Koneksi internet dengan kuota minimal 5-7 GB"

Output:
NOT_FOUND

--------------------------------------------------

Pertanyaan:
"Apa tujuan penelitian ini?"

Evidence:
"Tujuan dari tugas akhir akan dipaparkan pada
bagian berikutnya."

Output:
NOT_FOUND

Alasan internal:
Evidence hanya menyebut bahwa tujuan akan
dipaparkan, tetapi tidak memberikan isi tujuan.

--------------------------------------------------

Pertanyaan:
"Apa tujuan penelitian ini?"

Evidence:
"Penelitian ini bertujuan mengembangkan sistem
untuk mendeteksi jumlah ikan dan mengestimasi
panjang ikan secara otomatis."

Output:
ANSWERABLE

--------------------------------------------------

Pertanyaan:
"Apa hasil pengujian sistem?"

Evidence:
"Hasil pengujian sistem akan dibahas pada Bab IV."

Output:
NOT_FOUND

--------------------------------------------------

Pertanyaan:
"Apa metode yang digunakan?"

Evidence:
"Bab ini menjelaskan metode yang digunakan dalam
penelitian."

Output:
NOT_FOUND

--------------------------------------------------

Pertanyaan:
"Apa dataset yang digunakan?"

Evidence:
"Dari proses akuisisi diperoleh sebanyak 1.600
citra yang digunakan sebagai dataset awal
penelitian."

Output:
ANSWERABLE

--------------------------------------------------

Pertanyaan:
"Apa dataset yang digunakan?"

Evidence:
"Dataset selanjutnya melalui tahap pelabelan dan
augmentasi sebelum digunakan untuk pelatihan."

Output:
NOT_FOUND

Alasan internal:
Evidence menjelaskan pemrosesan dataset tetapi
tidak mengidentifikasi dataset yang digunakan.

--------------------------------------------------

Pertanyaan:
"Bagaimana dataset diproses?"

Evidence:
"Dataset melalui tahap pelabelan, preprocessing,
dan augmentasi sebelum digunakan untuk pelatihan."

Output:
ANSWERABLE

==================================================
OUTPUT
==================================================

Jawab tepat dengan salah satu nilai berikut:

ANSWERABLE

atau

NOT_FOUND

Jangan menambahkan teks lain.
""".strip()

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

    print(
        "[ANSWERABILITY CHUNK] Calling model",
        {
            "query": query,
            "context_length": len(chunk_context),
            "prompt_length": len(prompt),
            "model": model,
            "provider": provider,
        },
        flush=True,
    )

    try:

        request = PromptRequest(
            prompt=prompt,
            prompt_type=PromptType.VERIFIER,
            model=model,

            provider=provider,

        )

        verification_result = LLMTask.verifier(
            request
        )
        

    except Exception as exc:

        import traceback

        print(
            "[ANSWERABILITY CHUNK ERROR]",
            {
                "error_type": (
                    type(exc).__name__
                ),
                "error": str(exc),
            },
            flush=True,
        )

        traceback.print_exc()

        raise

    print(
        "[ANSWERABILITY RAW]",
        repr(verification_result),
        flush=True,
    )

    normalized = normalize_answerability(
        verification_result
    )

    print(
        "[ANSWERABILITY NORMALIZED]",
        normalized,
        flush=True,
    )

    return normalized

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

    request = PromptRequest(
            prompt=prompt,
            prompt_type=PromptType.VERIFIER,
            model=model,

        provider=provider,

    )

    verification_result = LLMTask.verifier(
        request
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

            print(
                "[ANSWERABLE CHUNK]",
                {
                    "document_id":
                        chunk.get("document_id"),

                    "page":
                        chunk.get("page"),

                    "chunk_index":
                        chunk.get("chunk_index"),

                    "score":
                        chunk.get("score"),

                    "text":
                        chunk.get("text"),
                },
                flush=True,
            )

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

Jawab pertanyaan user hanya berdasarkan informasi
yang tersedia dalam dokumen aktif.

==================================================
DOCUMENT CONTEXT
==================================================

{document_context}

==================================================
PERTANYAAN USER
==================================================

{query}

==================================================
PRINSIP UTAMA
==================================================

Konteks dokumen di atas adalah satu-satunya
sumber kebenaran untuk jawaban.

Jangan menggunakan:

- pengetahuan eksternal,
- asumsi,
- tebakan,
- generalisasi yang tidak didukung,
- atau informasi yang tidak terdapat dalam
  konteks dokumen.

Setiap klaim dalam jawaban harus didukung oleh:

1. fakta yang tertulis langsung dalam konteks
dokumen,

atau

2. hubungan struktural yang terlihat langsung,
seperti judul bagian, subjudul, daftar, tabel,
atau pengelompokan informasi.

==================================================
KELENGKAPAN JAWABAN
==================================================

Jawaban harus mencakup seluruh informasi relevan
yang secara langsung menjawab pertanyaan user.

1. Identifikasi semua fakta dalam konteks dokumen
yang menjawab pertanyaan.

2. Jangan berhenti pada fakta pertama jika terdapat
fakta relevan lain yang juga merupakan bagian dari
jawaban.

3. Jika pertanyaan meminta daftar, persyaratan,
pilihan, jenis, platform, sistem, metode, langkah,
nilai, atau beberapa item terkait, sertakan semua
item relevan yang tersedia dalam konteks.

4. Jangan menghilangkan alternatif yang setara.

5. Jangan memilih hanya satu item jika konteks
menunjukkan beberapa item sebagai jawaban yang
sama-sama relevan.

6. Kelengkapan tidak berarti menambahkan informasi
baru. Sertakan semua yang relevan, tetapi hanya
yang didukung oleh konteks dokumen.

Contoh prinsip:

Jika konteks menyebut dua sistem operasi minimum,
jawaban harus menyebut keduanya.

Jika konteks menyebut satu nilai kuota minimum,
jawaban cukup menyebut nilai tersebut.

==================================================
FOKUS INTI PERTANYAAN
==================================================

Sebelum menjawab, tentukan bagian utama yang
sebenarnya sedang ditanyakan user.

Jawaban harus merespons bagian utama tersebut,
bukan hanya mengulang fakta atau objek yang
disebut dalam pertanyaan.

Contoh:

Pertanyaan:
"Apakah persyaratan A dan B berlaku untuk semua
peserta?"

Bagian utama yang ditanyakan adalah cakupan:

"berlaku untuk semua peserta"

Jawaban tidak cukup hanya menjelaskan kembali
apa itu persyaratan A dan B.

Jawaban harus menjelaskan apakah cakupan
"semua peserta" didukung oleh dokumen.

Jika dokumen hanya menunjukkan bahwa A dan B
tercantum sebagai persyaratan untuk peserta,
tetapi tidak secara eksplisit mendukung kata
"semua", jawab dengan pola makna berikut:

"A dan B tercantum sebagai persyaratan untuk
peserta, tetapi dokumen tidak secara eksplisit
menyatakan bahwa keduanya berlaku untuk semua
peserta."

Aturan ini berlaku juga untuk pertanyaan tentang:

- apakah,
- mengapa,
- bagaimana,
- kapan,
- siapa,
- mana,
- berapa,
- perbedaan,
- hubungan,
- sebab,
- cakupan,
- pengecualian.

Jangan mengganti jawaban atas bagian utama
pertanyaan dengan pengulangan detail pendukung.


==================================================
BATAS DUKUNGAN INFORMASI
==================================================

Bedakan tiga kondisi berikut.

1. FAKTA LANGSUNG

Informasi tertulis langsung dalam konteks dokumen.

Fakta tersebut boleh dinyatakan secara langsung.

2. HUBUNGAN STRUKTURAL LANGSUNG

Informasi didukung oleh struktur dokumen.

Contohnya, beberapa item yang berada langsung
di bawah judul:

"Minimum System Requirements untuk Peserta"

boleh dijelaskan sebagai persyaratan minimum
untuk peserta.

3. KLAIM TIDAK DIDUKUNG

Informasi membutuhkan:

- asumsi tambahan,
- generalisasi,
- kepastian yang tidak tertulis,
- pengecualian yang tidak dibahas,
- atau pengetahuan di luar dokumen.

Klaim seperti ini tidak boleh dibuat.

==================================================
CAKUPAN DAN KLAIM UNIVERSAL
==================================================

Berikan perhatian khusus pada kata atau makna
seperti:

- semua,
- seluruh,
- setiap,
- selalu,
- tidak pernah,
- tanpa pengecualian,
- pasti,
- hanya,
- wajib bagi setiap,
- berlaku universal.

Jangan mengafirmasi klaim universal kecuali
cakupan universal tersebut didukung secara
eksplisit oleh konteks dokumen.

Jika pertanyaan user menggunakan klaim universal,
tetapi dokumen hanya mendukung cakupan yang lebih
terbatas:

1. nyatakan cakupan yang benar-benar didukung,

2. jangan memperluas cakupan tersebut,

3. jelaskan secara singkat batas informasi jika
diperlukan untuk menjawab pertanyaan.

Contoh prinsip:

Jika dokumen hanya menempatkan beberapa item
di bawah bagian persyaratan minimum untuk peserta,
boleh nyatakan bahwa item tersebut tercantum
sebagai persyaratan minimum untuk peserta.

Jangan menyatakan bahwa item tersebut berlaku
untuk semua peserta tanpa pengecualian kecuali
dokumen menyatakan cakupan universal tersebut
secara eksplisit.

==================================================
KETIDAKPASTIAN DAN PENGECUALIAN
==================================================

1. Jangan menyatakan bahwa tidak ada pengecualian
jika dokumen tidak membahas pengecualian.

2. Jangan menyatakan bahwa suatu aturan berlaku
untuk semua pihak hanya karena dokumen tidak
menyebut pengecualian.

3. Ketiadaan informasi bukan bukti bahwa sesuatu
tidak ada.

4. Jika dokumen mendukung hanya sebagian dari
pertanyaan, jawab bagian yang didukung.

5. Jika batas informasi penting untuk mencegah
kesimpulan yang salah, jelaskan batas tersebut
secara singkat.

6. Jangan memaksakan jawaban "ya" atau "tidak"
jika dokumen tidak mendukung kepastian tersebut.

==================================================
ATURAN JAWABAN
==================================================

1. Jawab pertanyaan secara langsung.

2. Gunakan seluruh fakta relevan yang diperlukan
untuk menghasilkan jawaban lengkap.

3. Jangan menghilangkan fakta relevan hanya untuk
membuat jawaban lebih singkat.

4. Jangan menambahkan fakta yang tidak diperlukan
untuk menjawab pertanyaan.

5. Jangan mengulang pertanyaan user.

6. Jangan mengawali jawaban dengan label seperti:

"Pertanyaan user:"

"Jawaban:"

"Jawaban berdasarkan evidence:"

"Berdasarkan evidence:"

"Analisis:"

7. Jangan mengutip ulang isi dokumen secara panjang
jika jawaban dapat disampaikan dengan parafrasa
yang akurat.

8. Pertahankan istilah, angka, versi, nama,
simbol, dan nilai penting sebagaimana terdapat
dalam dokumen.

9. Jika nama file membantu identifikasi sumber,
nama file boleh disebutkan secara natural.

10. Jika nomor halaman tersedia dan membantu
verifikasi jawaban, halaman boleh disebutkan
secara natural.

11. Jangan menyebut nama file atau halaman secara
mekanis jika tidak menambah kejelasan jawaban.

12. Jika terdapat informasi berbeda antar dokumen,
jelaskan perbedaannya hanya berdasarkan konteks.

13. Jika user meminta perbandingan dan data
mendukungnya, gunakan tabel Markdown.

14. Jika user meminta ringkasan, buat ringkasan
terstruktur hanya dari informasi yang tersedia.

==================================================
LARANGAN OUTPUT INTERNAL
==================================================

Jangan menjelaskan proses internal sistem.

Jangan menyebut:

- evidence,
- verified evidence,
- answerability,
- retrieval,
- retrieved chunk,
- chunk,
- context window,
- prompt,
- pipeline,
- model,
- verifier,
- similarity score.

Jangan menggunakan kalimat meta seperti:

"Informasi ini didasarkan langsung pada evidence
yang diberikan."

"Jawaban berdasarkan konteks yang tersedia."

"Menurut evidence yang diberikan."

Sampaikan hasilnya langsung sebagai jawaban untuk
user.

==================================================
FORMAT
==================================================

1. Gunakan Bahasa Indonesia.

2. Gunakan Markdown murni.

3. Jangan gunakan tag HTML.

4. Jangan membuat heading jika jawaban cukup
disampaikan dalam satu atau dua kalimat.

5. Jangan membuat tabel kecuali struktur pertanyaan
memang membutuhkannya.

6. Gunakan jawaban sesingkat mungkin tanpa
menghilangkan fakta relevan.

7. Prioritaskan urutan berikut:

- benar,
- lengkap,
- terdukung dokumen,
- langsung,
- ringkas.

8. Sebelum menghasilkan jawaban akhir, pastikan:

- tidak ada fakta relevan yang terlewat,
- tidak ada klaim yang melampaui dokumen,
- tidak ada label atau penjelasan proses internal,
- tidak ada pengulangan pertanyaan user.
""".strip()

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

    print(
        "[DOCUMENT ANALYSIS] Starting",
        {
            "query": query,
            "session_id": session_id,
            "active_document_ids": active_document_ids,
            "stream": stream,
        },
        flush=True,
    )

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

    try:

        document_result = (

            build_document_context(

                query=query,

                session_id=session_id,

                active_document_ids=(
                    active_document_ids
                ),

            )

        )

        print(
            "[DOCUMENT ANALYSIS] Context returned",
            flush=True,
        )

    except Exception as exc:

        import traceback

        print(
            "\n"
            "====================================\n"
            "DOCUMENT ENGINE ERROR\n"
            "====================================",
            flush=True,
        )

        print(
            f"[ERROR TYPE] {type(exc).__name__}",
            flush=True,
        )

        print(
            f"[ERROR MESSAGE] {exc}",
            flush=True,
        )

        traceback.print_exc()

        raise

    # =====================================
    # EXTRACT DOCUMENT RESULT
    # =====================================

    documents = (
        document_result["documents"]
    )

    chunks = (
        document_result["chunks"]
    )

    print(
        "[DOCUMENT ANALYSIS] Result extracted",
        {
            "document_count": len(documents),
            "chunk_count": len(chunks),
        },
        flush=True,
    )

    # =====================================
    # VALIDATE DOCUMENT CONTEXT
    # =====================================

    if not chunks:

        print(
            "[DOCUMENT ANALYSIS] No chunks found",
            flush=True,
        )

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

    print(
        "[ANSWERABILITY] Starting verification",
        {
            "query": query,
            "chunk_count": len(chunks),
            "document_count": len(documents),
            "model": model,
            "provider": provider,
        },
        flush=True,
    )

    try:

        verification = verify_answerability(

            query=query,

            chunks=chunks,

            documents=documents,

            model=model,

            provider=provider,

        )

    except Exception as exc:

        import traceback

        print(
            "\n"
            "====================================\n"
            "ANSWERABILITY VERIFICATION ERROR\n"
            "====================================",
            flush=True,
        )

        print(
            f"[ERROR TYPE] {type(exc).__name__}",
            flush=True,
        )

        print(
            f"[ERROR MESSAGE] {exc}",
            flush=True,
        )

        traceback.print_exc()

        raise

    print(
        "[ANSWERABILITY] Verification completed",
        verification,
        flush=True,
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

        request = PromptRequest(
            prompt=prompt,
            prompt_type=PromptType.VERIFIER,
            model=model,

            provider=provider,

        )

        llm_stream = LLMTask.stream_answer(
            request
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

    request = PromptRequest(
            prompt=prompt,
            prompt_type=PromptType.VERIFIER,
            model=model,

        provider=provider,

    )

    answer = LLMTask.answer(
        request
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


