from __future__ import annotations


from pathlib import Path



class LocalPDFResolver:
    """
    Resolve PDF from local repository cache.

    Priority:
    datasets/{id}/Fulltext.pdf
    """


    def __init__(
        self,
        root: str = "datasets",
    ) -> None:

        self.root = Path(
            root
        )


    def resolve(
        self,
        item_id: str,
    ) -> Path | None:


        candidates = [

            self.root
            /
            "poc"
            /
            item_id
            /
            "Fulltext.pdf",


            self.root
            /
            item_id
            /
            "Fulltext.pdf",


            self.root
            /
            item_id
            /
            "fulltext.pdf",

        ]


        for path in candidates:


            if path.exists():

                return path.resolve()



        return None
