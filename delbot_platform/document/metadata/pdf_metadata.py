from __future__ import annotations


import json

from pathlib import Path



class PDFMetadataResolver:



    def __init__(
        self,
        metadata_file:str
    ):


        self.items=json.loads(

            Path(metadata_file)
            .read_text(
                encoding="utf-8"
            )

        )



    def resolve(
        self,
        pdf_path:str
    ):


        filename=Path(pdf_path).stem



        for item in self.items:


            url=item.get(
                "url",
                ""
            )


            if filename in url:


                return item



        return {

            "source_file":pdf_path

        }

