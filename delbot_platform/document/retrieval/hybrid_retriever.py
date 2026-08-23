from __future__ import annotations



from delbot_platform.document.retrieval.metadata_retriever import (
    MetadataRetriever
)


from delbot_platform.document.ingestion.qdrant_ingest import (
    QdrantIngest
)



class HybridRetriever:


    def __init__(self):


        self.metadata = MetadataRetriever(
            "delbot_platform/repository_data/metadata/skripsi_dataset.json"
        )


        self.qdrant = QdrantIngest()



    def search(
        self,
        query:str,
        limit:int=5
    ):


        metadata_results = self.metadata.search(
            query,
            limit
        )


        pdf_results=[]


        try:

            pdf_results = self.qdrant.search(
                query,
                limit
            )


        except Exception:


            pass



        return {


            "metadata":

                metadata_results,


            "pdf":

                pdf_results


        }
