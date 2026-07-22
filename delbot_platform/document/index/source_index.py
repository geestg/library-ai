from __future__ import annotations


from qdrant_client import QdrantClient



class SourceIndex:



    COLLECTION="delbot_documents"



    def __init__(self):

        self.client=QdrantClient(

            host="127.0.0.1",

            port=6333

        )



    def build(self):


        sources={}


        offset=None



        while True:


            points,offset=self.client.scroll(

                collection_name=self.COLLECTION,

                limit=100,

                offset=offset

            )



            for point in points:


                payload=point.payload


                source=payload.get(
                    "source"
                )


                if not source:

                    continue



                if source not in sources:


                    sources[source]={

                        "pages":0,

                        "sample":""

                    }



                sources[source]["pages"]+=1



                if not sources[source]["sample"]:

                    sources[source]["sample"]=payload.get(
                        "text",
                        ""
                    )[:500]



            if offset is None:

                break



        return sources
