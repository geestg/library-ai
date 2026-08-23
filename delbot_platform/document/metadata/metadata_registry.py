from __future__ import annotations


import json

from pathlib import Path



class MetadataRegistry:


    def __init__(
        self,
        metadata_path:str,
        pdf_dir:str
    ):


        self.metadata_path = Path(
            metadata_path
        )


        self.pdf_dir = Path(
            pdf_dir
        )


        self.metadata=[]

        self.pdfs=[]


        self.load()



    def load(self):


        with open(
            self.metadata_path,
            encoding="utf-8"
        ) as f:

            self.metadata=json.load(f)



        self.pdfs=sorted(
            self.pdf_dir.glob("*.pdf")
        )



    def get(
        self,
        pdf_path:str
    ):


        pdfs=[
            str(x)
            for x in self.pdfs
        ]


        target=str(
            Path(pdf_path)
        )


        if target in pdfs:


            index=pdfs.index(
                target
            )


            if index < len(self.metadata):

                return self.metadata[index]



        return {

            "title":Path(pdf_path).stem,

            "author":"",

            "year":"",

            "abstract":"",

            "prodi":"",

            "url":""

        }
