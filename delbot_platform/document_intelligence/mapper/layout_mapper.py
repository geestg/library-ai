from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any

from delbot_platform.document_intelligence.models.page import (
    Page,
)


class LayoutMapper(ABC):

    @abstractmethod
    def build_page(
        self,
        page_index: int,
        page: Any,
    ) -> Page:
        ...
