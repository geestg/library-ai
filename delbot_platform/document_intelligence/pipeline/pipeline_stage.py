from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any


class PipelineStage(ABC):

    @abstractmethod
    def process(
        self,
        data: Any,
    ) -> Any:
        ...
