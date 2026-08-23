from __future__ import annotations


from delbot_platform.document.pipeline.pdf_loader import PDFLoader


from delbot_platform.document.pipeline.chunker import DocumentChunker


from delbot_platform.document.ingestion.qdrant_ingest import QdrantIngest


from delbot_platform.document.metadata.pdf_metadata import PDFMetadataResolver




class PDFIngestion:



    def __init__(self):


        self.loader=PDFLoader()


        self.chunker=DocumentChunker(
            size=500
        )


        self.qdrant=QdrantIngest()


        self.metadata=PDFMetadataResolver(

            "delbot_platform/repository_data/metadata/skripsi_dataset.json"

        )




    def ingest(
        self,
        pdf_path:str
    ):


        pages=self.loader.load(
            pdf_path
        )


        chunks=self.chunker.chunk(
            pages
        )


        metadata=self.metadata.resolve(
            pdf_path
        )


        inserted=0



        for chunk in chunks:


            payload={

                **metadata,


                "source_file":pdf_path,


                "page":chunk["page"],


                "text":chunk["text"],


                "type":"pdf"

            }



            self.qdrant.insert(

                chunk["text"],

                payload

            )


            inserted+=1



        return {

            "file":pdf_path,

            "pages":len(pages),

            "chunks":inserted

        }

