from __future__ import annotations

from ..loader.loaded_document import LoadedDocument

from ..models.block import Block
from ..models.bounding_box import BoundingBox
from ..models.line import Line
from ..models.page import Page
from ..models.parsed_document import ParsedDocument
from ..models.span import Span

from .document_parser import DocumentParser


class PDFParser(DocumentParser):

    def parse(
        self,
        document: LoadedDocument,
    ) -> ParsedDocument:

        pdf = document.backend_document

        pages = []

        for page_index in range(len(pdf)):

            fitz_page = pdf.load_page(page_index)

            text_dict = fitz_page.get_text("dict")

            blocks = []

            for block_dict in text_dict.get("blocks", []):

                if block_dict.get("type") != 0:
                    continue

                lines = []

                for line_dict in block_dict.get("lines", []):

                    spans = []

                    for span_dict in line_dict.get("spans", []):

                        bbox = span_dict.get("bbox")

                        spans.append(
                            Span(
                                text=span_dict.get("text", ""),
                                font_name=span_dict.get("font", ""),
                                font_size=float(
                                    span_dict.get("size", 0.0)
                                ),
                                is_bold=bool(
                                    span_dict.get("flags", 0) & 16
                                ),
                                is_italic=bool(
                                    span_dict.get("flags", 0) & 2
                                ),
                                bbox=(
                                    BoundingBox(
                                        left=bbox[0],
                                        top=bbox[1],
                                        right=bbox[2],
                                        bottom=bbox[3],
                                    )
                                    if bbox
                                    else None
                                ),
                            )
                        )

                    lines.append(
                        Line(
                            spans=spans,
                        )
                    )

                blocks.append(
                    Block(
                        lines=lines,
                    )
                )

            pages.append(
                Page(
                    page_index=page_index,
                    page_number=page_index + 1,
                    text=fitz_page.get_text("text"),
                    blocks=blocks,
                    metadata={},
                )
            )

        return ParsedDocument(
            source_document=document,
            pages=pages,
            headings=[],
            paragraphs=[],
        )
