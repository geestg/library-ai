from __future__ import annotations


from dataclasses import dataclass


from delbot_platform.repository import (
    Manifest,
)


from delbot_platform.repository.integration import (
    RepositoryDocumentBridge,
)



@dataclass(slots=True)
class RepositoryWorkflowResult:

    manifest: Manifest

    indexed: bool

    index_result: object | None = None

    error: str | None = None



class RepositoryWorkflow:
    """
    Complete repository workflow.

    Flow:

        Repository
            |
            v
        Ingestion
            |
            v
        Manifest
            |
            v
        Document Intelligence
    """


    def __init__(
        self,
        pipeline,
        bridge: RepositoryDocumentBridge | None = None,
    ) -> None:


        self.pipeline = pipeline


        self.bridge = (
            bridge
            if bridge is not None
            else RepositoryDocumentBridge()
        )



    async def execute(
        self,
        item,
    ) -> RepositoryWorkflowResult:


        try:

            pipeline_result = (
                self.pipeline.execute(
                    item,
                )
            )


            if not pipeline_result.success:

                return RepositoryWorkflowResult(

                    manifest=pipeline_result.manifest,

                    indexed=False,

                    error=pipeline_result.error,

                )



            index_result = await self.bridge.process(

                pipeline_result.manifest,

            )


            return RepositoryWorkflowResult(

                manifest=pipeline_result.manifest,

                indexed=True,

                index_result=index_result,

            )


        except Exception as exc:


            return RepositoryWorkflowResult(

                manifest=None,

                indexed=False,

                error=str(exc),

            )
