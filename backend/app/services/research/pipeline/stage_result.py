from dataclasses import dataclass, field

from typing import Any


@dataclass
class StageResult:

    """
    Standard result dari setiap stage.
    """

    success: bool = True

    stop_pipeline: bool = False

    skip_remaining: bool = False

    message: str = ""

    payload: dict = field(default_factory=dict)

    metadata: dict = field(default_factory=dict)

    duration_ms: float = 0.0

