from __future__ import annotations


from delbot_platform.knowledge.citation.source import (
    CitationSource,
)


from delbot_platform.knowledge.reranking.result import (
    RerankResult,
)



class CitationBuilder:


    def build(
        self,
        results: list[RerankResult],
    ) -> list[CitationSource]:


        citations = []


        for item in results:


            metadata = item.metadata


            citations.append(

                CitationSource(

                    document_id=metadata.get(
                        "document_id",
                        "",
                    ),

                    source=metadata.get(
                        "source",
                        "",
                    ),

                    section=metadata.get(
                        "section",
                        "",
                    ),

                    page_start=metadata.get(
                        "page_start",
                    ),

                    page_end=metadata.get(
                        "page_end",
                    ),

                )

            )


        return citations