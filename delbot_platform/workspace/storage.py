from __future__ import annotations


import json

from pathlib import Path



class WorkspaceStorage:


    def __init__(self):

        self.path = Path(
            "runtime/workspace/sessions.json"
        )


        self.path.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        if not self.path.exists():

            self.save({})



    def load(self):

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def save(self,data):

        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False
            )
