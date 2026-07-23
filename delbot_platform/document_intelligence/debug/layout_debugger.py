from __future__ import annotations

from delbot_platform.document_intelligence.models.parsed_document import (
    ParsedDocument,
)


class LayoutDebugger:

    @staticmethod
    def dump(
        document: ParsedDocument,
        *,
        max_pages: int = 1,
        max_blocks: int = 5,
        max_lines: int = 5,
        max_spans: int = 5,
    ) -> None:

        print("=" * 80)
        print("LAYOUT DEBUG")
        print("=" * 80)

        for page in document.pages[:max_pages]:

            print(
                f"\nPAGE {page.page_number}"
            )

            print(
                f"Blocks : {len(page.blocks)}"
            )

            for block_index, block in enumerate(
                page.blocks[:max_blocks]
            ):

                print(
                    f"\n  BLOCK {block_index}"
                )

                print(
                    f"  Lines : {len(block.lines)}"
                )

                for line_index, line in enumerate(
                    block.lines[:max_lines]
                ):

                    print(
                        f"\n    LINE {line_index}"
                    )

                    print(
                        f"    Spans : {len(line.spans)}"
                    )

                    for span_index, span in enumerate(
                        line.spans[:max_spans]
                    ):

                        print(
                            f"      [{span_index}] "
                            f"{repr(span.text)}"
                        )

                        print(
                            f"          font={span.font_name}"
                        )

                        print(
                            f"          size={span.font_size}"
                        )

                        print(
                            f"          bbox={span.bbox}"
                        )
