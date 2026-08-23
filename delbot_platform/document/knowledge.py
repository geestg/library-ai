from delbot_platform.document.pipeline import DocumentPipeline
from delbot_platform.document.embedding.client import EmbeddingClient
from delbot_platform.document.storage.qdrant import QdrantStorage



class KnowledgePipeline:


    def __init__(self):

        self.document = DocumentPipeline()

        self.embedding = EmbeddingClient()

        self.storage = QdrantStorage()



    def ingest(
        self,
        pdf:str,
    ):


        result = self.document.process(
            pdf
        )


        vectors=[]
        payloads=[]


        for chunk in result["data"]:

            vector = self.embedding.embed(
                chunk["text"]
            )


            vectors.append(vector)


            payloads.append(
                {
                    "page":chunk["page"],
                    "text":chunk["text"],
                }
            )


        if vectors:

            self.storage.ensure_collection(
                size=len(vectors[0])
            )


            self.storage.insert(
                vectors,
                payloads,
            )


        return {

            "pages":result["pages"],

            "chunks":len(vectors),

            "indexed":len(vectors)

        }
