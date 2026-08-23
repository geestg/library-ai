from __future__ import annotations


from pathlib import Path

import json


from delbot_platform.repository.models import (
    RepositoryItem,
)



class PDFManifestBuilder:
    """
    Build persistent PDF availability manifest.
    """


    def __init__(
        self,
        output: str = "data/repository/manifests/pdf_manifest.json",
    ) -> None:


        self.output = Path(
            output
        )



    def build(
        self,
        items: list[RepositoryItem],
    ) -> Path:


        self.output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )


        documents = []


        for item in items:


            documents.append(
                {

                    "document_id":
                        item.id,


                    "title":
                        item.metadata.get(
                            "title"
                        ),


                    "author":
                        item.metadata.get(
                            "author"
                        ),


                    "year":
                        item.metadata.get(
                            "year"
                        ),


                    "prodi":
                        item.metadata.get(
                            "prodi"
                        ),


                    "repository_url":
                        item.repository_url,


                    "pdf_path":
                        item.local_path,


                    "status":
                        (
                            "available"
                            if item.local_path
                            else
                            "missing"
                        )

                }
            )



        with self.output.open(
            "w",
            encoding="utf-8",
        ) as f:


            json.dump(
                documents,
                f,
                indent=2,
                ensure_ascii=False,
            )



        return self.output


