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

            sections.append(
                "\n".join(
                    [
                        f"[SOURCE {index}]",
                        f"Document: {metadata.source}",
                        f"Section: {metadata.section}",
                        f"Pages: {metadata.page_start}-{metadata.page_end}",
                        "",
                        item.content,
                    ]
                )
            )

        return "\n\n".join(
            sections,
        )
