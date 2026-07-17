from __future__ import annotations


from delbot_platform.documents.classification.document_type import (
    DocumentBlockType,
)

from delbot_platform.documents.models.block import (
    Block,
)


class BlockExtractor:
    """
    Extract atomic document blocks from PDF pages.

    Responsibility:

    PDF Page
        |
        v
    Layout blocks
        |
        v
    Document Block objects

    This layer only extracts physical information.
    Semantic classification is handled by HeadingClassifier.
    """


    def extract(
        self,
        page,
    ) -> list[Block]:

        blocks: list[Block] = []

        data = page.get_text(
            "dict",
        )


        counter = 0


        for item in data.get(
            "blocks",
            [],
        ):


            #
            # Ignore image blocks
            #

            if "lines" not in item:

                continue



            texts: list[str] = []

            font_sizes: list[float] = []

            font_names: list[str] = []


            bold = False



            for line in item.get(
                "lines",
                [],
            ):


                for span in line.get(
                    "spans",
                    [],
                ):


                    text = span.get(
                        "text",
                        "",
                    )


                    if text:

                        texts.append(
                            text,
                        )


                    font_sizes.append(
                        float(
                            span.get(
                                "size",
                                0,
                            )
                        )
                    )


                    font_names.append(
                        span.get(
                            "font",
                            "",
                        )
                    )


                    font = span.get(
                        "font",
                        "",
                    )


                    if "Bold" in font:

                        bold = True



            content = " ".join(
                texts,
            ).strip()


            if not content:

                continue



            counter += 1



            average_font_size = (

                sum(font_sizes)
                /
                len(font_sizes)

                if font_sizes

                else 0.0

            )


            font_name = (

                font_names[0]

                if font_names

                else ""

            )



            blocks.append(

                Block(

                    id=f"block-{counter}",

                    page=page.number + 1,

                    bbox=tuple(
                        item["bbox"]
                    ),

                    text=content,


                    #
                    # semantic classification
                    # will happen later
                    #

                    type=DocumentBlockType.UNKNOWN,


                    font_size=average_font_size,

                    font_name=font_name,

                    bold=bold,


                    metadata={

                        "source": "pymupdf",

                    },

                )

            )


        return blocks