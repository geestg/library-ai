from __future__ import annotations

from pathlib import Path

from delbot_platform.documents.registry.manager import (
    DocumentRegistryManager,
)
from delbot_platform.knowledge.hydration.base import (
    DocumentProvider,
)
from delbot_platform.knowledge.models import (
    Author,
    Collection,
    Document,
    KnowledgeDomain,
    KnowledgeSource,
    Repository,
)
from delbot_platform.research.models import Citation


class LocalDocumentProvider(DocumentProvider):

    def __init__(
        self,
    ) -> None:

        self.registry = DocumentRegistryManager()

    async def citation(
        self,
        document_id: str,
        page_start: int,
        page_end: int,
        section: str,
        text: str,
    ) -> Citation:

        record = self.registry.get(
            document_id,
        )

        if record is None:

            document = Document(
                document_id=document_id,
                title=document_id,
                file_path="",
            )

        else:

            author_name = (
                record.author
                if record.author is not None
                else ""
            )

            authors: list[Author] = []

            if author_name:

                authors.append(
                    Author(
                        full_name=author_name,
                    )
                )

            domain = KnowledgeDomain()

            source = KnowledgeSource(
                name="local",
                domain=domain,
            )

            repository = Repository(
                repository_id="local",
                name="Local Repository",
                root_path=str(
                    Path(record.pdf_path).parent,
                ),
                source=source,
            )

            collection = Collection(
                collection_id="default",
                name="Default",
                repository=repository,
            )

            document = Document(
                document_id=record.id,
                title=record.title or record.id,
                file_path=str(
                    record.pdf_path,
                ),
                collection=collection,
                authors=authors,
            )

        return Citation(
            document=document,
            page=page_start,
            text=text,
            metadata={
                "page_start": page_start,
                "page_end": page_end,
                "section": section,
            },
        )
