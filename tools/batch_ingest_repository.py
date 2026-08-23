from __future__ import annotations


import sys
import json


from pathlib import Path


ROOT=Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(ROOT)
)



from delbot_platform.document.pipeline.ingest_pdf import PDFIngestion

from delbot_platform.ai.client.embedding_client import EmbeddingClient

from delbot_platform.knowledge.vector.qdrant_store import QdrantStore



PDF_DIR=Path(
    "delbot_platform/repository_data/thesis_files"
)


META_FILE=Path(
    "delbot_platform/repository_data/metadata/skripsi_dataset.json"
)



def load_metadata():

    with open(
        META_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def main():


    print("="*60)
    print("DELBot BATCH VECTOR INGEST")
    print("="*60)


    pdfs=list(
        PDF_DIR.glob("*.pdf")
    )


    print(
        "PDF COUNT:",
        len(pdfs)
    )


    metadata=load_metadata()


    pdf_engine=PDFIngestion()

    embedder=EmbeddingClient()

    store=QdrantStore()


    store.create_collection(
        1024
    )


    total=0


    for index,pdf in enumerate(
        pdfs,
        start=1
    ):


        print()
        print(
            f"[{index}/{len(pdfs)}]",
            pdf.name
        )


        result=pdf_engine.ingest(
            str(pdf)
        )


        chunks=result.get(
            "chunks",
            []
        )


        if not chunks:

            print(
                "NO CHUNKS"
            )

            continue



        print(
            "Chunks:",
            len(chunks)
        )


        vectors=embedder.embed(
            chunks
        )


        print(
            "Vectors:",
            len(vectors)
        )


        payloads=[]


        meta=metadata[
            (index-1) % len(metadata)
        ]


        for chunk in chunks:


            payloads.append(
                {
                    "text":chunk,
                    "title":meta.get("title"),
                    "author":meta.get("author"),
                    "year":meta.get("year"),
                    "prodi":meta.get("prodi"),
                    "source":pdf.name
                }
            )



        inserted=store.insert(
            vectors,
            payloads
        )


        total+=inserted


        print(
            "Inserted:",
            inserted
        )



    print()
    print("="*60)
    print(
        "TOTAL VECTOR:",
        total
    )


    print(
        "QDRANT COUNT:",
        store.count()
    )


    print(
        "DONE"
    )



if __name__=="__main__":
    main()
