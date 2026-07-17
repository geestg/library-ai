from __future__ import annotations


from delbot_platform.repository.services.repository_service import (
    RepositoryService,
)


from delbot_platform.repository.services.artifact_service import (
    RepositoryArtifactService,
)


from delbot_platform.repository.integration.document_bridge import (
    RepositoryDocumentBridge,
)


from delbot_platform.repository.models import (
    Manifest,
)


from delbot_platform.documents.pipeline.indexing import (
    DocumentIndexingPipeline,
)



class RepositoryIndexService:
    """
    Repository indexing orchestration.

    Flow:

        Repository Item
              |
              v
        Artifact Resolver
              |
              v
        Manifest
              |
              v
        Document Pipeline
              |
              v
        Vector Index
    """


    def __init__(
        self,
        repository_service: RepositoryService | None = None,
        artifact_service: RepositoryArtifactService | None = None,
        bridge: RepositoryDocumentBridge | None = None,
        indexing_pipeline: DocumentIndexingPipeline | None = None,
    ) -> None:


        self.repository_service = (
            repository_service
            if repository_service is not None
            else RepositoryService()
        )


        self.artifact_service = (
            artifact_service
            if artifact_service is not None
            else RepositoryArtifactService()
        )


        self.bridge = (
            bridge
            if bridge is not None
            else RepositoryDocumentBridge()
        )


        self.pipeline = (
            indexing_pipeline
            if indexing_pipeline is not None
            else DocumentIndexingPipeline()
        )



    async def index(
        self,
        item_id: str,
    ):


        item = (
            self.repository_service
            .get_item(
                item_id,
            )
        )


        if item is None:

            raise ValueError(
                f"Repository item not found: {item_id}"
            )


        #
        # Resolve PDF Artifact
        #

        pdf_path = (
            self.artifact_service
            .resolve(
                item_id,
            )
        )


        #
        # Create Manifest
        #

        manifest = Manifest(

            document_id=item.id,

            checksum="",

            pdf_path=str(
                pdf_path,
            ),

            processed=False,

        )


        #
        # Document indexing
        #

        result = await self.pipeline.index(
            str(
                pdf_path,
            ),
        )


        #
        # Update processed state
        #

        manifest.processed = True


        self.repository_service.update_manifest(
            manifest,
        )


        return result