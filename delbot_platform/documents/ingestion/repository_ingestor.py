from __future__ import annotations


from pathlib import Path


from delbot_platform.repository import (
    RepositoryDocumentLoader,
)


from delbot_platform.documents.pipeline.indexing import (
    DocumentIndexingPipeline,
)



class RepositoryDocumentIngestor:
    """
    Adapter between repository documents
    and DELBot document indexing pipeline.
    """


    def __init__(
        self,
        repository_loader: RepositoryDocumentLoader | None = None,
        indexing_pipeline: DocumentIndexingPipeline | None = None,
    ) -> None:


        self.repository_loader = (
            repository_loader
            if repository_loader is not None
            else RepositoryDocumentLoader()
        )


        self.pipeline = (
            indexing_pipeline
            if indexing_pipeline is not None
            else DocumentIndexingPipeline()
        )



    async def ingest_available_documents(
        self,
    ) -> list:


        documents = (
            self.repository_loader.load_available()
        )


        results = []


        for document in documents:


            pdf_path = Path(
                document["pdf_path"]
            )


            if not pdf_path.exists():

                continue



            result = await self.pipeline.index(
                str(pdf_path)
            )


            results.append(
                {
                    "document_id":
                        document["document_id"],

                    "result":
                        result,
                }
            )


        return results
