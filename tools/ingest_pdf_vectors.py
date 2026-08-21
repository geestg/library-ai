from __future__ import annotations


import sys

from pathlib import Path



ROOT=Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(ROOT)
)



from delbot_platform.document_intelligence.pipeline.pdf_pipeline import PDFPipeline

from delbot_platform.ai.client.embedding_client import EmbeddingClient

from delbot_platform.knowledge.vector.qdrant_store import QdrantStore



PDF_DIR=Path(
"delbot_platform/repository_data/thesis_files"
)



def main():


    print("="*60)
    print("PDF VECTOR INGEST")
    print("="*60)



    ingestion=PDFPipeline()

    embedder=EmbeddingClient()

    store=QdrantStore(
        "delbot_documents"
    )


    store.create_collection()



    total=0



    for pdf in PDF_DIR.glob("*.pdf"):


        print(
            "\nPDF:",
            pdf.name
        )


        result=ingestion.ingest(
            str(pdf)
        )



        chunks=result["chunks"]


        if not chunks:

            continue



        texts=[
            c["text"]
            for c in chunks
        ]


        vectors=embedder.embed(
            texts
        )



        payloads=[]


        for c in chunks:


            payloads.append(
                {
                    "type":"pdf",

                    "file":pdf.name,

                    "page":c["page"],

                    "text":c["text"],

                    **c["metadata"]
                }
            )



        inserted=store.insert(
            vectors,
            payloads
        )


        total+=inserted


        print(
            "INSERTED:",
            inserted
        )



    print(
        "\nTOTAL VECTOR:",
        total
    )



if __name__=="__main__":

    main()
