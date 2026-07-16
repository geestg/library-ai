from __future__ import annotations


from delbot_platform.knowledge.retrieval.result import (
    RetrievalResult,
)



class ContextBuilder:


    def build(
        self,
        results: list[RetrievalResult],
    ) -> str:


        sections: list[str] = []


        for index, item in enumerate(
            results,
            start=1,
        ):


            metadata = item.metadata


            source = metadata.get(
                "source",
                "unknown",
            )


            section = metadata.get(
                "section",
                "unknown",
            )


            page_start = metadata.get(
                "page_start",
                "",
            )


            page_end = metadata.get(
                "page_end",
                "",
            )


            sections.append(

                "\n".join(

                    [

                        f"[SOURCE {index}]",

                        f"Document: {source}",

                        f"Section: {section}",

                        f"Pages: {page_start}-{page_end}",

                        "",

                        item.content,

                    ]

                )

            )


        return "\n\n".join(
            sections
        )