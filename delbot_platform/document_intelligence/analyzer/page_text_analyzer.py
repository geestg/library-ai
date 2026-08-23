from __future__ import annotations

from delbot_platform.document_intelligence.analyzer.document_analyzer import (
    DocumentAnalyzer,
)
from delbot_platform.document_intelligence.models.parsed_document import (
    ParsedDocument,
)


class PageTextAnalyzer(DocumentAnalyzer):

    def analyze(
        self,
        document: ParsedDocument,
    ) -> ParsedDocument:

        for page in document.pages:

            line_texts: list[str] = []

            for block in page.blocks:

                for line in block.lines:

                    text = "".join(
                        span.text
                        for span in line.spans
                    ).rstrip()

                    if text:
                        line_texts.append(
                            text,
                        )

            page.text = "\n".join(
                line_texts,
            )

        return document
