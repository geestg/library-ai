from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

# =====================================
# TEXT SPLITTER
# =====================================

splitter = RecursiveCharacterTextSplitter(

    chunk_size=1200,

    chunk_overlap=200,

    separators=[

        "\n\n",

        "\n",

        ". ",

        " ",

        ""
    ]
)

# =====================================
# CHUNK PLAIN TEXT
# =====================================

def chunk_plain_text(text):

    chunks = splitter.split_text(text)

    results = []

    for idx, chunk in enumerate(chunks):

        results.append({

            "text": chunk,

            "metadata": {

                "chunk_index": idx,

                "chunk_length": len(chunk)
            }
        })

    return results


# =====================================
# CHUNK PAGE-BASED TEXT
# =====================================

def chunk_pages(

    pages,

    metadata=None
):

    if metadata is None:

        metadata = {}

    results = []

    chunk_index = 0

    # =================================
    # LOOP PAGES
    # =================================

    for page_data in pages:

        page_number = page_data["page"]

        page_text = page_data["text"]

        # =============================
        # SKIP EMPTY PAGE
        # =============================

        if not page_text.strip():

            continue

        # =============================
        # SPLIT PAGE
        # =============================

        chunks = splitter.split_text(
            page_text
        )

        # =============================
        # LOOP CHUNKS
        # =============================

        for chunk in chunks:

            results.append({

                "text": chunk,

                "metadata": {

                    **metadata,

                    "page": page_number,

                    "chunk_index": chunk_index,

                    "chunk_length": len(chunk)
                }
            })

            chunk_index += 1

    return results


# =====================================
# BACKWARD COMPATIBILITY
# =====================================

def chunk_text(data, metadata=None):

    # =============================
    # STRING INPUT
    # =============================

    if isinstance(data, str):

        return chunk_plain_text(data)

    # =============================
    # PAGE LIST INPUT
    # =============================

    if isinstance(data, list):

        return chunk_pages(
            data,
            metadata
        )

    raise ValueError(
        "Unsupported chunk input type"
    )