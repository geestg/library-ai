from abc import ABC
from abc import abstractmethod

from time import perf_counter

from app.services.research.models.research_context import (
    ResearchContext,
)

from app.services.research.pipeline.stage_result import (
    StageResult,
)


class BaseStage(ABC):

    name = "base"

    priority = 100

    requires = []

    enabled = True

    # =====================================
    # PUBLIC ENTRYPOINT
    # =====================================

    def run(

        self,

        context: ResearchContext,

    ) -> StageResult:

        start = perf_counter()

        result = self.execute(
            context
        )

        if result is None:

            result = StageResult()

        result.duration_ms = (

            perf_counter() - start

        ) * 1000

        return result

    # =====================================
    # BUSINESS LOGIC
    # =====================================

    @abstractmethod
    def execute(

        self,

        context: ResearchContext,

    ) -> StageResult:

        ...