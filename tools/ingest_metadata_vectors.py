from __future__ import annotations


import sys
import json
import uuid

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(ROOT)
)


from delbot_platform.ai.client.embedding_client import EmbeddingClient
from delbot_platform.knowledge.vector.qdrant_store import QdrantStore



META = Path(
    "delbot_platform/repository_data/metadata/skripsi_dataset.json"
)


BATCH_SIZE = 32



def main():

    print("="*60)
    print("METADATA VECTOR INGEST")
    print("="*60)


    with open(
        META,
        encoding="utf8"
    ) as f:

        items=json.load(f)


    print(
        "TOTAL:",
        len(items)
    )


    embedder = EmbeddingClient()


    store = QdrantStore(
        "delbot_metadata"
    )

    store.create_collection()


    total_inserted=0


    for start in range(
        0,
        len(items),
        BATCH_SIZE
    ):


        batch = items[
            start:start+BATCH_SIZE
        ]


        texts=[]
        payloads=[]


        for item in batch:


            text=f"""
Title:
{item.get('title','')}

Author:
{item.get('author','')}

Year:
{item.get('year','')}

Abstract:
{item.get('abstract','')}

Prodi:
{item.get('prodi','')}
"""


            texts.append(text)


            payloads.append(
                {
                    "id":str(uuid.uuid4()),

                    "type":"metadata",

                    **item
                }
            )



        print(
            f"BATCH {start}/{len(items)}"
        )


        vectors=embedder.embed(
            texts
        )


        inserted=store.insert(
            vectors,
            payloads
        )


        total_inserted += inserted


        print(
            "INSERTED:",
            total_inserted
        )



    print("="*60)
    print(
        "DONE:",
        total_inserted
    )
    print("="*60)



if __name__=="__main__":
    main()
