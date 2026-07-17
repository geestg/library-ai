from __future__ import annotations

from dataclasses import replace

from delbot_platform.repository.ingestion import (
    MetadataParser,
)

from delbot_platform.repository.models import (
    RepositoryItem,
)


class DSpaceMetadataParser(
    MetadataParser,
):

    def parse(
        self,
        item: RepositoryItem,
        raw: dict,
    ) -> RepositoryItem:


        metadata = raw.get(
            "metadata",
            {},
        )


        title = (
            metadata.get(
                "dc.title",
            )
            or item.title
        )


        bitstreams = raw.get(
            "bitstreams",
            [],
        )


        pdf_url = None


        for bitstream in bitstreams:

            name = (
                bitstream.get(
                    "name",
                    "",
                )
            )


            if name.lower().endswith(
                ".pdf"
            ):

                pdf_url = (
                    bitstream.get(
                        "url"
                    )
                )

                break



        return replace(
            item,
            title=title,
            source_url=pdf_url,
        )