from __future__ import annotations


import requests



class RerankerClient:



    def __init__(
        self,
        url="http://localhost:8106/v1/rerank"
    ):

        self.url=url



    def rerank(
        self,
        query:str,
        documents:list[dict]
    ):


        texts=[]


        for doc in documents:

            texts.append(
                doc["text"]
            )



        response=requests.post(

            self.url,

            json={

                "query":query,

                "documents":texts

            },

            timeout=600

        )



        response.raise_for_status()



        ranked=response.json()["results"]



        output=[]



        for item in ranked:


            original=documents[
                item["index"]
            ]


            output.append(

                {

                    **original,

                    "rerank_score":item["score"]

                }

            )


        return output
