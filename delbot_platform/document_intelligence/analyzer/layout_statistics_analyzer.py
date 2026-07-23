from __future__ import annotations

from collections import Counter
from statistics import median

from delbot_platform.document_intelligence.models.layout_statistics import (
    LayoutStatistics,
)
from delbot_platform.document_intelligence.models.parsed_document import (
    ParsedDocument,
)


class LayoutStatisticsAnalyzer:

    def analyze(
        self,
        document: ParsedDocument,
    ) -> LayoutStatistics:

        page_count = len(document.pages)

        block_count = 0
        empty_block_count = 0
        line_count = 0
        span_count = 0

        font_usage: Counter[str] = Counter()
        font_size_usage: Counter[float] = Counter()

        font_sizes: list[float] = []

        for page in document.pages:

            for block in page.blocks:

                block_count += 1

                if not block.lines:
                    empty_block_count += 1

                for line in block.lines:

                    line_count += 1

                    for span in line.spans:

                        span_count += 1

                        font_usage[span.font_name] += 1

                        font_size_usage[span.font_size] += 1

                        font_sizes.append(
                            span.font_size,
                        )

        if font_sizes:

            average_font_size = (
                sum(font_sizes)
                / len(font_sizes)
            )

            median_font_size = float(
                median(font_sizes),
            )

            minimum_font_size = min(
                font_sizes,
            )

            maximum_font_size = max(
                font_sizes,
            )

        else:

            average_font_size = 0.0
            median_font_size = 0.0
            minimum_font_size = 0.0
            maximum_font_size = 0.0

        return LayoutStatistics(
            page_count=page_count,
            block_count=block_count,
            empty_block_count=empty_block_count,
            line_count=line_count,
            span_count=span_count,
            font_usage=dict(font_usage),
            font_size_usage=dict(font_size_usage),
            average_font_size=average_font_size,
            median_font_size=median_font_size,
            minimum_font_size=minimum_font_size,
            maximum_font_size=maximum_font_size,
        )
