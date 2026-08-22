import json
import re
import uuid
from qdrant_client.models import PointStruct
from app.rag.embedder import get_embedding
from app.rag.qdrant_client import client, ensure_collection_exists
from app.core.constants import THESIS_DATASET_COLLECTION

DATASET_PATH = "/app/app/dataset/skripsi_dataset_trpl.json"
CHUNK_SIZE   = 800
CHUNK_OVERLAP = 100
BATCH_SIZE   = 16

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"\r\n", " ", text)
    text = re.sub(r"\n+",  " ", text)
    text = re.sub(r"\s+",  " ", text)
    return text.strip()

def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    text = text.strip()
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        start += size - overlap
    return chunks

def build_chunks(item: dict) -> list:
    title    = clean_text(item.get("title",  ""))
    author   = clean_text(item.get("author", ""))
    year     = item.get("year",  "")
    prodi    = item.get("prodi", "")
    url      = item.get("url",   "")
    keywords = item.get("keywords", [])
    content  = item.get("content", {})

    base_payload = {
        "title"   : title,
        "author"  : author,
        "year"    : year,
        "prodi"   : prodi,
        "url"     : url,
        "keywords": keywords,
    }

    all_chunks = []

    # --- Abstract ---
    abstract = clean_text(content.get("abstract", ""))
    if not abstract:
        abstract = clean_text(item.get("abstract", ""))

    if abstract:
        text = f"Judul: {title}\nAbstrak: {abstract}"
        all_chunks.append({
            **base_payload,
            "source_bab": "abstract",
            "chunk": clean_text(text),
        })

    # --- Bab 1, 3, 5 ---
    bab_map = {
        "bab1": "Bab 1 - Pendahuluan",
        "bab3": "Bab 3 - Metodologi",
        "bab5": "Bab 5 - Kesimpulan",
    }

    for bab_key, bab_label in bab_map.items():
        bab_text = clean_text(content.get(bab_key, ""))
        if not bab_text:
            continue

        sub_chunks = chunk_text(bab_text)
        for idx, sub in enumerate(sub_chunks):
            all_chunks.append({
                **base_payload,
                "source_bab"  : bab_key,
                "source_label": bab_label,
                "chunk_index" : idx,
                "chunk"       : sub,
            })

    return all_chunks

def ingest_trpl():
    print("\n" + "="*60)
    print("INGEST NEW TRPL THESIS DATA ONLY")
    print("="*60)

    ensure_collection_exists(THESIS_DATASET_COLLECTION)

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    print(f"[LOAD] {len(dataset)} new TRPL records loaded")

    all_chunk_dicts = []
    for item in dataset:
        all_chunk_dicts.extend(build_chunks(item))

    print(f"[CHUNK] {len(all_chunk_dicts)} TRPL chunks generated")

    if not all_chunk_dicts:
        print("[ERROR] No chunks generated.")
        return

    points_buffer = []
    errors        = 0
    success       = 0

    for i, chunk_dict in enumerate(all_chunk_dicts):
        chunk_text_val = chunk_dict["chunk"]
        if not chunk_text_val:
            continue

        try:
            vector = get_embedding(chunk_text_val)
            point = PointStruct(
                id      = str(uuid.uuid4()),
                vector  = vector,
                payload = chunk_dict,
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
                print(f"[UPSERT] {success} embedded | {errors} errors | batch {i // BATCH_SIZE}")
            except Exception as e:
                print(f"[QDRANT ERROR] {str(e)}")
            points_buffer = []

    if points_buffer:
        try:
            client.upsert(
                collection_name=THESIS_DATASET_COLLECTION,
                points=points_buffer,
            )
        except Exception as e:
            print(f"[QDRANT FLUSH ERROR] {str(e)}")

    print("\n" + "="*60)
    print("TRPL INGESTION COMPLETE")
    print(f"  Total chunks embedded : {success}")
    print(f"  Total errors          : {errors}")
    print("="*60)

if __name__ == "__main__":
    ingest_trpl()
