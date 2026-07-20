from __future__ import annotations


import json

from pathlib import Path


from delbot_platform.repository.models import (
    RepositoryItem,
)



class DatasetLoader:


    def __init__(
        self,
        path: str,
    ) -> None:


        self.path = Path(
            path
        )



    def _generate_id(
        self,
        url: str,
    ) -> str:


        parts = (
            url
            .rstrip("/")
            .split("/")
        )


        if len(parts) >= 2:

            return (
                parts[-2]
                +
                "-"
                +
                parts[-1]
            )


        return parts[-1]



    def load(
        self,
    ) -> list[RepositoryItem]:


        data = json.loads(
            self.path.read_text(
                encoding="utf-8"
            )
        )


        items = []


        for row in data:


            item = RepositoryItem(

                id=self._generate_id(
                    row["url"]
                ),

                title=row.get(
                    "title",
                    "",
                ),

                repository_url=row["url"],

                metadata=row,

            )


            items.append(
                item
            )


        return items