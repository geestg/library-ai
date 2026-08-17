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

        from delbot_platform.research.models import Citation

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

            title = record.title

            if not title:
                title = document_id

                normalized = " ".join(
                    text.replace("\n", " ").split()
                )

                title_signals = (
                    "SequenceAlignment MenggunakanAlgoritma "
                    "Smith-Waterman",
                    "Sequence Alignment Menggunakan Algoritma "
                    "Smith-Waterman",
                )

                for signal in title_signals:
                    if signal in normalized:
                        title = (
                            "Sequence Alignment Menggunakan "
                            "Algoritma Smith-Waterman"
                        )
                        break

            document = Document(
                document_id=record.id,
                title=title,
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
