from __future__ import annotations


import json

from pathlib import Path



class MetadataRetriever:


    def __init__(
        self,
        metadata_file:str
    ):


        self.path = Path(metadata_file)


        with open(
            self.path,
            encoding="utf-8"
        ) as f:

            self.documents = json.load(f)



    def search(
        self,
        query:str,
        limit:int=5
    ):


        query = query.lower()


        results=[]


        for item in self.documents:


            score=0


            fields=[

                item.get(
                    "title",
                    ""
                ),

                item.get(
                    "abstract",
                    ""
                ),

                item.get(
                    "prodi",
                    ""
                ),

            ]


            text=" ".join(fields).lower()



            for word in query.split():

                if word in text:

                    score += 1



            if score>0:


                results.append(
                    {
                        "score":score,
                        "source":"metadata",
                        "title":item.get(
                            "title"
                        ),
                        "author":item.get(
                            "author"
                        ),
                        "year":item.get(
                            "year"
                        ),
                        "abstract":item.get(
                            "abstract"
                        ),
                        "url":item.get(
                            "url"
                        )
                    }
                )



        results.sort(
            key=lambda x:x["score"],
            reverse=True
        )


        return results[:limit]
