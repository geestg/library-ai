from __future__ import annotations


from delbot_platform.repository import (
    Manifest,
)


from delbot_platform.repository.integration.indexing_adapter import (
    DocumentIndexingAdapter,
)



class RepositoryDocumentBridge:
    """
    Connects repository artifacts
    into DELBot document intelligence.
    """


    def __init__(
        self,
        indexer: DocumentIndexingAdapter | None = None,
    ) -> None:


        self.indexer = (
            indexer
            if indexer is not None
            else DocumentIndexingAdapter()
        )


    async def process(
        self,
        manifest: Manifest,
    ):


        result = await self.indexer.index(
            manifest.pdf_path,
        )


        return result
