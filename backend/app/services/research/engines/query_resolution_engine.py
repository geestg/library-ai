from app.services.llm.tasks.llm_task import (
    LLMTask,
)

# =====================================
# CONTEXT REFERENCE PATTERNS
# =====================================

CONTEXT_REFERENCE_PATTERNS = [

    r"\bini\b",

    r"\bitu\b",

    r"\btersebut\b",

    r"\bkeduanya\b",

    r"\bketiganya\b",

    r"\bsemuanya\b",

    r"\byang tadi\b",

    r"\byang sebelumnya\b",

    r"\byang pertama\b",

    r"\byang kedua\b",

    r"\byang ketiga\b",

    r"\bdokumen tadi\b",

    r"\bmetode tadi\b",

    r"\bmetode tersebut\b",

    r"\bsistem tersebut\b",

    r"\bhasil tersebut\b",

    r"\bpenelitian tersebut\b",

    r"\bbagaimana dengan\b",

    r"\bapakah sama\b",

    r"\bapakah berbeda\b",

]


# =====================================
# NORMALIZE TEXT
# =====================================

def normalize_text(
    value,
) -> str:

    if value is None:

        return ""

    return str(
        value
    ).strip()


# =====================================
# DETECT CONTEXT DEPENDENCY
# =====================================

def is_context_dependent_query(
    query: str,
) -> bool:

    normalized_query = (
        normalize_text(
            query
        ).lower()
    )

    if not normalized_query:

        return False

    for pattern in CONTEXT_REFERENCE_PATTERNS:

        if re.search(

            pattern,

            normalized_query,

            flags=re.IGNORECASE,

        ):

            return True

    return False


# =====================================
# BUILD QUERY RESOLUTION PROMPT
# =====================================

def build_query_resolution_prompt(

    query: str,

    conversation_history: str,

) -> str:

    return f"""
Anda adalah query resolver untuk sistem research
dan document retrieval.

Tugas Anda adalah mengubah pertanyaan terbaru user
menjadi pertanyaan mandiri yang dapat dipahami tanpa
harus membaca percakapan sebelumnya.

==================================================
RIWAYAT PERCAKAPAN SEBELUM PERTANYAAN TERBARU
==================================================

{conversation_history}

==================================================
PERTANYAAN TERBARU USER
==================================================

{query}

==================================================
ATURAN
==================================================

1. Gunakan riwayat percakapan hanya untuk
menyelesaikan referensi yang ambigu.

2. Referensi ambigu dapat berupa:
"keduanya", "ketiganya", "ini", "itu",
"tersebut", "yang pertama", "yang kedua",
"yang tadi", "bagaimana dengan yang lain",
atau referensi kontekstual serupa.

3. Pertahankan maksud asli pertanyaan user.

4. Jangan menjawab pertanyaan.

5. Jangan menambahkan fakta baru.

6. Jangan menggunakan pengetahuan eksternal.

7. Jangan membuat asumsi yang tidak didukung
oleh riwayat percakapan.

8. Jika pertanyaan terbaru sudah mandiri,
kembalikan pertanyaan tersebut tanpa perubahan.

9. Output hanya satu pertanyaan hasil resolusi.

10. Jangan menambahkan penjelasan, label,
Markdown, tanda kutip, atau teks lain.

==================================================
OUTPUT
==================================================

Kembalikan hanya pertanyaan mandiri.
""".strip()


# =====================================
# CLEAN RESOLVED QUERY
# =====================================

def clean_resolved_query(
    value,
) -> str:

    resolved_query = normalize_text(
        value
    )

    if not resolved_query:

        return ""

    # =================================
    # REMOVE COMMON WRAPPING QUOTES
    # =================================

    if (

        len(resolved_query) >= 2

        and (

            (
                resolved_query.startswith('"')
                and
                resolved_query.endswith('"')
            )

            or

            (
                resolved_query.startswith("'")
                and
                resolved_query.endswith("'")
            )

        )

    ):

        resolved_query = (
            resolved_query[1:-1].strip()
        )

    return resolved_query


# =====================================
# RESOLVE QUERY
# =====================================

def resolve_query(

    query: str,

    conversation_history: str = "",

    model: str | None = None,

    provider: str | None = None,

) -> dict:

    original_query = normalize_text(
        query
    )

    history = normalize_text(
        conversation_history
    )

    # =================================
    # EMPTY QUERY
    # =================================

    if not original_query:

        return {

            "query":
                original_query,

            "resolved_query":
                original_query,

            "was_resolved":
                False,

            "reason":
                "empty_query",

        }

    # =================================
    # NO HISTORY
    # =================================

    if not history:

        return {

            "query":
                original_query,

            "resolved_query":
                original_query,

            "was_resolved":
                False,

            "reason":
                "no_conversation_history",

        }

    # =================================
    # QUERY IS ALREADY STANDALONE
    # =================================

    if not is_context_dependent_query(
        original_query
    ):

        return {

            "query":
                original_query,

            "resolved_query":
                original_query,

            "was_resolved":
                False,

            "reason":
                "standalone_query",

        }

    # =================================
    # BUILD RESOLUTION PROMPT
    # =================================

    prompt = build_query_resolution_prompt(

        query=original_query,

        conversation_history=history,

    )

    # =================================
    # RESOLVE WITH MODEL
    # =================================

    result = LLMTask.query_resolution(

        prompt=prompt,

        model=model,

        provider=provider,
        


    )

    resolved_query = clean_resolved_query(
        result
    )

    # =================================
    # SAFE FALLBACK
    # =================================

    if not resolved_query:

        return {

            "query":
                original_query,

            "resolved_query":
                original_query,

            "was_resolved":
                False,

            "reason":
                "empty_resolution",

        }

    # =================================
    # DONE
    # =================================

    return {

        "query":
            original_query,

        "resolved_query":
            resolved_query,

        "was_resolved":
            (
                resolved_query
                !=
                original_query
            ),

        "reason":
            "context_reference_resolved",

    }