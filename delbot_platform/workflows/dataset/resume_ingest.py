"""
RESUME INGESTION & DE-DUPLICATE
================================
Membaca skripsi_dataset_enriched.json dan membandingkannya dengan Qdrant collection 'thesis_dataset'.
1. Menghapus data duplikat yang ada di Qdrant.
2. Melanjutkan ingesti chunk yang belum di-embed.
"""

import json
import re
import uuid
from qdrant_client.models import PointStruct, PointIdsList

from delbot_platform.research.retrieval.embedder import get_embedding
from delbot_platform.research.retrieval.qdrant_client import client, ensure_collection_exists
from delbot_platform.core.constants import THESIS_DATASET_COLLECTION
from delbot_platform.dataset.ingest_enriched import build_chunks, DATASET_PATH, BATCH_SIZE

def clean_and_resume():
    print("\n" + "="*60)
    print("RESUME INGESTION & DE-DUPLICATE SCRIPT")
    print("="*60)

    # 1. Scroll existing points from Qdrant
    print("[QDRANT] Scrolling existing points to find duplicates...")
    offset = None
    seen_chunks = {}  # key: (title, source_bab, chunk_index) -> point_id
    points_to_delete = []
    total_scrolled = 0

    while True:
        res = client.scroll(
            collection_name=THESIS_DATASET_COLLECTION,
            limit=1000,
            offset=offset,
            with_payload=True
        )
        points = res[0]
        offset = res[1]
        if not points:
            break
        
        for p in points:
            total_scrolled += 1
            payload = p.payload or {}
            title = payload.get("title")
            source_bab = payload.get("source_bab")
            chunk_index = payload.get("chunk_index", 0)
            
            key = (title, source_bab, chunk_index)
            if key in seen_chunks:
                # Duplicate found, mark for deletion
                points_to_delete.append(p.id)
            else:
                seen_chunks[key] = p.id
                
        if offset is None:
            break

    print(f"[QDRANT] Total points in DB: {total_scrolled}")
    print(f"[QDRANT] Unique points: {len(seen_chunks)}")
    print(f"[QDRANT] Duplicate points to delete: {len(points_to_delete)}")

    # Delete duplicates in batches
    if points_to_delete:
        print("[QDRANT] Deleting duplicates...")
        del_batch_size = 500
        for idx in range(0, len(points_to_delete), del_batch_size):
            batch = points_to_delete[idx : idx + del_batch_size]
            client.delete(
                collection_name=THESIS_DATASET_COLLECTION,
                points_selector=PointIdsList(points=batch)
            )
        print(f"[QDRANT] Successfully deleted {len(points_to_delete)} duplicate points.")

    # 2. Load enriched dataset
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    # Build all chunks
    all_chunk_dicts = []
    for item in dataset:
        all_chunk_dicts.extend(build_chunks(item))

    print(f"[LOAD] {len(all_chunk_dicts)} total chunks generated from JSON dataset.")

    # Filter chunks that are already in Qdrant
    chunks_to_ingest = []
    for chunk_dict in all_chunk_dicts:
        title = chunk_dict.get("title")
        source_bab = chunk_dict.get("source_bab")
        chunk_index = chunk_dict.get("chunk_index", 0)
        key = (title, source_bab, chunk_index)
        
        if key not in seen_chunks:
            chunks_to_ingest.append(chunk_dict)

    print(f"[FILTER] Chunks already in Qdrant: {len(all_chunk_dicts) - len(chunks_to_ingest)}")
    print(f"[FILTER] Chunks remaining to ingest: {len(chunks_to_ingest)}")

    if not chunks_to_ingest:
        print("[SUCCESS] All chunks are already ingested. Nothing to do!")
        return

    # Ingest remaining chunks
    points_buffer = []
    errors = 0
    success = 0

    print(f"[INGEST] Starting embedding and upsert for {len(chunks_to_ingest)} chunks...")
    for i, chunk_dict in enumerate(chunks_to_ingest):
        chunk_text_val = chunk_dict["chunk"]
        if not chunk_text_val:
            continue

        try:
            vector = get_embedding(chunk_text_val)
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload=chunk_dict,
            )
            points_buffer.append(point)
            success += 1
        except Exception as e:
            errors += 1
            print(f"[EMBED ERROR] chunk {i}: {str(e)}")
            continue

        if len(points_buffer) >= BATCH_SIZE:
            try:
                client.upsert(
                    collection_name=THESIS_DATASET_COLLECTION,
                    points=points_buffer,
                )
                print(
                    f"[UPSERT] {success}/{len(chunks_to_ingest)} embedded | "
                    f"{errors} errors | "
                    f"batch {i // BATCH_SIZE}"
                )
            except Exception as e:
                print(f"[QDRANT ERROR] {str(e)}")
            points_buffer = []

    # Flush remaining
    if points_buffer:
        try:
            client.upsert(
                collection_name=THESIS_DATASET_COLLECTION,
                points=points_buffer,
            )
            print(f"[UPSERT] Final flush: {len(points_buffer)} points upserted.")
        except Exception as e:
            print(f"[QDRANT FLUSH ERROR] {str(e)}")

    print("\n" + "="*60)
    print("INGESTION COMPLETE")
    print(f"  Total new chunks embedded : {success}")
    print(f"  Total errors              : {errors}")
    print("="*60)

if __name__ == "__main__":
    clean_and_resume()
