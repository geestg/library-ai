# =====================================
# DOCUMENT CHAT MEMORY
# =====================================

DOCUMENT_CHAT_MEMORY = {}


def get_document_history(
    document_id: str
):

    return DOCUMENT_CHAT_MEMORY.get(
        document_id,
        []
    )


def append_document_history(

    document_id: str,

    role: str,

    content: str
):

    if document_id not in DOCUMENT_CHAT_MEMORY:

        DOCUMENT_CHAT_MEMORY[
            document_id
        ] = []

    DOCUMENT_CHAT_MEMORY[
        document_id
    ].append({

        "role": role,

        "content": content
    })

    # keep last 10 messages

    DOCUMENT_CHAT_MEMORY[
        document_id
    ] = DOCUMENT_CHAT_MEMORY[
        document_id
    ][-10:]

