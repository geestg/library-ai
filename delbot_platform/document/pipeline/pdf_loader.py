from __future__ import annotations


from pathlib import Path


import fitz



class PDFLoader:


    def load(
        self,
        path:str,
    ):


        document = fitz.open(
            path
        )


        pages=[]


        for index,page in enumerate(document):

            text = page.get_text()


            pages.append(
                {
                    "page":index+1,
                    "text":text,
                }
            )


        return pages
