from __future__ import annotations


from pathlib import Path

import json



class RepositoryDocumentLoader:
    """
    Load available PDF documents
    from repository manifest.
    """


    def __init__(
        self,
        manifest_path: str = "data/repository/manifests/pdf_manifest.json",
    ) -> None:


        self.manifest_path = Path(
            manifest_path
        )



    def load_available(
        self,
    ) -> list[dict]:


        if not self.manifest_path.exists():

            raise FileNotFoundError(
                self.manifest_path
            )


        with self.manifest_path.open(
            "r",
            encoding="utf-8",
        ) as file:


            data = json.load(
                file
            )



        documents = []


        for item in data:


            if (
                item["status"]
                ==
                "available"
                and
                item["pdf_path"]
            ):


                documents.append(
                    item
                )


        return documents

