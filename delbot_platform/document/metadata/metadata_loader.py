from __future__ import annotations


import json

from pathlib import Path



class MetadataLoader:


    def __init__(
        self,
        path:str
    ):

        self.path = Path(path)



    def load(self):

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as f:

            data=json.load(f)


        return data
