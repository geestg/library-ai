from .models import (
    Repository,
    Collection,
    RepositoryItem,
    Manifest,
)


from .services import (
    RepositoryService,
    RepositoryIngestionService,
    RepositoryCrawlService,
    RepositoryIndexService,
    RepositoryArtifactService,
)


from .scanner import (
    RepositoryScanner,
    CollectionScanner,
    ItemScanner,
)


from .ingestion import (
    MetadataParser,
    FileParser,
    FileDownloader,
)


from .dspace import (
    DSpaceClient,
    DSpaceHTTPClient,
    DSpaceMetadataParser,
    DSpaceFileParser,
    DSpaceDownloader,
    DSpaceURLResolver,
)


from .auth import (
    RepositoryCredential,
    RepositorySession,
    RepositoryAuthManager,
    GitLabAuth,
    RepositoryCredentialLoader,
    EnvironmentCredentialProvider,
)


from .manifest import (
    ManifestBuilder,
)


from .crawler import (
    CollectionCrawler,
    RepositoryCrawler,
)


from .state import (
    DocumentState,
    DocumentStatus,
    CheckpointManager,
)


from .engine import (
    RepositoryEngine,
    RepositoryPipeline,
    RepositoryPipelineResult,
)


from .integration import (
    DocumentIndexingAdapter,
    RepositoryDocumentBridge,
)


from .orchestration import (
    RepositoryWorkflow,
    RepositoryWorkflowResult,
)


from .api import (
    router as repository_router,
    RepositoryAPIService,
    RepositoryRegisterRequest,
    RepositoryIngestRequest,
    RepositoryStatusResponse,
    RepositoryIndexResponse,
)



__all__ = [

    # Models

    "Repository",

    "Collection",

    "RepositoryItem",

    "Manifest",



    # Services

    "RepositoryService",

    "RepositoryIngestionService",

    "RepositoryCrawlService",

    "RepositoryIndexService",

    "RepositoryArtifactService",



    # Scanner

    "RepositoryScanner",

    "CollectionScanner",

    "ItemScanner",



    # Ingestion

    "MetadataParser",

    "FileParser",

    "FileDownloader",



    # DSpace

    "DSpaceClient",

    "DSpaceHTTPClient",

    "DSpaceMetadataParser",

    "DSpaceFileParser",

    "DSpaceDownloader",

    "DSpaceURLResolver",



    # Authentication

    "RepositoryCredential",

    "RepositorySession",

    "RepositoryAuthManager",

    "GitLabAuth",

    "RepositoryCredentialLoader",



    # Manifest

    "ManifestBuilder",



    # Crawler

    "CollectionCrawler",

    "RepositoryCrawler",



    # State

    "DocumentState",

    "DocumentStatus",

    "CheckpointManager",



    # Engine

    "RepositoryEngine",

    "RepositoryPipeline",

    "RepositoryPipelineResult",



    # Integration

    "DocumentIndexingAdapter",

    "RepositoryDocumentBridge",



    # Orchestration

    "RepositoryWorkflow",

    "RepositoryWorkflowResult",



    # API

    "repository_router",

    "RepositoryAPIService",

    "RepositoryRegisterRequest",

    "RepositoryIngestRequest",

    "RepositoryStatusResponse",

    "RepositoryIndexResponse",

    "EnvironmentCredentialProvider",

]