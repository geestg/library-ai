from __future__ import annotations

import sys
from pathlib import Path

from delbot_platform.documents.extraction.block import (
    BlockExtractor,
)

from delbot_platform.documents.loader.sources.local import (
    LocalDocumentSource,
)

from delbot_platform.documents.models.block import (
    Block,
)

from delbot_platform.documents.parser.backend.pymupdf import (
    PyMuPDFBackend,
)

from delbot_platform.documents.classification.document_type import (
    DocumentBlockType,
)


class DocumentExtractionService:
    """
    Extract document blocks from PDF.

    Primary path:
        PDF text layer
        -> PyMuPDF
        -> BlockExtractor

    Fallback path:
        Image-only PDF
        -> PyMuPDF render
        -> PaddleOCR
        -> Block objects
    """

    OCR_ROOT = Path(
        sys.prefix
    ) / "lib" / "python3.10" / "site-packages" / "paddleocr"

    def __init__(
        self,
    ) -> None:

        self.backend = PyMuPDFBackend()

        self.extractor = BlockExtractor()

        self.ocr = None

    def _load_ocr(
        self,
    ):

        if self.ocr is not None:
            return self.ocr

        import sys

        ocr_root = str(
            self.OCR_ROOT
        )

        site_root = str(
            Path(sys.prefix)
            / "lib"
            / "python3.10"
            / "site-packages"
        )

        paths = [
            ocr_root,
            site_root,
        ]

        for path in reversed(paths):

            if path not in sys.path:
                sys.path.insert(
                    0,
                    path,
                )

        workspace_tools = (
            Path.cwd()
            / "tools"
        )

        workspace_tools_str = str(
            workspace_tools
        )

        sys.path[:] = [
            item
            for item in sys.path
            if item != workspace_tools_str
        ]

        for module_name in list(sys.modules):
            if module_name == "tools" or module_name.startswith("tools."):
                del sys.modules[module_name]

        from paddleocr import (
            PaddleOCR,
        )

        self.ocr = PaddleOCR(
            use_angle_cls=True,
            use_gpu=False,
            show_log=False,
        )

        return self.ocr

    def _ocr_page(
        self,
        page,
        page_number: int,
    ) -> list[Block]:

        ocr = self._load_ocr()

        image_path = (
            Path("/tmp")
            / "delbot_ocr_pages"
        )

        image_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        target = (
            image_path
            / f"page_{page_number:04d}.png"
        )

        pixmap = page.get_pixmap(
            matrix=None,
            alpha=False,
        )

        pixmap.save(
            str(target)
        )

        result = ocr.ocr(
            str(target),
            cls=True,
        )

        blocks: list[Block] = []

        if not result:
            return blocks

        page_result = result[0]

        if not page_result:
            return blocks

        counter = 0

        for item in page_result:

            if not item or len(item) < 2:
                continue

            box = item[0]
            text_info = item[1]

            if not text_info:
                continue

            text = str(
                text_info[0]
            ).strip()

            confidence = float(
                text_info[1]
            )

            if not text:
                continue

            xs = [
                float(point[0])
                for point in box
            ]

            ys = [
                float(point[1])
                for point in box
            ]

            bbox = (
                min(xs),
                min(ys),
                max(xs),
                max(ys),
            )

            counter += 1

            blocks.append(
                Block(
                    id=(
                        f"ocr-{page_number}-"
                        f"{counter}"
                    ),
                    page=page_number,
                    bbox=bbox,
                    text=text,
                    type=(
                        DocumentBlockType.UNKNOWN
                    ),
                    font_size=0.0,
                    font_name="",
                    bold=False,
                    confidence=confidence,
                    metadata={
                        "source": "paddleocr",
                        "ocr": True,
                    },
                )
            )

        return blocks

    def extract(
        self,
        pdf_path: str,
    ) -> list[Block]:

        source = LocalDocumentSource(
            pdf_path,
        )

        self.backend.open(
            source,
        )

        blocks: list[Block] = []

        try:

            page_count = (
                self.backend.page_count()
            )

            for index in range(
                page_count,
            ):

                page = self.backend.page(
                    index,
                )

                page_blocks = (
                    self.extractor.extract(
                        page,
                    )
                )

                blocks.extend(
                    page_blocks,
                )

            if blocks:
                return blocks

            print(
                "TEXT_LAYER=ABSENT",
                flush=True,
            )

            print(
                "OCR_FALLBACK=START",
                flush=True,
            )

            for index in range(
                page_count,
            ):

                page = self.backend.page(
                    index,
                )

                ocr_blocks = (
                    self._ocr_page(
                        page,
                        index + 1,
                    )
                )

                blocks.extend(
                    ocr_blocks,
                )

                if (
                    index == 0
                    or (index + 1) % 25 == 0
                    or index + 1 == page_count
                ):

                    print(
                        f"OCR_PAGE={index + 1}/{page_count} "
                        f"BLOCKS={len(blocks)}",
                        flush=True,
                    )

            print(
                f"OCR_FALLBACK=COMPLETE BLOCKS={len(blocks)}",
                flush=True,
            )

        finally:

            self.backend.close()

        return blocks
