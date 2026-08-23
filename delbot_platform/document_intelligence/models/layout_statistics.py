from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field


@dataclass(slots=True, frozen=True)
class LayoutStatistics:
    """
    Aggregate statistics produced by the layout analysis stage.

    This model is intentionally immutable and contains no business logic.
    """

    page_count: int = 0

    block_count: int = 0
    empty_block_count: int = 0

    line_count: int = 0

    span_count: int = 0

    font_usage: dict[str, int] = field(
        default_factory=dict,
    )

    font_size_usage: dict[float, int] = field(
        default_factory=dict,
    )

    average_font_size: float = 0.0

    median_font_size: float = 0.0

    minimum_font_size: float = 0.0

    maximum_font_size: float = 0.0
