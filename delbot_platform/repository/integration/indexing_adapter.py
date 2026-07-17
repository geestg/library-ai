from __future__ import annotations


from delbot_platform.documents.pipeline.indexing import (
    DocumentIndexingPipeline,
)


class DocumentIndexingAdapter:
    """
    Adapter between Repository Engine
    and Document Intelligence Pipeline.
    """


    def __init__(
        self,
        indexing_pipeline: DocumentIndexingPipeline | None = None,
    ) -> None:

        self.pipeline = (
            indexing_pipeline
            if indexing_pipeline is not None
            else DocumentIndexingPipeline()
        )


    async def index(
        self,
        pdf_path: str,
    ):

        result = await self.pipeline.index(
            pdf_path,
        )

        return result
