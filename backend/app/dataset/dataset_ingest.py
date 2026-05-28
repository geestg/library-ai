import uuid

from qdrant_client.models import PointStruct

from app.dataset.thesis_parser import (
    load_dataset
)

from app.dataset.thesis_cleaner import (
    clean_text
)

from app.dataset.metadata_extractor import (
    extract_metadata
)

from app.rag.embedder import (
    get_embedding
)

from app.rag.chunker import (
    chunk_text
)

from app.rag.qdrant_client import (
    client,
    ensure_collection_exists
)

from app.core.constants import (
    THESIS_DATASET_COLLECTION
)


# =====================================
# BUILD RAW TEXT
# =====================================

def build_raw_text(item):

    return f"""
    Title:
    {item.get("title", "")}

    Abstract:
    {item.get("abstract", "")}

    Keywords:
    {item.get("keywords", "")}

    Method:
    {item.get("method", "")}

    Department:
    {item.get("prodi", "")}
    """


# =====================================
# INGEST DATASET
# =====================================

def ingest_dataset():

    print("\n[START] Dataset ingestion process")

    # =================================
    # ENSURE COLLECTION
    # =================================

    ensure_collection_exists(
        THESIS_DATASET_COLLECTION
    )

    # =================================
    # LOAD DATASET
    # =================================

    dataset = load_dataset(
        "app/dataset/skripsi_dataset.json"
    )

    print(
        f"\n[DATASET LOADED] "
        f"{len(dataset)} items"
    )

    if len(dataset) == 0:

        print("[ERROR] Empty dataset")
        return

    print("\n[DATASET SAMPLE]")
    print(dataset[0])

    points = []

    # =================================
    # LOOP DATASET
    # =================================

    for item_index, item in enumerate(dataset):

        print(
            f"\n=============================="
        )

        print(
            f"[PROCESSING ITEM] "
            f"{item_index + 1}"
        )

        # =============================
        # EXTRACT METADATA
        # =============================

        metadata = extract_metadata(item)

        # =============================
        # BUILD RAW TEXT
        # =============================

        raw_text = build_raw_text(item)

        print(
            f"[RAW TEXT LENGTH] "
            f"{len(raw_text)}"
        )

        # =============================
        # CLEAN TEXT
        # =============================

        cleaned_text = clean_text(raw_text)

        print(
            f"[CLEANED TEXT LENGTH] "
            f"{len(cleaned_text)}"
        )

        if not cleaned_text:

            print("[SKIP] Empty cleaned text")
            continue

        # =============================
        # CHUNKING
        # =============================

        chunks = chunk_text(cleaned_text)

        print(
            f"[CHUNKS GENERATED] "
            f"{len(chunks)}"
        )

        if not chunks:

            print("[SKIP] No chunks generated")
            continue

        # =============================
        # LOOP CHUNKS
        # =============================

        for idx, chunk_data in enumerate(chunks):

            try:

                chunk_value = chunk_data["text"]

                chunk_metadata = chunk_data["metadata"]

                # =====================
                # EMBEDDING
                # =====================

                embedding = get_embedding(
                    chunk_value
                )

                # =====================
                # QDRANT POINT
                # =====================

                point = PointStruct(

                    id=str(uuid.uuid4()),

                    vector=embedding,

                    payload={

                        **metadata,

                        **chunk_metadata,

                        "chunk": chunk_value,

                        "chunk_index": idx,
                    }
                )

                points.append(point)

                print(
                    f"[EMBED SUCCESS] "
                    f"Chunk {idx + 1}"
                )

            except Exception as e:

                print(
                    f"[EMBED ERROR] "
                    f"{str(e)}"
                )

    # =================================
    # SUMMARY
    # =================================

    total_points = len(points)

    print(
        f"\n[TOTAL POINTS GENERATED] "
        f"{total_points}"
    )

    if total_points == 0:

        print(
            "\n[ERROR] No points generated. "
            "Check dataset structure."
        )

        return

    # =================================
    # UPSERT TO QDRANT
    # =================================

    try:

        BATCH_SIZE = 64

        for start_idx in range(
            0,
            total_points,
            BATCH_SIZE
        ):

            end_idx = start_idx + BATCH_SIZE

            batch = points[start_idx:end_idx]

            print(
                f"[UPSERT BATCH] "
                f"{start_idx} - {end_idx}"
            )

            client.upsert(

                collection_name=THESIS_DATASET_COLLECTION,

                points=batch
            )

        print(
            f"\n[UPSERT SUCCESS] "
            f"{total_points} chunks stored"
        )

    except Exception as e:

        print(
            f"\n[QDRANT ERROR] "
            f"{str(e)}"
        )


# =====================================
# MAIN
# =====================================

if __name__ == "__main__":

    ingest_dataset()