from __future__ import annotations

from dataclasses import replace

from delbot_platform.repository.ingestion import (
    FileParser,
)

from delbot_platform.repository.models import (
    RepositoryItem,
)


class DSpaceFileParser(
    FileParser,
):

    def parse(
        self,
        item: RepositoryItem,
        raw: dict,
    ) -> RepositoryItem:


        files = raw.get(
            "files",
            [],
        )


        pdf_path = item.pdf_path


        for file in files:

            name = file.get(
                "name",
                "",
            )


            if name.lower().endswith(
                ".pdf"
            ):

                pdf_path = name

                break


        return replace(
            item,
            pdf_path=pdf_path,
        )