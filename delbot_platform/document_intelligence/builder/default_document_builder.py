from __future__ import annotations

from delbot_platform.document_intelligence.builder.document_builder import (
    DocumentBuilder,
)
from delbot_platform.document_intelligence.models.parsed_document import (
    ParsedDocument,
)
from delbot_platform.knowledge.models.document import (
    Document,
)


class DefaultDocumentBuilder(DocumentBuilder):

    def build(
        self,
        document: ParsedDocument,
    ) -> Document:

        return Document(
            title=document.title,
            file_path=document.file_path,
            metadata=document.metadata.copy(),
        )
