from .document import (
    router as document_router,
)

from .research import (
    router as research_router,
)

from .repository import (
    router as repository_router,
)


__all__ = [

    "document_router",

    "research_router",

    "repository_router",

]
