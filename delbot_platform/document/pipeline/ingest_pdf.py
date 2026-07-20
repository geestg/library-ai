from __future__ import annotations



from delbot_platform.document.pipeline.pdf_loader import (
    PDFLoader,
)


from delbot_platform.document.pipeline.chunker import (
    DocumentChunker,
)


from delbot_platform.document.ingestion.qdrant_ingest import (
    QdrantIngest,
)



class PDFIngestion:


    def __init__(self):

        self.loader=PDFLoader()

        self.chunker=DocumentChunker()

        self.database=QdrantIngest()



    def ingest(
        self,
        pdf_path:str,
    ):


        pages=self.loader.load(
            pdf_path
        )


        chunks=self.chunker.chunk(
            pages
        )


        for chunk in chunks:


            self.database.insert(
                chunk["text"],
                {
                    "source":pdf_path,
                    "page":chunk["page"],
                    "type":"pdf_chunk",
                }
            )


        return {
            "pages":len(pages),
            "chunks":len(chunks),
        }
