from __future__ import annotations

from delbot_platform.documents.models.block import (
    Block,
)


class BlockExtractor:

    def extract(
        self,
        page,
    ) -> list[Block]:

        result: list[Block] = []

        data = page.get_text(
            "dict",
        )

        counter = 0

        for item in data.get(
            "blocks",
            [],
        ):

            if "lines" not in item:
                continue

            texts: list[str] = []

            font_sizes: list[float] = []

            font_names: list[str] = []

            is_bold = False

            for line in item["lines"]:

                for span in line["spans"]:

                    texts.append(
                        span["text"],
                    )

                    font_sizes.append(
                        span["size"],
                    )

                    font_names.append(
                        span["font"],
                    )

                    if "Bold" in span["font"]:
                        is_bold = True

            text = " ".join(
                texts,
            ).strip()

            if not text:
                continue

            counter += 1

            average_font_size = (
                sum(font_sizes) / len(font_sizes)
                if font_sizes
                else 0.0
            )

            font_name = (
                font_names[0]
                if font_names
                else ""
            )

            result.append(
                Block(
                    id=f"block-{counter}",
                    page=page.number + 1,
                    bbox=tuple(
                        item["bbox"]
                    ),
                    text=text,
                    block_type="text",
                    font_size=average_font_size,
                    font_name=font_name,
                    bold=is_bold,
                )
            )

        return result